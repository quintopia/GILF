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
        """Produce a binary string from a number. Ensure it has at least the specified length. Push it. Return string of pushed bits."""
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
            
    def pushBitsToFront(self, bits):
        """For pushing bits to the front of the queue so that popping the same number of bits just pushed to front will return same bits"""
        """bits is a string of 1 and 0 characters"""
        """basically just pop in reverse"""
        if self.currentbyte is not None:
            cbn = ord(self.currentbyte)
            for i in range(self.bitposition+1,8):
                if not bits: return
                cbn ^= (-int(bits[-1:]) ^ cbn) & (1 << i)
                bits = bits[:-1]
            self.data = chr(cbn)+self.data
            self.currentbyte = None
            self.bitposition = 7
        while len(bits)>=8:
            byte = chr(int(bits[-8:],2))
            bits = bits[:-8]
            self.data = byte+self.data
        if bits:
            self.currentbyte = chr(int(bits,2))
            self.bitposition = len(bits)-1
            
                
    
    def nextByte(self):
        """Get next 8 bits as a byte, tail-padded with zeroes if queue has fewer than 8 bits"""
        # We could just call nextBit() 8 times and glue them all together, but this is faster
        if not len(self.data) and self.currentbyte is None:
            if self.currentinputbyte:
                output = chr(int(self.currentinputbyte + "0"*(8-len(self.currentinputbyte)),2))
                self.currentinputbyte = ""
                return output
            else:
                raise Queue.Empty()
        if self.currentbyte is None:
            self.currentbyte = self.data[0]
            self.data = self.data[1:]
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
        else:
            self.currentbyte = None
            self.bitposition = 7
            
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
        
    def bit_iterator(self):
        while self.hasBit():
            yield self.nextBit()
    
    def intValue(self):
        """
        Return value of queue as a single long integer.
        """
        #we could just call nextBit() until queue is empty, but this is faster
        output = 0
        if self.currentbyte is not None:
            output = ord(self.currentbyte) & ((1<<self.bitposition)-1)
        for char in self.data:
            output = output*2**8 + ord(char)
        output = output*2**len(self.currentinputbyte) + int("0"+self.currentinputbyte,2)
        return output
    
    def popBits(self, numBits):
        """
        dequeue the next numBits bits as an int
        """
        if len(self)<numBits:
            raise ValueError("Requested more bits than queue contains.")
        output = 0
        if self.currentbyte is not None:
            output = ord(self.currentbyte) & ((1<<min(self.bitposition,numBits)+1)-1)
            newnumbits = max(0,numBits-self.bitposition-1)
            self.bitposition = max(-1,self.bitposition - numBits)
            numBits = newnumbits
        while numBits > 8 and len(self.data)>0:
            output = output*2**8 + ord(self.data[0])
            self.data = self.data[1:]
            numBits-=8
        if numBits > 0 and len(self.data):
            self.currentbyte = self.data[0]
            self.data = self.data[1:]
            self.bitposition = 7-numBits
            output = 2**numBits*output+(ord(self.currentbyte)>>8-numBits)
            numBits = 0
        while numBits>0:
            output = 2*output+int(self.currentinputbyte[0])
            self.currentinputbyte = self.currentinputbyte[1:]
        if self.bitposition < 0:
            self.bitposition = 7
            if len(self.data)>0:
                self.currentbyte = self.data[0]
                self.data = self.data[1:]
            else:
                self.currentbyte = None
        return output
            
        
    def bitString(self):
        """
        return a string of bits representing the queue contents
        """
        output=""
        if self.currentbyte is not None:
            output += ("{0:0%db}"%(self.bitposition+1)).format(ord(self.currentbyte) & (2**(self.bitposition+1)-1))
        for char in self.data:
            output += "{0:08b}".format(ord(char))
        output += self.currentinputbyte
        return output
    
    def byteString(self):
        """
        return a string representing the queue contents
        """
        #nothing faster than nextByte() is possible here, so we make copies and restore them so this doesn't have side effects
        #good thing all the data is strings...
        bpcopy = self.bitposition
        cbcopy = self.currentbyte
        dacopy = self.data
        cibcopy = self.currentinputbyte
        output = reduce(lambda a,b: a+b,self.byte_iterator())
        self.bitposition = bpcopy
        self.currentbyte = cbcopy
        self.data = dacopy
        self.currentinputbyte = cibcopy
        return output
    
    def byte_iterator(self):
        """
        iterator that consumes the queue and produces bytes
        """
        while self.hasBit():
            yield self.nextByte()
    

if __name__=="__main__":
    import pdb
    bbq = BitQueue("test")
    assert bbq.byteString()=="test"
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
    bbq.pushBitsToFront("10101011010101001010100110001100111010110001111100001010110100101010101101010100101010011000110011101011000111110000101011010010")
    assert len(bbq)==128
    assert bbq.popBits(64)==12345678901234567890
    assert bbq.popBits(64)==12345678901234567890
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
    assert bbq.intValue()==99
    assert bbq.bitString()=="0001100011"
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