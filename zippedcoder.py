# -*- coding: utf-8 -*-
import bitqueue
import bz2

def encode(s,bq=None):
    if bq is None: bq=bitqueue.BitQueue()
    bq.pushBytes(bz2.compress(s.encode('utf8')))
    return bq
    
def decode(bq):
    s = bz2.decompress(bq.byteString())
    bq.popBits(len(bz2.compress(s))*8)
    return s
    
if __name__=="__main__":
    teststring = u"Here's a pretty pretty pretty random string. Ṱ͕̮̯͢o̵ ̸̬ì̯̗͉n͖̤v̝̰̜̹̟o̭̜̬͈k҉̜̲̥̟̞ę͙̯̗̣̣̠ͅ ͎̬̫̜͎t͜h̺̝̙͖͙̦ͅḛ͙͜ ̛͉̺͖̱̩̲h̶̰̗̻͔̤ḭ̞͚͔̜̝̖͟v̪͕̜̟͜e-̷m͇̪̲̰̟̰̲͡in̩̤̫͇͕d̵ ̱r̗̼̟͉͞e̞͓p̫͚͖̦̝͔̲r͉̭̩̤͓e̺̝̘̟̝͇͢s̭̱̝͢e̲̼͈̩n҉̦͈͇̖̖t̻i͜n̮̮̩ͅg̤͢ ̺̖̻̘̪͕͜c͈̣͕̬̜ͅh̨a̴̠̞̠͈̞̰̟ọ̯͍s.̙̝̥ͅͅ"
    bq = encode(teststring)
    bq.pushBytes("garbagedata")
    assert decode(bq)==teststring.encode('utf8')
    assert bq.byteString()=="garbagedata"