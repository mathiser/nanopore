import getopt
import sys

from Bio.Blast import NCBIWWW, NCBIXML
from Bio import SeqIO

class blaster():
    def __init__(self, argv):
        self.argv = argv
        self.inputfile = "/mnt/genomedk1/faststorage/endo/out/unicycled/barcode09/assembly.fasta"
        self.outputfile = "./"
        self.db = 'nt'
        self.record = ''
        self.result_handle = ''
        
        #self.load_args()
        self.load_file()
        #self.blast()
        #self.print_results()
        #self.test()

    def load_args(self):
        try:
            opts, args = getopt.getopt(self.argv, "hi:o:db", ["inputfile=", "outputfile="])
        except getopt.GetoptError:
            print('merger.py -i <inputfile> -o <outputfile> -db <nt/16s/ASR>')
            sys.exit(2)
        
        for opt, arg in opts:
            if opt == '-h':
                print('merger.py -i <inputfile> -o <outputfile> -db <nt/16s/ASR>')
                sys.exit()
            elif opt in ("-i"):
                self.inputfile = arg
            elif opt in ("-o"):
                self.outputfile = arg
            elif opt in ("-db"):
                self.db = arg

    def load_file(self):
        self.fasta = open(self.inputfile).read()
		
    def blast(self):
        self.result_handle = NCBIWWW.qblast("blastn", self.db, self.fasta)
        # print(self.result_handle)

    def print_results(self):
        self.blast_records = NCBIXML.parse(self.result_handle)
        E_VALUE_THRESH = 0.04
        for br in self.blast_records[:1]:
            for alignment in br.alignments:
                for hsp in alignment.hsps:
                    if hsp.expect < E_VALUE_THRESH:
                        print("****Alignment****")
                        print("sequence:", alignment.title)
                        print("length:", alignment.length)
                        print("e value:", hsp.expect)

    def save_file(self):
        save_file = open("{}.xml".format(self.inputfile.split('/')[1].split(".")[0]), "w")
        save_file.write(self.result_handle)
        save_file.close()


    def read_file(self):
        print(self.inputfile)
        for seq_record in SeqIO.parse(self.inputfile, format=self.inputfile.split(".")[-1]):
            print(seq_record.id)
            print(repr(seq_record.seq))
            print(len(seq_record))


n = blaster(sys.argv[1:])