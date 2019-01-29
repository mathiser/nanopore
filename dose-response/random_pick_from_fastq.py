import sys
import random

from Bio.SeqIO.QualityIO import FastqGeneralIterator
count = 0
total_len = 0
with open(sys.argv[2]) as in_handle:
    for title, seq, qual in FastqGeneralIterator(in_handle):
        count += 1
        total_len += len(seq)

random.randint(0, count)