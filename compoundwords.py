import sys
from successordict import SuccessorDict as sdict
import json
import gzip
import copy
import dawg
from operator import mul
import time

def memoize(f):
    """ Memoization decorator for a function taking a single argument """
    class memodict(dict):
        def __missing__(self, key):
            ret = self[key] = f(key)
            return ret 
    return memodict().__getitem__
    
with gzip.open('engmodel1.json.gz', 'rb') as f:
    countdict = json.load(f,object_pairs_hook=sdict)
ddawg = dawg.CompletionDAWG(countdict.keys())

@memoize
def tokenize(word):
    #print word
    prefices = ddawg.prefixes(word)
    l = []
    if word in countdict.keys():
        l = [[word]]
    for prefix in prefices[:-1]:
        suffix = word[len(prefix):]
        for tokenlist in tokenize(suffix):
            newlist = [prefix]
            newlist.extend(tokenlist) #tokenlist is an element of a memoized return value, so we must not modify it. CAN'T USE tokenlist.insert!
            if newlist not in l:
                l.append(newlist)
    return l

total = sum(countdict.values())
print total
wtd = {}

sys.stdout.write("Words loaded. Processing");sys.stdout.flush()
for i,word in enumerate(countdict.keys()):
    currelfreq = float(countdict[word])/total
    maxsofar = currelfreq
    bestsplit = word
    toks = tokenize(word)
    for tokenization in toks[1:]:
        if tokenization:
            score = reduce(mul, [countdict[j]/float(total) for j in tokenization])
            if score>maxsofar:
                maxsofar = score
                bestsplit = tokenization
    if maxsofar > currelfreq:
        sys.stdout.write("\nGoing to delete "+word);sys.stdout.flush()
        wtd[word] = bestsplit
    if not i%500:
        sys.stdout.write(".");sys.stdout.flush()
print "done!"
sys.stdout.write("Deleting uncommons");sys.stdout.flush()
for word,split in wtd.items():
    val = countdict[word]
    del countdict[word]
    for token in split:
        countdict[token] += val
print "done!"
sys.stdout.write("Saving new model...");sys.stdout.flush()
with gzip.open('engmodel3.json.gz', 'wb') as f:
    f.write(json.dumps(countdict, f, separators=(',',':')))
print "done!"""