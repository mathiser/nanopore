import argparse
import json
import os
from pprint import pprint


class Main:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--file', '-f', type=str, default='.', help='folder containing .json-files')
        self.parser.add_argument('--command', '-c', type=str, default='je', help='<je>, <ao>')
        self.parser.add_argument('--prefix', '-p', type=str, default='', help='')

        self.args = self.parser.parse_args()
        if self.args.command == "je":
            JsonExtracter(self.args.file, self.args.prefix)
        elif self.args.command == "ao":
            AssemblyOverview(self.args.file, self.args.prefix)
        elif self.args.command == "amrex":
            AmrExtracter(self.args.file, self.args.prefix)

class AssemblyOverview:
    def __init__(self, file, prefix):
        open("%s_assembly_paths.txt" %prefix, 'w').write("")
        for fol, subs, files in os.walk(file):
            for file in files:
                if os.path.getsize(os.path.join(fol, file)) == 0: continue

                if file.endswith(".fasta") and fol.split("/")[-1] == "1" and "APOMMIR" in fol:
                    filename = os.path.join(fol, file)
                    with open("%s_assembly_paths.txt" %prefix, 'a') as f:
                        f.write(filename)
                        f.write("\n")



class JsonExtracter:
    def __init__(self, file, prefix):
        jsons = {}
        for fol, subs, files in os.walk(file):
            # print(files)
            for file in files:
                if file.endswith("_mlst.json") and fol.split("/")[-1] == "1" and "APOMMIR" in fol:
                    r = open(os.path.join(fol, file), 'r')

                    s = fol.split("/")
                    print(s[-2]+'_'+s[-1])
                    try:
                        jsons[s[-2]+'_'+s[-1]] = json.loads(r.read())
                    except Exception as e:
                        print(e, os.path.join(fol, file))
                    r.close()

        pprint(jsons)
        open("%s_matches.txt"%prefix, 'w').write("")
        fr = open("%s_matches.txt"%prefix, 'a')

        for k, v in jsons.items():
            try:
                v['taxon_prediction']
                fr.write(k+";"+str(len(v['exact_matches'])) +";")
                for i in v['taxon_prediction']:
                    fr.write(i['taxon'] + ';' + str(i['support']))
                    fr.write("\n")
            except KeyError as e:
                pass
        fr.close()

class AmrExtracter:

    def __init__(self, file, prefix):
        jsons = {}
        for fol, subs, files in os.walk(file):
            for file in files:
                if file == "results_table.txt" and os.path.getsize(os.path.join(fol, file)) != 0:
                    print(os.path.join(fol, file))
                    print("SÅ SKER DET: " + open(os.path.join(fol, file), 'r').read())



if __name__ == "__main__":
    Main()