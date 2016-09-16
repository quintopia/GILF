import bitqueue
import string
#i know str.translate could do what i'm doing with this table, but it's less mentally taxing to construct the table by hand
__table = [0,1,2,3,4,5,6,7,8,29,41,9,10,40,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,68,98,96,123,124,
           117,119,95,100,101,114,107,105,106,104,115,39,38,37,36,35,34,33,32,31,30,102,103,108,118,109,97,125,67,
           66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,51,50,49,48,47,46,45,44,43,42,110,116,111,122,99,126,69,70,
           71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,112,120,113,121]
def encode(s,bq=bitqueue.BitQueue()):
    # pack the string into the given bitqueue
    if isinstance(s,unicode):
        raise UnicodeError("Packed strings do not support unicode.")
    chars = map(lambda x:__table[x],map(ord,s))
    lowest = min(chars)-1
    if lowest<0:
        raise ValueError("String contains a null byte.")
    highest = max(chars)
    #need number of bits required per character:
    numbits = (highest-lowest).bit_length()
    if numbits > 7:
        raise OverflowError("Characters in string vary too widely to be packed.")
    bq.pushBytes(chr(lowest)) #first 8 bits are the lower bound character
    bq.pushNum(numbits,3) #next 3 bits tell the number of bits per character
    for char in chars:
        bq.pushNum(char-lowest,numbits) #push numbits bits for the difference of each character with the low char
    bq.pushNum(0,numbits) #push numbits zeroes to mark end of string (all differences on previous line are guaranteed to be >= 1, so this is out-of-band)
    return bq

def decode(bq):
    lowest = ord(bq.nextByte())
    numbits = bq.popBits(3)
    s = ""
    bits = bq.popBits(numbits)
    while bits:
        char = lowest+bits
        if char in __table:
            s += chr(__table.index(char))
        else:
            s += chr(char)
        bits = bq.popBits(numbits)
    return s

if __name__=="__main__":
    strings = ["abcdefg","!@#$%^&*(","ABABABABABABABABABABABABABABBBBBBBB","%%%%%%%%%%%%%%%%%%%%%%%%","090909","    zzzz"]
    for teststr in strings:
        #import pdb;pdb.set_trace()
        bq = encode(teststr)
        print len(bq),len(teststr)*8+8
        outstr = decode(bq)
        assert outstr==teststr
        
"""
35 64
61 80
83 288
36 200
39 56
56 72
"""