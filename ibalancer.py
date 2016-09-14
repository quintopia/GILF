from collections import OrderedDict as odict
import math
import sys
import gzip
import json

sys.stdout.write("Reading in words...");sys.stdout.flush()
with gzip.open('engmodel1.json.gz', 'rb') as f:
    dictionary = odict(json.loads(f.read()))
acount = 0
icount = 0
tcount = 0
print "done."
print "i standalone frequency",dictionary["i"]
print "o standalone frequency",dictionary["a"]
print "n standalone frequency",dictionary["t"]
sys.stdout.write("Counting all occurrences...");sys.stdout.flush()
for key in dictionary.keys():
    acount += key.count("a")
    tcount += key.count("t")
    icount += key.count("i")
print "done."
print "a frequency",acount
print "i frequency",icount
print "t frequency",tcount