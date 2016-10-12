# -*- coding: utf-8 -*-
import bisect
import bitqueue
import math
import re
import operator
import dawg
from successordict import SuccessorDict as sdict
from repoze.lru import lru_cache

class ArithmeticCodec:
    # Thanks to nayuki and contributors at Github for making it clearer how the binary approximation works, and a few lines of code here and there
    def get_bounds(self,w):
        """Find the lower and upper bounds of the word in the dictionary"""
        ub = self._encodemap[w]
        try:
            lb = self._encodemap[self._encodemap.prev_key(w)]
        except ValueError:
            lb = 0
        return lb,ub
        
    @lru_cache(30000)
    def tokenize(self, word):
        """Find all possible ways to tokenize the word, and return the highest scoring"""
        prefices = self._tokens.prefixes(word)
        best_score = 0
        for prefix in prefices:
            lb,ub = self.get_bounds(prefix)
            prefix_score = (ub-lb)/float(self._upper)
            suffix = word[len(prefix):]
            if suffix:
                suffixsplit,splitscore = self.tokenize(suffix)
            else:
                suffixsplit,splitscore = [],1
            if prefix_score*splitscore > best_score:
                best_split = [prefix]+suffixsplit
                best_score = prefix_score*splitscore
        return best_split,best_score
        
    def split_first_token(self,s):
        """Find the optimal token at the beginning of the string and split the string on it"""
        # thanks to Mikhail Korobov and contributors for DAWG. much easier to make this project faster with it.
        word = ""
        #all words in model are short, so no need to optimize over more than the first 50 chars (even this is overkill)
        if not s:
            return "",""
        cut = self._split_re.split(s[:50],1)
        if len(cut)>=3 and s.isupper():
            return u"WHOLESTRINGCAPS",s.lower()
        cut = cut[0] if cut[0] else cut[1]
        word,score=self.tokenize(cut)
        word = word[0]
        if len(cut)>1 and len(word)==1 and word[0].isupper() and cut[0].lower()+cut[1:] in filter(lambda x: isinstance(x,unicode),self._encodemap.keys()):
            return u"CAPITALIZED",word.lower()+s[1:] #capitalized word not capitalized in dict -> capitalization token and lowercased word in string
        if len(word)==1 and len(cut)>1 and cut.isupper():
            lb,ub = self.get_bounds("ALLCAPS")
            word2,score2 = self.tokenize(cut.lower())
            altscore = (ub-lb)/float(self._upper)*score2

            if len(word2[0])>1 and altscore > score:
                return u"ALLCAPS",s[:len(word2[0])].lower()+s[len(word2[0]):] #all caps word -> all caps token and lowercased word in string
        #we return the first token of the split, but thanks to the magic of memoization, if there was more than one token in it, we've got the rest "buffered"
        return word,s[len(word):]
    
    def __init__(self,model):
        """
        words is a list of words sorted in the same order as the corresponding breakpoints in breakpoints
        """
        
        self._encodemap = model
        oldval=0
        
        self._tokens = dawg.CompletionDAWG(model.keys()[:-1])
        self._upper = model[model.last_key()]
        self._size = self._upper.bit_length()+2
        self._split_re = re.compile("([^a-zA-Z0-9'])")
    
    def encode(self,string,code=None):
        """Given a string and a bitqueue, arithmetically encode the string and push the result directly into the queue and return it
        If no bitqueue is provided, return a fresh one containing only the encoded string."""
        if code is None: code = bitqueue.BitQueue()
        MASK = (1<<self._size+1)-1
        TOP_MASK = 1<<self._size
        lower = 0
        upper = MASK
        underflow = 0
        # loop through symbols and do arithmetic coding
        total = len(string)
        w,string = self.split_first_token(string)
        while w:
            lb,ub = self.get_bounds(w)
            rrange = upper-lower+1
            upper = lower + (rrange * ub // self._upper)-1
            lower = lower + (rrange * lb // self._upper)
            # push out a bit to simplify fractions whenever possible (for speed and memory)
            # renormalize and pull in more bits if necessary
 
            while not ((upper ^ lower) & TOP_MASK):
                #print "{0:041b}".format(lower),"{0:041b}".format(upper)
                if upper == 1: sys.exit(1)
                bit = lower >> self._size
                code.pushBits(str(bit)+str(bit^1)*underflow)
                # these do the equivalent of 2*bound or 2*bound-1 (depending on top half or bottom half of range)
                lower = lower<<1 & MASK
                upper = upper<<1 & MASK | 1
                underflow = 0
            while lower & ~upper & TOP_MASK>>1:
                #print "{0:041b}".format(lower),"{0:041b}".format(upper)
                underflow+=1
                # these are the equivalent of 2*bound - 1/2
                lower = lower<<1 & MASK>>1
                upper = upper<<1 & MASK>>1 | TOP_MASK | 1
            w,string = self.split_first_token(string)
            #progressbar.printProgress(total-len(string),total)
            #print "{0:041b}".format(lower),"{0:041b}".format(upper)
            #print "next!"
        #now push a stop symbol
        ub = self._encodemap[-1]
        try:
            lb = self._encodemap[self._encodemap.prev_key(-1)]
        except ValueError:
            lb = 0
        rrange = upper-lower+1
        upper = lower + (rrange * ub // self._upper)-1
        lower = lower + (rrange * lb // self._upper)
        
        #now pull out bits until this range is unambiguous (includes 0)
        while not ((upper ^ lower) & TOP_MASK):
            #print "{0:041b}".format(lower),"{0:041b}".format(upper)
            bit = lower >> self._size
            #print str(bit)+str(bit^1)*underflow
            code.pushBits(str(bit)+str(bit^1)*underflow)
            # these do the equivalent of 2*bound or 2*bound-1 (depending on top half or bottom half of range)
            lower = lower<<1 & MASK
            upper = upper<<1 & MASK | 1
            underflow = 0
        while lower & ~upper & TOP_MASK>>1:
            #print "{0:041b}".format(lower),"{0:041b}".format(upper)
            underflow+=1
            # these are the equivalent of 2*bound - 1/2
            lower = lower<<1 & MASK>>1
            upper = upper<<1 & MASK>>1 | TOP_MASK | 1
        
        #flush the last bits
        underflow+=1
        bit = (lower & TOP_MASK>>1)>>self._size-1
        code.pushBits(str(bit)+str(bit^1)*underflow)
                
        return code
    
    def decode(self,bq):
        """Given a bitqueue containing only an encoded string, and a stop symbol
        decode the string up to and including the stop symbol and return it."""
        words = self._encodemap.keys() # its time-expensive to make these lists so we best only do so once
        boundaries = self._encodemap.values()
        symbol = ""
        output = ""
        MASK = (1<<self._size+1)-1
        TOP_MASK = 1<<self._size
        lower = 0
        upper = MASK
        location = bq.popBits(self._size+1)
        #print self._size
        #print "{0:0b}".format(MASK)
        #print "{0:0b}".format(TOP_MASK)
        #print ("{0:0%db}"%(self._size+1)).format(location)
        extrazeroes=0
        capitalizenext=0
        allcapsnext=0
        nothinbutcaps=0
        while symbol!=-1 and (bq.hasBit() or location):
            #scale location from code range to frequency table range
            #print lower,upper
            rrange = upper - lower + 1
            offset = location - lower
            value = ((offset + 1)*self._upper - 1) // rrange
            
            #import pdb;pdb.set_trace()
            #bisect finds the symbol in logarithmic time
            ind = bisect.bisect(boundaries,value)
            try: symbol = words[ind]
            except IndexError: pass
            #print value,ind,symbol
            ub = self._encodemap[symbol]
            try: 
                lb = self._encodemap[self._encodemap.prev_key(symbol)]
            except ValueError:
                lb = 0
            assert lb<=value<ub
            #print lb,ub
            #import pdb;pdb.set_trace()
            if symbol==u"CAPITALIZED": capitalizenext=1
            elif symbol==u"ALLCAPS": allcapsnext=1
            elif symbol==u"WHOLESTRINGCAPS": nothinbutcaps=1
            elif symbol!=-1: 
                if capitalizenext:
                    output+=symbol.capitalize()
                    capitalizenext=0
                elif allcapsnext or nothinbutcaps:
                    output+=symbol.upper()
                    allcapsnext=0
                else: output+=symbol
            
            #update bounds to remove effect of removed symbol
            upper = lower + (rrange * ub // self._upper)-1
            lower = lower + (rrange * lb // self._upper)
                        
            # renormalize and pull in more bits if necessary
            while not ((upper ^ lower) & TOP_MASK):
                lower = lower<<1 & MASK
                upper = upper<<1 & MASK | 1
                location = location<<1 & MASK 
                if bq.hasBit(): location |= bq.nextBit()
                else: extrazeroes+=1
            while lower & ~upper & TOP_MASK>>1:
                lower = lower<<1 & MASK>>1
                upper = upper<<1 & MASK>>1 | TOP_MASK | 1
                location = location & TOP_MASK | location<<1 & MASK>>1 
                if bq.hasBit(): location |= bq.nextBit()
                else: extrazeroes+=1
          
        #import pdb;pdb.set_trace()
        if symbol!=-1: raise BufferError("No stop symbol found! Corrupt string!")
        
        #Now put back all the bits we didn't need!
        location &= MASK>>2
        location >>= extrazeroes
        bits = ("{0:0%db}"%(self._size - 2 - extrazeroes)).format(location)
        bq.pushBitsToFront(bits)
        return output

if __name__=="__main__":
    import gzip
    from successordict import SuccessorDict as sdict
    import json
    import sys
    import modelbuilder
    import time
    
    #teststring = u"I have no idea how long this shit will take. I better not make it too long, or I'll never get the data I need."
    teststring = u"""You're a girl who's great at science,
Always experimenting.
You're a girl who looks amazing in lab coats,
Always peering down microscopes.
You're a girl who's great at lying,
Always running rings around the teachers.
You're a girl who loves solitude,
Always gazing up at the sky alone.
I may have only got five points on the last mock test but even I know
That girl's probably a polarised smuttiness filter.

My alcohol lamp is burning up,
Being separated out by a micropipette.
My evaporator is flying high,
Grasped with a Faraday cup.
Your gas detector's getting wet,
Melting from the heating mantle.
Your mortar's spinning more and more,
With the vacuum pump pouring into it.
But even so, the science girl stays straight-faced.

You're the one I love the most in the world!
Of course I can't say something that shifty!
If I tried to tell you with elemental symbols
Everyone would just make fun of me.
Please tell me your phone number!
But I don't have the courage or the guts to say that.
Please experiment on me!
In that case, strip down right now, okay?
Don't look so appalled -
If you're going to get naked so shyly,
Jump off Toujinbou cliff
Immediately!

"Idiots should definitely catch colds"
Did anyone even decide that?
Inviting in the freezing gusts of wind,
My nose won't stop running.
Even if you call me a guinea pig,
Even if I turn into a research sample,
Even if a typhoon sweeps over here,
I'll still go to meet you with an umbrella,
But even so, the science girl won't look back.

The only flower in the world
Lives alone, alone as a different species from everyone else.
Thus, it's wonderful even if it only manages to bloom
With all everything it's got.
And because somebody said that,
I'll sow seeds for you
Because, if only so that that flower can bloom,
Let's give everything we've got.
Shackling you and locking you into a collar,
Binding you with rope,
If I blindfold you,
Turn around thrice and bark like a dog!

My alcohol lamp is burning up,
Being separated out by a micropipette.
My evaporator is flying high,
Grasped with a Faraday cup.
I keep suffering from these normal feelings;
We spun around the globe together.
It's not really something that can be put into words -
It was tied up in the euphoria of your mystery.

Unwinding, getting wet from liquid nitrogen -
Solve that emotion, would you?
If you can't sum it up in words,
Show me the proof of those through processes, would you?
And so the gas detector's getting wet,
Melting from the heating mantle.
And the mortar's spinning more and more,
Because the vacuum pump poured into it.

And only then did the science girl laugh."""
    """teststring = u"\""We're no strangers to love
You know the rules and so do I
A full commitment's what I'm thinking of
You wouldn't get this from any other guy

I just want to tell you how I'm feeling
Gotta make you understand

Never gonna give you up, never gonna let you down
Never gonna run around and desert you
Never gonna make you cry, never gonna say goodbye
Never gonna tell a lie and hurt you

We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it

And if you ask me how I'm feeling
Don't tell me you're too blind to see

Never gonna give you up, never gonna let you down
Never gonna run around and desert you
Never gonna make you cry, never gonna say goodbye
Never gonna tell a lie and hurt you

Never gonna give you up, never gonna let you down
Never gonna run around and desert you
Never gonna make you cry, never gonna say goodbye
Never gonna tell a lie and hurt you

We've known each other for so long
Your heart's been aching but you're too shy to say it
Inside we both know what's been going on
We know the game and we're gonna play it

I just want to tell you how I'm feeling
Gotta make you understand

Never gonna give you up, never gonna let you down
Never gonna run around and desert you
Never gonna make you cry, never gonna say goodbye
Never gonna tell a lie and hurt you"""
    teststring = u"THIS IS A TEST OF ALL CAPS COMPRESSION."
    sys.stdout.write("Loading and compiling english model...");sys.stdout.flush()
    starttime = time.time()
    with gzip.open('engmodel6.json.gz', 'rb') as f:
        countdict = json.load(f,object_pairs_hook=sdict)
    #with gzip.open('engmodel2.json.gz','rb') as f:
    #    teststring = " ".join(json.load(f).keys()[:10000])
    with open("symbols.json") as f:
        symbols = json.load(f)
    fullmodel = modelbuilder.build_model(countdict,symbols)
    print "done: %d seconds"%(time.time()-starttime)
    sys.stdout.write("Creating arithmetic coder based on model...");sys.stdout.flush()
    ac = ArithmeticCodec(fullmodel)
    print "done."
    sys.stdout.write("Encoding test string...");sys.stdout.flush()
    starttime = time.time()
    bq = ac.encode(teststring)
    print "done: %d seconds, length: %d"%(time.time()-starttime, len(bq))
    bq.pushBits("110100100010000")
    #print bq.byteString()
    #print bq.bitString()
    sys.stdout.write("Decoding test bit sequence...");sys.stdout.flush()
    starttime = time.time()
    output = ac.decode(bq)
    print "done: %d seconds"%(time.time()-starttime)
    assert output==teststring
    assert bq.bitString()=="110100100010000"