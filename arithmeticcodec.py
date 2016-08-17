import blackjack
import bitqueue
from fractions import *
import math
import dawg
from collections import defaultdict as ddict
import time

class ArithmeticCodec:
    
    def split_first_token(self,s):
        """Find the longest possible token at the beginning of the string and split the string on it"""
        # thanks to Mikhail Korobov and contributors for DAWG. much easier to make this project faster with it.
        word = ""
        prefices = self._tokens.prefixes(s)
        if prefices:
            word = prefices[-1]
        return word,s[len(word):]
    
    def __init__(self,dictionary,upper):
        """
        dictionary maps symbols to ranges (tuples)
        upper is the total of all frequencies in the dictionary
        """
        self._encodemap = dictionary
        def key_func(value):
            """
            for the purpose of insertion, the key is the median of the range
            """
            return (value[1][0]+value[1][1])/2.
        sys.stdout.write("building tree...");sys.stdout.flush()
        curtime = time.time()
        self._decodemap = blackjack.BJ(iterable=dictionary.items(),key=key_func)
        print "%f secs"%(time.time()-curtime)
        sys.stdout.write("building DAFSA...");sys.stdout.flush()
        curtime = time.time()
        self._tokens = dawg.CompletionDAWG(dictionary.keys())
        print "%f secs"%(time.time()-curtime)
        self._upper = upper
    
    def encode(self,string,code=bitqueue.BitQueue()):
        """Given a string and a bitqueue, arithmetically encode the string and push the result directly into the queue and return it
        If no bitqueue is provided, return a fresh one containing only the encoded string."""
        lower = Fraction(0)
        upper = Fraction(1)
        # loop through symbols and do arithmetic coding
        w,string = self.split_first_token(string)
        while w:
            lb, ub = _encodemap[w]
            range = upper-lower
            upper = lower + (range * ub / self._upper)
            lower = lower + (range * lb / self._upper)
            # push out a bit to simplify fractions whenever possible (for speed and memory)
            if lower > .5:
                code.pushBit(1)
                upper = 1-2*upper
                lower = 2*lower-1
            elif upper < .5:
                code.pushBit(0)
                upper *= 2
                lower *= 2
            w,string = split_first_token(string)
        #Find the first binary fraction denominator big enough to guarantee there is at least one in the range
        binlength = (upper-lower).denominator.bit_length()
        #Find a numerator in the range
        binnumer = math.ceil(lower*(1<<binlength))
        #push it
        code.pushNum(binnumer,binlength+(lower==1))
        return code
    
    def decode(self,s,stop):
        """Given a bitstring containing only an encoded string, and a stop symbol
        decode the string up to and including the stop symbol and return it."""
        #Thanks to Corbin Simpson for red/black tree implementation. Happy to not have to implement a fast tree data structure myself.
        def cmp_func(comp, other):
            """
            the first argument is a number, the second is one of the items we are looking for
            we check whether the number is in its range, before its range, or after its range
            """
            if comp <= other[1][0]:
                return -1
            elif comp > other[1][1]:
                return 1
            else:
                assert other[1][0] < comp <= other[1][1]
                return 0
        symbol = ""
        output=""
        location = Fraction(int(s,2),2**len(s))
        while symbol != stop:
            #blackjack finds the symbol in logarithmic time
            symbol,bounds = self._decodemap.find_cmp(location,cmp_func)
            output+=symbol
            #correct location to remove effect of removed symbol
            range = Fraction(bounds[1]-bounds[0],self._upper)
            location = (location-Fraction(bounds[0],self._upper))/range
        return output
if __name__=="__main__":
    import gzip
    import cStringIO
    from collections import defaultdict as ddict
    import json
    import sys
    import modelbuilder
    
    sys.stdout.write("Loading and compiling english model...");sys.stdout.flush()
    with gzip.open('engmodel1.json.gz', 'rb') as f:
        countdict = ddict(int,json.loads(f.read()))
    model,upper = modelbuilder.build_model(countdict)
    print "done."
    sys.stdout.write("Creating arithmetic coder based on model...");sys.stdout.flush()
    ac = ArithmeticCodec(model,upper)
    print "done."
    sys.stdout.write("Encoding test string...");sys.stdout.flush()
    bq = ac.encode("Hello world")
    print "done."
    count = 0
    for bit in bq.bit_iterator():
        sys.stdout.write(str(bit))
        count+=1
        if not count%100: sys.stdout.write("\n")