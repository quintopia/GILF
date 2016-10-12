from repoze.lru import CacheMaker
import literalcoder
import bitqueue

class NullaryFunction(object):
""" Nullary functions just return some bit of data either gleaned from program source or constant.
    For instance, string literals, character literals, numeric literals, list literals, mathematical constants....
    Since they do not depend on input, we can go ahead and evaluate them while parsing the program, and just return
    the data without evaluation when the program is actually run."""
    def __init__(self, codename, data):
        self.data = data
        self.hasParent = hasParent
    
    def set_value(self,value):
        self.data = value
    
    def __call__(self):
        return self.data
    
    def __len__(self):
    """ Number of arguments in all children of a node """
        return 0
    
    def encoding(self,hufftree,groupmap,ast_list,bq=None):
        if bq is None: bq=bitqueue.BitQueue()
        h.encode(self.codename,bq)
        return literalcoder.encode(self.data,bq)
        
class UnaryFunction(object):
""" Unary functions take one input. Memoizing."""
    def __init__(self, codename, function, argument):
    """ argument is not a value. it is a reference to another callable.
        As you would expect from a functional language.... """
        self.cache_maker = CacheMaker()
        self.codename = codename
        self.function = cache_maker.expiring_lrucache(maxsize=30000,timeout=30)(function)
        self.argument = argument
        self.length = len(argument)+1
    
    def __call__(self):
        return self.function(self.argument())
    
    def __len__(self):
        return self.length
    
    def encoding(self,hufftree,groupmap,ast_list,bq=None):
        if bq is None: bq = bitqueue.BitQueue()
        hufftree.encode(groupmap[self.codename],bq)
        mypos = ast_list.index(self)
        argpos = ast_list.index(self.argument)
        return encode_argument(argpos-mypos,bq)

class BinaryFunction(object):
""" Binary functions take two inputs. Memoizing."""
    def __init__(self, codename, function, left_argument, right_argument):
        self.cache_maker = CacheMaker()
        self.codename = codename
        self.function = cache_maker.expiring_lrucache(maxsize=30000,timeout=30)(function)
        self.left_argument = left_argument
        self.right_argument = right_argument
        self.length = len(left_argument) + len(right_argument) + 2
        
    def __call__(self):
        return self.function(self.left_argument(),self.right_argument())
    
    def __len__(self):
        return self.length
    
    def encoding(self,hufftree,groupmap,ast_list,bq=None):
        if bq is None: bq = bitqueue.BitQueue()
        hufftree.encode(groupmap[self.codename],bq)
        mypos = ast_list.index(self)
        relpos1 = ast_list.index(left_argument) - mypos
        relpos2 = ast_list.index(right_argument) - mypos
        return encode_arguments(relpos1,relpos2,bq)