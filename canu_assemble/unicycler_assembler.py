import getopt
import os
import sys
import threading


class unicycler_assembler():
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = ""
        self.outputfile = ""
        self.load_args()
        self.unicycle()

    def load_args(self):
        try:
            opts, args = getopt.getopt(self.argv, "hi:o:", ["inputfile=", "outputfile="])
        except getopt.GetoptError:
            print('unicycle_assembler.py -i <inputfile> -o <outputfile>')
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print('unicycle_assembler.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i"):
                self.inputfile = arg
            elif opt in ("-o"):
                self.outputfile = arg


    def unicycle(self):
        for fol, sub, files in os.walk(self.inputfile):
            for file in files:
                print(file)
                if ".fastq" in file:
                    opf = os.path.join(self.outputfile, file.replace(".fastq",''))
                    os.makedirs(opf)
                    os.system("unicycler -l {} -o {}".format(os.path.join(fol, file), opf))



u = unicycler_assembler(sys.argv[1:])
