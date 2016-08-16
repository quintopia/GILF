import Queue
class BitQueue(object):
    """A queue which can pop data one bit or byte at a time and push data as strings of bits or bytes.
    Not thread-safe.
    
    Usage:
    >>> bq = BitQueue()
    >>> bq.pushBits("01")
    >>> len(bq)
    2
    >>> bq.nextBit()
    0
    >>> bq.nextBit()
    1
    >>> bq.pushBytes("abc")
    >>> len(bq)
    24
    >>> bq.nextByte()
    "a"
    """
    
    def __init__(self,data=""):
        self.data = data
        self.currentbyte = None
        self.bitposition = 7
        self.currentinputbyte = ""
        
    def pushNum(self, s,l,push=1):
        """Produce a binary string from a number. Ensure it has the specified length. Push it. Return string of pushed bits."""
        s=str(s) if s<=1 and l<=1 else self.pushNum(s>>1,l-1,0) + str(s&1)
        if push: self.pushBits(s)
        return s
    
    def nextBit(self):
        """Get next bit."""
        if not len(self.data) and self.currentbyte is None:
            if self.currentinputbyte:
                output = int(self.currentinputbyte[0])
                self.currentinputbyte = self.currentinputbyte[1:]
                return output
            else:
                raise Queue.Empty()
        if self.currentbyte is None:
            self.currentbyte = self.data[0]
            self.data = self.data[1:]
        bitmask = 1 << self.bitposition
        bit = ord(self.currentbyte) & bitmask
        bit >>= self.bitposition
        self.bitposition-=1
        if self.bitposition < 0:
            self.bitposition = 7
            self.currentbyte = None
        return bit
    
    def pushBit(self, bit):
        """push a single bit!"""
        self.pushBits(str(bit))
    
    def pushBits(self, bits):
        """bits is a string of 1 and 0 characters"""
        cut = 8 - len(self.currentinputbyte)
        self.currentinputbyte += bits[:cut]
        bits = bits[cut:]
        while len(self.currentinputbyte) == 8:
            byte = int(self.currentinputbyte,2)
            self.data += chr(byte)
            self.currentinputbyte = bits[0:8]
            bits = bits[8:]
    
    def nextByte(self):
        """Get next 8 bits as a byte, tail-padded with zeroes if queue has fewer than 8 bits"""
        # We could just call nextBit() 8 times and glue them all together, but this is faster
        if not len(self.data) and self.currentbyte is None:
            if self.currentinputbyte:
                output = chr(int(self.currentinputbyte + "0"*(8-len(self.currentinputbyte)),2))
                self.currentinputbyte = ""
            else:
                raise Queue.Empty()
        bitmask = (2 << self.bitposition) - 1
        bits = ord(self.currentbyte) & bitmask
        bits <<= 7 - self.bitposition
        if self.bitposition < 7:
            if self.data:
                self.currentbyte = self.data[0]
                self.data = self.data[1:]
                bitmask = ( (2 << (7 - self.bitposition) ) - 1) << (self.bitposition + 1)
                bits2 = ord(self.currentbyte) & bitmask
                bits |= bits2 >> (self.bitposition+1)
            elif self.currentinputbyte:
                self.currentinputbyte += "0"*(7 - self.bitposition - len(self.currentinputbyte))
                bits2 = int(self.currentinputbyte[:7 - self.bitposition],2)
                bits |= bits2
                self.currentinputbyte = self.currentinputbyte[7-self.bitposition:]
                self.bitposition = 7
                self.currentbyte = None
            else:
                self.bitposition = 7
                self.currentbyte = None
            
        return chr(bits)
        
    def hasBit(self):
        """return true iff the queue contains at least one bit"""
        return len(self.data) or self.currentbyte is not None or self.currentinputbyte
        
    def pushBytes(self, bytes):
        """bytes is a normal string"""
        for c in bytes:
            bits = bin(ord(c))[2:]
            byte = "0" * (8-len(bits)) + bits
            self.pushBits(byte)
    
    def __len__(self):
        return (self.bitposition if self.currentbyte is not None else -1) + 1 + 8 * len(self.data) + len(self.currentinputbyte)
    

if __name__=="__main__":
    bbq = BitQueue("test")
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    bbq.pushBits("011")
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    try:
        bbq.nextBit()
        assert False
    except Queue.Empty:
        assert len(bbq)==0
    bbq.pushBytes("qu")
    assert len(bbq)==16
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert len(bbq)==10
    assert bbq.nextByte()==']'
    assert len(bbq)==2
    assert bbq.nextByte()=='@'
    bbq.pushNum(99,10)
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.nextBit()==1
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==0
    assert bbq.nextBit()==1
    assert bbq.hasBit()
    assert bbq.nextBit()==1
    assert not bbq.hasBit()
    try:
        bbq.nextBit()
        assert False
    except Queue.Empty:
        print "Success!"