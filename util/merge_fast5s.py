# !/home/mathiser/anaconda3/bin/python

import os, sys, getopt

class fast5merger():
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = ''
        self.outputfile = ''
        self.barcodefol = ''
        self.load_args()
        self.barcodes = {}
        self.sequence = {}

        self.make_output_tree()
        self.merge_files()

    def load_args(self):
        try:
            opts, args = getopt.getopt(self.argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print('fast5merger.py -i <inputfile> -o <outputfile>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('fast5merger.py -i <inputfile> -o <outputfile>')
                sys.exit()
            elif opt in ("-i"):
                self.inputfile = arg
            elif opt in ("-o"):
                self.outputfile = arg
        print('Input file is "', self.inputfile)
        print('Output file is "', self.outputfile)

    def make_output_tree(self):
        print("Creating output files ...")
        for fol, subs, files in os.walk(self.inputfile):
            for sub in subs:
                if "barcode" in sub:
                    if not sub in self.barcodes.keys():
                        self.barcodes[sub] = []
                        self.sequence[sub] = []

            for bc, l in self.barcodes.items():
                for fil in files:
                    if bc in fol and "pass" in fol and fil.endswith(".fastq"):
                        self.barcodes[bc].append(os.path.join(fol, fil))
                        
                    if "sequencing_summary.txt" in fil:
                        self.sequence[bc].append(os.path.join(fol, fil))
                        
        self.barcodefol = os.path.join(self.outputfile, "fastq")

        if not os.path.exists(self.barcodefol):
            os.makedirs(os.path.join(self.barcodefol))

        for bc, l in self.barcodes.items():
            with open(os.path.join(self.barcodefol, "{}.fastq".format(bc)), 'w') as f:
                f.write("")

        with open (os.path.join(self.outputfile, "sequencing_summary.txt"), 'w') as f:
            f.write("")

    def merge_files(self):

        print("Merging fastqs")        
        for bc, l in self.barcodes.items():
            for fil in l:
                with open(os.path.join(self.barcodefol, "{}.fastq".format(bc)), 'a') as f:
                    f.write(open(fil, 'r').read())
                    #print(open(fil, 'r').read())
                    #pass
        
        print("Merging sequence_summaries")
        for bc, l in self.sequence.items():
            for fil in l:
                with open(os.path.join(self.outputfile, "sequencing_summary.txt"), 'a') as f:
                    f.write(open(fil, 'r').read())
                    f.write("\n")
                    #print(open(fil, 'r').read())

        print("Done")
        
if __name__ == "__main__":
    main = fast5merger(sys.argv[1:])
