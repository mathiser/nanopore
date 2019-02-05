# !/home/mathiser/anaconda3/bin/python

import os, sys, getopt

class fast5merger:
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = ''
        self.outputfile = ''
        self.barcodefol = ''
        self.filter = ''
        self.barcodes = {}
        self.sequence = []

        self.load_args()

        self.make_output_tree()
        self.merge_fastq()
        self.merge_summaries()

    def load_args(self):
        try:
            opts, args = getopt.getopt(self.argv, "hi:o:", ["ifile=", "ofile="])
        except getopt.GetoptError:
            print('fast5merger.py -i <inputfile> -o <outputfile> -f <filter>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('fast5merger.py -i <inputfile> -o <outputfile> -f <optional: empty/fail/pass')
                sys.exit()
            elif opt in ("-i"):
                self.inputfile = arg
            elif opt in ("-o"):
                self.outputfile = arg
                self.outputfile = os.path.join(self.outputfile, "merged")
            elif opt in ("-f"):
                self.filter = arg

        print('Input file is "', self.inputfile)
        print('Output file is "', self.outputfile)

    def make_output_tree(self):
        print("Creating output files ...")
        for fol, subs, files in os.walk(self.inputfile):
            for sub in subs:
                if "barcode" in sub or 'unclassified' in sub:
                    if not sub in self.barcodes.keys():
                        self.barcodes[sub] = []

            for bc, l in self.barcodes.items():
                for fil in files:
                    if bc in fol and fil.endswith("_porechopped.fastq"):
                        if self.filter == '':
                            self.barcodes[bc].append(os.path.join(fol, fil))
                        elif self.filter in fol:
                            self.barcodes[bc].append(os.path.join(fol, fil))
                        else:
                            pass

            for fil in files:
                if "sequencing_summary.txt" in fil:
                    self.sequence.append(os.path.join(fol, fil))

        for bc, l in self.barcodes.items():
            if not os.path.exists(os.path.join(self.outputfile, bc)):
                os.makedirs(os.path.join(self.outputfile, bc))

    def merge_fastq(self):
        print("Merging fastqs")
        for bc, l in self.barcodes.items():
            for fil in l:
                with open(os.path.join(self.outputfile, bc, "{}.fastq".format(bc)), 'a') as f:
                    f.write(open(fil, 'r').read())

    def merge_summaries(self):
        print("Merging sequence_summaries")
        with open(os.path.join(self.outputfile, "sequencing_summary.txt"), 'w') as f:
            f.write((open(self.sequence[0], 'r').readline()))

        for fil in self.sequence:
            with open(os.path.join(self.outputfile, "sequencing_summary.txt"), 'a') as f:
                with open(fil, 'r') as r:
                    for line in r.readlines()[1:]:
                        f.write(line)

        print("Done")
        
if __name__ == "__main__":
    main = fast5merger(sys.argv[1:])
