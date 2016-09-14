import sys
from successordict import SuccessorDict as sdict
import json
import gzip
import copy
import dawg
from operator import mul
import time
import progressbar
from repoze.lru import lru_cache
    
with gzip.open('engmodel1.json.gz', 'rb') as f:
    countdict = json.load(f,object_pairs_hook=sdict)
ddawg = dawg.CompletionDAWG(countdict.keys())

@lru_cache(30000)
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
length = len(countdict)
print "Words loaded. Processing..."
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
        wtd[word] = bestsplit
        for token in bestsplit:
            if token in wtd.keys():
                del wtd[token]
        #sys.stdout.write("\nGoing to delete "+word);sys.stdout.flush()
        
    if not i%500:
        progressbar.printProgress(i,length)
print "done!"
sys.stdout.write("Deleting uncommons...");sys.stdout.flush()
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