import json
import os
from pprint import pprint

jsons = {}
for fol, subs, files in os.walk("/mnt/genomedk1/faststorage/endo/out/201901310943/merged"):
    for file in files:
        if file.endswith("_mlst.json") and "dose-response" not in fol:
            f = open(os.path.join(fol, file), 'r')
            s = fol.split("/")
            print(fol)
            jsons[s[-2]+'_'+s[-1]] = json.loads(f.read())


open("matches.txt", 'w').write("")
f = open("matches.txt", 'a')
for k, v in jsons.items():
    f.write(k+";"+str(len(v['exact_matches'])) +";")
    print(k, len(v['exact_matches']))
    try:
        for i in v['taxon_prediction']:
            f.write(i['taxon'] + ';' + str(i['support']))
            f.write("\n")
    except Exception as e:
        print(e)
        f.write("\n")