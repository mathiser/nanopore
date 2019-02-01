# !/home/mathiser/anaconda3/bin/python

import os, sys, getopt
from multiprocessing.dummy import Pool as ThreadPool
from queue import Queue
from threading import Thread

class Sumtools():
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = ''
        self.outputfile = ''
        self.command = ''
        self.threads = 16
        self.helpline = "sumtools.py -i <inputfile> -o <outputfol> -t <threads> -x <deplex>"
        self.load_args()


    def load_args(self):
        try:
            opts, args = getopt.getopt(self.argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print(self.helpline)
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print(self.helpline)
                sys.exit()
            elif opt in ("-i"):
                self.inputfile = arg
            elif opt in ("-o"):
                self.outputfol = arg
                if not os.path.exists(self.outputfol):
                    os.makedirs(self.outputfol)
            elif opt in ("-t"):
                self.threads = arg
            elif opt in ("-x"):
                self.command = arg
            else:
                print(self.helpline)

        print('Input file is "', self.inputfile)
        print('Output fol is "', self.outputfol)

        if self.command in ["deplex", '']:
            Deplexer(self.inputfile, self.outputfol, self.threads)
        else:
            print(self.helpline)



class Deplexer:
    def __init__(self, input, output, threads):
        self.header = ''
        self.inputfile = input
        self.outputfile = output
        self.threads = threads

        self.barcodeQueue = Queue()
        self.barcodeThreads = {} ##k=barcode, v=BarcodeThread

        self.t = Thread(target=self.barcode_adder)
        self.t.start()

        self.read_file()
        self.report()
        self.close_threads()

    def read_file(self):
        r = open(self.inputfile, 'r')
        line = r.readline()
        if line == '': return

        self.header = line
        self.splitted_header = self.header.replace("\n", "")
        self.splitted_header = self.splitted_header.split("\t")
        self.barcode_arrangement = self.splitted_header.index('barcode_arrangement')

        while line != '':
            queue = []
            for i in range(0, 50000):
                line = r.readline()
                if line == '': break
                queue.append(line)

            pool = ThreadPool(self.threads)
            pool.map(self.assign_line, queue)
            pool.close()
            pool.join()

    def assign_line(self, line):
        bc = line.split("\t")[self.barcode_arrangement]
        try:
            self.barcodeThreads[bc].add(line)
        except Exception as e:
            # print(e)
            self.barcodeQueue.put((bc, line))

    def barcode_adder(self):
        while True:
            bc, line = self.barcodeQueue.get()
            if not bc in self.barcodeThreads.keys():
                self.barcodeThreads[bc] = self.BarcodeThread(name=bc, header=self.header,
                                                        outputfol=os.path.join(self.outputfile, bc))
            else:
                self.assign_line(line)

            self.barcodeQueue.task_done()

    def close_threads(self):
        self.t.join()
        for bc, t in self.barcodeThreads.items():
            t.close_thread()


    def report(self):
        for bc, t in self.barcodeThreads.items():
            print("{} deplexed to: {}".format(t.file_count, bc))

    class BarcodeThread():
        def __init__(self, name, header, outputfol):
            self.queue = Queue()
            self.name = name
            self.header = header
            self.outputfol = outputfol
            self.filename = os.path.join(self.outputfol, "sequencing_summary.txt")
            self.file_count = 0

            if not os.path.exists(self.outputfol):
                os.makedirs(self.outputfol)

            (open(self.filename, 'w')).write(self.header)
            self.file = open(self.filename, 'a')
            print("Barcode thread started: %s"%self.name)
            self.t = Thread(target=self.executer)
            self.t.start()

        def add(self, line):
            self.queue.put(line)

        def close_thread(self):
            self.t.join()

        def close_file(self):
            self.file.close()

        def save_file(self):
            self.file.close()
            self.file = open(self.filename, 'a')

        def executer(self):
            counter = 0
            while True:
                line = self.queue.get()## HER SKER DER TIMEOUT. DERFOR STOPPER PROGRAMMET IKKE.
                self.file.write(line)
                counter += 1
                self.file_count += 1

                if counter == 3000:
                    self.save_file()
                    counter = 0

                self.queue.task_done()



if __name__ == "__main__":
    main = Sumtools(sys.argv[1:])
