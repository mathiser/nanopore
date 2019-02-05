# !/home/mathiser/anaconda3/bin/python

import os, sys, getopt
import time
from multiprocessing.dummy import Pool as ThreadPool
from queue import Queue
from threading import Thread

class Sumtools():
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = ''
        self.outputfile = ''
        self.command = ''
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
            Deplexer(self.inputfile, self.outputfol)
        else:
            print(self.helpline)


class Deplexer:
    def __init__(self, input, output):
        self.header = ''
        self.inputfile = input
        self.outputfile = output


        self.barcodes = {} ##k=barcode, v=file

        self.read_file()
        self.close_files()

    def read_file(self):
        r = open(self.inputfile, 'r')
        line = r.readline()
        if line == '': return

        self.header = line
        self.splitted_header = self.header.replace("\n", "")
        self.splitted_header = self.splitted_header.split("\t")
        self.barcode_arrangement = self.splitted_header.index('barcode_arrangement')

        counter = 0
        while line != '':
            line = r.readline()
            if line == '': break
            self.assign_line(line)
            counter += 1
            print(counter)

    def assign_line(self, line):
        bc = line.split("\t")[self.barcode_arrangement]
        if bc not in self.barcodes.keys():

            if not os.path.exists(os.path.join(self.outputfile, bc)):
                os.makedirs(os.path.join(self.outputfile, bc))

            (open(os.path.join(self.outputfile, bc, "sequencing_summary.txt"), 'w')).write(self.header)
            self.barcodes[bc] = open(os.path.join(self.outputfile, bc, "sequencing_summary.txt"), 'a')

        self.barcodes[bc].write(line)

    def close_files(self):
        for bc, file in self.barcodes.items():
            file.close()


if __name__ == "__main__":
    main = Sumtools(sys.argv[1:])
