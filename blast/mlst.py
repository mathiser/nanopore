#!/usr/bin/env python3
# Upload contigs file to PubMLST rMLST species identifier via RESTful API
# Written by Keith Jolley
# Copyright (c) 2018, University of Oxford
# Licence: GPL3
import os
import sys, requests, argparse, base64, json
from multiprocessing.pool import ThreadPool
from pprint import pprint

parser = argparse.ArgumentParser()
parser.add_argument('--file', '-f', type=str, default='.', help='folder containing .json-files')
args = parser.parse_args()



def main():
    assemblies = []
    for fol, subs, files in os.walk(args.file):
        for fil in files:
            if fol.split("/")[-1] == "1":
                if fil.endswith(".fasta") and os.path.getsize(os.path.join(fol, fil)) != 0:
                    assemblies.append(os.path.join(fol, fil))

    print(len(assemblies))
    # for ass in assemblies:
    #     blast(ass)
    threads = ThreadPool(2)
    threads.map(blast, assemblies)
    threads.close()
    threads.join()


def blast(file):
    uri = 'http://rest.pubmlst.org/db/pubmlst_rmlst_seqdef_kiosk/schemes/1/sequence'
    with open(file, 'r') as x:
        fasta = x.read()

    payload = '{"base64":true,"details":true,"sequence":"' + base64.b64encode(fasta.encode()).decode() + '"}'
    print("posting: %s" %file)
    response = requests.post(uri, data=payload)
    if response.status_code == requests.codes.ok:
        data = response.json()
        # pprint(data)
        with open(file.replace(".fasta", "_mlst.json"), "w") as f:
            f.write(json.dumps(data))
            print("done med fil: %s" % file)
    else:
        blast(file)
        print(response.status_code)
        print("trying again with: %s" % file)


if __name__ == "__main__":
    main()