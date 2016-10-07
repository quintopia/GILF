import bitqueue
import arithmeticcodec
import plainstrcoder
import packedcoder
import zippedcoder
import numcoder
import gzip
from successordict import SuccessorDict as sdict
import json
import modelbuilder
import struct
import encoder
ac = None

class GILFprogram:
    def __init__(self,rootnode):
        self.root = rootnode
        
    def run(self):
        self.root()
        
def prepare():
    global ac
    with gzip.open('engmodel6.json.gz', 'rb') as f:
        countdict = json.load(f,object_pairs_hook=sdict)
    with open("symbols.json") as f:
        symbols = json.load(f)
    ac = ArithmeticCodec(modelbuilder.build_model(countdict,symbols))

def encode(data, bq=bitqueue.BitQueue()):
    if isinstance(data, str) or isinstance(data, unicode):
        bq.pushBits("0")
        return encode_str(data,bq)
    elif isinstance(data, int) or isinstance(data, long):
        bq.pushBits("10")
        return numcoder.encode(data,bq)
    elif isinstance(data, float):
        bq.pushBits("110")
        bq.pushBytes(struct.pack('!f',data))
        return bq
#    elif type(data) is GILFprogram: 
#        bq.pushBits("111")
#        return encoder.encode(data)
    raise ValueError("Literals of type %s are not supported"%data.__class__.__name__)

def encode_str(s, bq=bitqueue.BitQueue()):
    global ac
    if ac is None:
        prepare()
    try:
        bq1 = packedcoder.encode(s)
        encodetype = "01"
    except:
        pass
    try:
        bq2 = plainstrcoder.encode(s)
    except:
        pass
    if bq1 is None or bq2 is not None and len(bq2)<len(bq1):
        bq1 = bq2
        encodetype = "00"
    bq2 = zippedcoder.encode(s)
    if bq1 is None or len(bq2)<len(bq1):
        bq1 = bq2
        encodetype = "10"
    bq2 = ac.encode(teststring)
    if len(bq2)<len(bq1):
        bq1=bq2
        encodetype = "11"
    bq.pushBits(encodetype)
    bq.append(bq1)
    return bq

def decode(bq):
    if not bq.nextBit():
        return decode_str(bq)
    if not bq.nextBit():
        return numcoder.decode(bq)
    if not bq.nextBit():
        return struct.unpack('!f',bq.popBytes(4))[0]
    return GILFprogram(encoder.decode(bq))

def decode_str(bq):
    global ac
    if ac is None:
        prepare()
    encodetype = bq.popBits(2)
    return [plainstrcoder,packedcoder,zippedcoder,ac][encodetype].decode(bq)