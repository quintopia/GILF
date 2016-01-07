import Queue

class BitQueue(object):
    """A read-only queue which returns string (byte array) data one bit at a time.
    
    Usage:
    >>> bq = BitQueue(data)
    >>> bq.next()
    1
    >>> bq.next()
    0"""
    
    def __init__(self,data):
        self.data = data
        self.position = 0
        self.bitposition = 0
    
    def next(self):
        """Get next bit."""
        if self.position == len(self.data):
            raise Queue.Empty()
        character = self.data[self.position]
        bitmask = 1<<(7-self.bitposition)
        bit = ord(character)&bitmask
        bit >>= 7-self.bitposition
        self.bitposition+=1
        if self.bitposition == 8:
            self.bitposition = 0
            self.position += 1
        return bit

if __name__=="__main__":
    bbq = BitQueue("test")
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==0
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==1
    assert bbq.next()==0
    assert bbq.next()==0
    try:
        bbq.next()
        assert False
    except Queue.Empty:
        print "Success!"