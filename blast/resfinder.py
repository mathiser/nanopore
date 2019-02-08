import argparse
import json
import os
from pprint import pprint
from multiprocessing.pool import Pool


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--file', '-f', type=str, default='.', help='folder containing .json-files')
        self.parser.add_argument('--prefix', '-p', type=str, default='', help='')

        self.args = self.parser.parse_args()
        Resfinder(self.args.file, self.args.prefix)

class Resfinder:
    resFinderPath = "/home/l/nanoporeproj/apps/resfinder/resfinder.py"
    dbPath = "/home/l/nanoporeproj/apps/resfinder_db/"
    t = "0.9"
    l = "0.6"
    folfiles = []
    def __init__(self, file, prefix):
        self.file = file
        self.prefix = prefix

        for fol, subs, files in os.walk(file):
            for file in files:
                if os.path.getsize(os.path.join(fol, file)) == 0: continue
                if file.endswith(".fasta") and fol.split("/")[-1] == "1" and "APOMMIR" in fol:
                    self.folfiles.append((fol, file))

        pool = Pool(16)
        pool.map(self.resser, self.folfiles)
        pool.close()
        pool.join()


    def resser(self, folfile):
        fol, file = folfile
        outfile = os.path.join(self.prefix, fol.split("/")[-2])
        if not os.path.exists(outfile): os.makedirs(outfile)
        os.system("python {} -i {} -o {} -p {} -t {} -l {}".format(self.resFinderPath, os.path.join(fol, file), outfile,
                                                                 self.dbPath, self.t, self.l))


if __name__ == "__main__":
    Main()
