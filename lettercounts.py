import json
from collections import defaultdict as ddict
import sys 
import gzip
import cStringIO

sys.stdout.write("Reading in words...");sys.stdout.flush()
with gzip.open('bwordcounts.json.gz', 'rb') as f:
    bcountdict = ddict(int,json.loads(f.read()))
    
with gzip.open('cwordcounts.json.gz', 'rb') as f:
    words = ddict(int,json.loads(f.read()))
print "done!"
sys.stdout.write("Combining dictionaries...");sys.stdout.flush()
words.update(bcountdict)
print "done!"
chars = ddict(int)
c=0
w=0
t=0
ws=0
tick=len(words)/20
sys.stdout.write("Counting characters");sys.stdout.flush()
word=""
for word,count in sorted(words.items()):
    ws+=count
    for char in word:
        chars[char]+=1
        t+=1
    w+=1
    if w-c*tick>tick:
        sys.stdout.write(".");sys.stdout.flush()
        c+=1
print "done!"
sys.stdout.write("Rescaling to target weight...");sys.stdout.flush()
tweight = ws/4
for char,val in sorted(chars.items()):
    words[char] += int(tweight/float(t)*val)
print "done!"
"""sys.stdout.write("Computing cumulative sums...");sys.stdout.flush()
cumsum = 0
for key, value in sorted(words.items()):
    cumsum += value
    words[key]=cumsum
print "done!"""

sys.stdout.write("Writing model to file...");sys.stdout.flush()
with gzip.open('engmodel1.json.gz', 'wb') as f:
    f.write(json.dumps(words, f, sort_keys=True, separators=(',',':')))

print "done!"
