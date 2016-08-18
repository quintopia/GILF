import bisect
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
    
    def __init__(self,model,words,breakpoints):
        """
        dictionary maps symbols to ranges (tuples)
        words is a list of words sorted in the same order as the corresponding breakpoints in breakpoints
        breakpoints is the right (excluded) boundary of the interval of the corresponding word in words
        upper is the total of all frequencies in the dictionary
        """
        self._words = words
        self._breakpoints = breakpoints
        self._encodemap = model
        self._tokens = dawg.CompletionDAWG(words[:-1])
        self._upper = breakpoints[-1]
    
    def encode(self,string,code=bitqueue.BitQueue()):
        """Given a string and a bitqueue, arithmetically encode the string and push the result directly into the queue and return it
        If no bitqueue is provided, return a fresh one containing only the encoded string."""
        lower = Fraction(0)
        upper = Fraction(1)
        # loop through symbols and do arithmetic coding
        w,string = self.split_first_token(string)
        while w:
            lb, ub = self._encodemap[w]
            range = upper-lower
            upper = lower + (range * ub / self._upper)
            lower = lower + (range * lb / self._upper)
            # push out a bit to simplify fractions whenever possible (for speed and memory)
            if lower > .5:
                code.pushBit(1)
                upper = 2*upper-1
                lower = 2*lower-1
            elif upper < .5:
                code.pushBit(0)
                upper *= 2
                lower *= 2
            w,string = self.split_first_token(string)
        #now push a stop symbol
        lb,ub = self._encodemap[-1]
        range = upper-lower
        upper = lower + (range * ub / self._upper)
        lower = lower + (range * lb / self._upper)
        #now pull out bits until this range is unambiguous (includes 0)
        while not lower<=0<upper:
            if upper>.5:
                code.pushBit(1)
                upper = 2*upper-1
                lower = 2*lower-1
            else:
                code.pushBit(0)
                upper *= 2
                lower *= 2
        return code
    
    def decode(self,s):
        """Given a bitqueue containing only an encoded string, and a stop symbol
        decode the string up to and including the stop symbol and return it."""
        symbol = ""
        output = ""
        location = Fraction(s.intValue(),2**len(s))
        while 0<=location<1:
            #bisect finds the symbol in logarithmic time
            symbol = self._words[bisect.bisect(self._breakpoints,self._upper*location)-1]
            
            if symbol==-1: break
            bounds = self._encodemap[symbol]
            output+=symbol
            #correct location to remove effect of removed symbol
            range = Fraction(bounds[1]-bounds[0],self._upper)
            location = (location-Fraction(bounds[0],self._upper))/range
        if symbol!=-1: raise BufferError("No stop symbol found! Corrupt string!")
        return output
if __name__=="__main__":
    import gzip
    import cStringIO
    from collections import defaultdict as ddict
    import json
    import sys
    import modelbuilder
    teststring = u"Hello is it tea youre looking for"
    sys.stdout.write("Loading and compiling english model...");sys.stdout.flush()
    with gzip.open('engmodel1.json.gz', 'rb') as f:
        countdict = ddict(int,json.loads(f.read()))
    model,words,breakpoints = modelbuilder.build_model(countdict)
    print "done."
    sys.stdout.write("Creating arithmetic coder based on model...");sys.stdout.flush()
    ac = ArithmeticCodec(model,words,breakpoints)
    print "done."
    sys.stdout.write("Encoding test string '%s'..."%teststring);sys.stdout.flush()
    bq = ac.encode(teststring)
    print "done:"
    print bq.byteString()
    sys.stdout.write("Decoding test bit sequence...");sys.stdout.flush()
    output = ac.decode(bq)
    print "done:"
    print output
    