

class HuffmanTree(object):

    class node(object):
     
        def __init__(self, word, value, left=None, right=None):
            self.children = [left,right]
            self.word = word
            self.value = value
            self.parent = None
            self.childnum = None
    
    def build_tree(self, word_list):
        if len(word_list)==1:
            return word_list
        
        word_list.sort(key=lambda x:x.value)
        
        new_node = HuffmanTree.node(None,word_list[0].value+word_list[1].value,word_list[0],word_list[1])
        word_list[0].parent = new_node
        word_list[0].childnum = 0
        word_list[1].parent = new_node
        word_list[1].childnum = 1
        del word_list[0],word_list[0]
        word_list.append(new_node)
        return self.build_tree(word_list)
        
    def encode(self,word):
        word_node = self.encoding_dict[word]
        return self.build_symbol(word_node)
    
    def build_symbol(self,word_node):
        if word_node == self.root:
            return []
        output_list = self.build_symbol(word_node.parent)
        output_list.append(word_node.childnum)
        return output_list
    
    def decode(self, bit):
        """decode(bit) consumes bits one at a time, traversing the huffman tree.
        If it has not found a codeword yet, it returns None.
        As soon as it finds a code word, it returns it and resets to begin traversing for another word."""
        self.curloc = self.curloc.children[bit]
        output = self.curloc.word
        if output is not None:
            self.curloc = self.root
        return output
    
    def reset_decode(self):
        """Call reset_decode() to reset the tree traversal when decoding,
        for instance to abort an in-progress symbol decode."""
        self.curloc = self.root
        
    def __init__(self,word_table):
        word_list=list()
        self.encoding_dict=dict()
        for k,v in word_table.iteritems():
            new_node = HuffmanTree.node(k,v)
            word_list.append(new_node)
            self.encoding_dict[k]=new_node
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
    assert h.encode("q") == [0]
    assert h.encode("u") == [1,0]
    assert h.encode("i") == [1,1,0]
    assert h.encode("n") == [1,1,1,1]
    assert h.encode("t") == [1,1,1,0]
    assert h.decode(0) == "q"
    assert h.decode(1) is None
    assert h.decode(0) == "u"
    assert h.decode(1) is None
    assert h.decode(1) is None
    assert h.decode(0) == "i"
    assert h.decode(1) is None
    assert h.decode(1) is None
    assert h.decode(1) is None
    assert h.decode(1) == "n"
    assert h.decode(1) is None
    assert h.decode(1) is None
    assert h.decode(1) is None
    assert h.decode(0) == "t"
    print "Success!"