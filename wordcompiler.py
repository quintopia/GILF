import json
from collections import defaultdict as ddict
import sys 
import gzip
import cStringIO

sys.stdout.write("Reading in words...");sys.stdout.flush()
with gzip.open('bwordcounts.json.gz', 'rb') as f:
    bcountdict = ddict(int,json.loads(f.read()))
    
with gzip.open('cwordcounts.json.gz', 'rb') as f:
    countdict = ddict(int,json.loads(f.read()))
print "done!"
sys.stdout.write("Combining dictionaries...");sys.stdout.flush()
countdict.update(bcountdict)
print "done!"


