import bitqueue
import Queue

class HuffmanTree(object):

    class node(object):
     
        def __init__(self, word, value, left=None, right=None):
            self.children = [left,right]
            self.word = word
            self.value = value
            self.parent = None
            self.childnum = None
    
    def build_tree(self, word_list):
        if len(word_list) == 1:
            return word_list
        
        word_list.sort(key=lambda x:x.value)
        
        new_node = HuffmanTree.node(None, word_list[0].value + word_list[1].value, word_list[0], word_list[1])
        word_list[0].parent = new_node
        word_list[0].childnum = 0
        word_list[1].parent = new_node
        word_list[1].childnum = 1
        del word_list[0], word_list[0]
        word_list.append(new_node)
        return self.build_tree(word_list)
        
    def encode(self,word,bq=None):
        if bq is None: bq=bitqueue.BitQueue()
        word_node = self.encoding_dict[word]
        return self.build_symbol(word_node,bq)
    
    def build_symbol(self,word_node,bq):
        if word_node == self.root:
            return bq
        bq = self.build_symbol(word_node.parent,bq)
        bq.pushBit(word_node.childnum)
        return bq
    
    def decode(self, bq):
        """decode(bit) consumes exactly as many bits from the queue as needed to find a codeword"""
        curloc = self.root
        while curloc.word is None:
            try:
                bit = bq.nextBit()
            except Queue.Empty:
                raise ValueError("No codeword found in queue")
            curloc = curloc.children[bit]
        return curloc.word
    
    def reset_decode(self):
        """Call reset_decode() to reset the tree traversal when decoding,
        for instance to abort an in-progress symbol decode."""
        self.curloc = self.root
        
    def __init__(self,word_table):
        word_list = list()
        self.encoding_dict = dict()
        for k,v in word_table.iteritems():
            new_node = HuffmanTree.node(k,v)
            word_list.append(new_node)
            self.encoding_dict[k] = new_node
        self.root = self.build_tree(word_list)[0]
        self.curloc = self.root
        
if __name__=="__main__":
    counts = {"q":.5,"u":.25,"i":.125,"n":.0625,"t":.0625}
    h = HuffmanTree(counts)
    assert h.root.children[0].word == "q"
    assert h.root.children[1].children[0].word == "u"
    assert h.root.children[1].children[1].children[0].word == "i"
    assert h.root.children[1].children[1].children[1].children[1].word == "n"
    assert h.root.children[1].children[1].children[1].children[0].word == "t"
    q = h.encode("q")
    assert q.bitString() == "0"
    u = h.encode("u")
    assert u.bitString() == "10"
    i = h.encode("i")
    assert i.bitString() == "110"
    n = h.encode("n")
    assert n.bitString() == "1111"
    t = h.encode("t")
    assert t.bitString() == "1110"
    assert h.decode(q) == "q"
    assert h.decode(u) == "u"
    assert h.decode(i) == "i"
    assert h.decode(n) == "n"
    assert h.decode(t) == "t"
    print "Success!"