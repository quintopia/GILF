import bitqueue
import math

def encode(n,bq=bitqueue.BitQueue()):
    if -8<=n<=7: #4 bit tiny number
        if n<0: n+=16
        bq.pushBits("0"+"{:04b}".format(n))
    elif -128<=n<=127: #8 bit byte number
        if n<0: n+=256
        bq.pushBits("10"+"{:08b}".format(n))
    else: #everything bigger, chunked into 16 bit blocks
        bq.pushBits("11")
        bq.pushBits("1" if n<0 else "0")
        n = abs(n)
        numblocks = math.ceil(n.bit_length()/16.)
        bytelist = str(bytearray.fromhex(('{:0%dx}'%(4*numblocks)).format(n)))
        while len(bytelist)>2:
            bq.pushBits("1")
            bq.pushBytes(bytelist[:2])
            bytelist = bytelist[2:]
        bq.pushBits("0")
        bq.pushBytes(bytelist)
    return bq

def decode(bq):
    if bq.nextBit():
        if bq.nextBit():
            sign = bq.nextBit()
            s=""
            while bq.nextBit():
                s+=bq.popBytes(2)
            s+=bq.popBytes(2)
            n = int(s.encode('hex'),16)
            if sign: n*=-1
        else: # 8 bit byte number
            n = bq.popBits(8)
            if n > 127: n-=256
    else: # 4 bit tiny number
        n = bq.popBits(4)
        if n>7: n-=16
    return n

if __name__=="__main__":
    n = -40
    bq = encode(n)
    p = decode(bq)
    assert p == n