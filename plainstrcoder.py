# -*- coding: utf-8 -*-
import bitqueue

def encode(s,bq=None):
    if bq is None: bq = bitqueue.BitQueue()
    if "\x00" in s:
        raise ValueError("String contains a null byte.")
    bq.pushBytes(s.encode('utf8')+"\x00")
    return bq

def decode(bq):
    s = ""
    for byte in bq.byte_iterator():
        if ord(byte):
            s+=byte
        else:
            break
    return s

if __name__=="__main__":
    teststring = u"Ṱ͕̮̯͢o̵ ̸̬ì̯̗͉n͖̤v̝̰̜̹̟o̭̜̬͈k҉̜̲̥̟̞ę͙̯̗̣̣̠ͅ ͎̬̫̜͎t͜h̺̝̙͖͙̦ͅḛ͙͜ ̛͉̺͖̱̩̲h̶̰̗̻͔̤ḭ̞͚͔̜̝̖͟v̪͕̜̟͜e-̷m͇̪̲̰̟̰̲͡in̩̤̫͇͕d̵ ̱r̗̼̟͉͞e̞͓p̫͚͖̦̝͔̲r͉̭̩̤͓e̺̝̘̟̝͇͢s̭̱̝͢e̲̼͈̩n҉̦͈͇̖̖t̻i͜n̮̮̩ͅg̤͢ ̺̖̻̘̪͕͜c͈̣͕̬̜ͅh̨a̴̠̞̠͈̞̰̟ọ̯͍s.̙̝̥ͅͅ"
    bq = encode(teststring)
    s = decode(bq)
    assert teststring.encode('utf8')==s
    assert len(bq)==0