import bitqueue

def encode(s,bq=bitqueue.BitQueue()):
    # pack the string into the given bitqueue
    if isinstance(s,unicode):
        raise UnicodeError("Packed strings do not support unicode.")
    chars = map(ord,s)
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
        s += chr(lowest+bits)
        bits = bq.popBits(numbits)
    return s

if __name__=="__main__":
    strings = ["abcdefg","!@#$%^&*(","ABABABABABABABABABABABABABABBBBBBBB","%%%%%%%%%%%%%%%%%%%%%%%%","090909","    zzzz"]
    for teststr in strings:
        bq = encode(teststr)
        print len(bq),len(teststr)*8+8
        outstr = decode(bq)
        assert outstr==teststr