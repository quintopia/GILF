import sys
from successordict import SuccessorDict as sdict
import json
import gzip
import copy
import dawg
from operator import mul

    
with gzip.open('engmodel1.json.gz', 'rb') as f:
    countdict = json.load(f,object_pairs_hook=sdict)
ddawg = dawg.CompletionDAWG(countdict.keys())

def tokenize(word):
    #print word
    prefices = ddawg.prefixes(word)
    l = []
    if word in countdict.keys():
        l = [[word]]
    for prefix in prefices[:-1]:
        suffix = word[len(prefix):]
        #import pdb;pdb.set_trace()
        for tokenlist in tokenize(suffix):
            tokenlist.insert(0,prefix)
            if tokenlist not in l:
                l.append(tokenlist)
    return l

print tokenize(u"wholesome")
"""total = countdict[countdict.last_key()]

sys.stdout.write("Words loaded. Processing");sys.stdout.flush()
for i,word in enumerate(countdict.keys()):
    currelfreq = float(countdict[word])/total
    maxsofar = currelfreq
    bestsplit = word
    toks = tokenize(word) 
    if toks:
        print toks[0]
    for tokenization in tokenize(word):
        print tokenization
        if tokenization:
            score = float(reduce(mul, [countdict[j] for j in tokenization]))/total**len(tokenization)
            if score>maxsofar:
                maxsofar = score
                bestsplit = tokenization
    if maxsofar > currelfreq:
        val = countdict[word]
        del countdict[word]
        sys.stdout.write("\nDeleted "+word);sys.stdout.flush()
        for token in bestsplit:
            countdict[token] += val
    if not i%500:
        sys.stdout.write(".");sys.stdout.flush()

print "done!"
sys.stdout.write("Saving new model...");sys.stdout.flush()
with gzip.open('engmodel3.json.gz', 'wb') as f:
    f.write(json.dumps(countdict, f, separators=(',',':')))
print "done!"""