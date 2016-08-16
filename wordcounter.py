import json
from collections import defaultdict as ddict
import sys 
import gzip
import cStringIO

sys.stdout.write("Reading in words...");sys.stdout.flush()
wordfile = open('words.txt','r')
words = wordfile.read().split('\n'); wordfile.close()
print "done."
with gzip.open('bwordcounts.json.gz', 'rb') as f:
    countdict = ddict(int,json.loads(f.read()))
#countdict = ddict(int)
print "Processing words..."
with open('zwords.txt','r') as countfile:
    for n,line in enumerate(countfile):
        parts = line.split()
        word = parts[0].lower()
        if word not in words: continue
        if not n%500: print word
        countdict[word] += int(parts[2])
print "done."
sys.stdout.write("Writing counts to file...");sys.stdout.flush()

with gzip.open('bwordcounts.json.gz', 'wb') as f:
    f.write(json.dumps(countdict, f, sort_keys=True, separators=(',',':')))

print "done!"