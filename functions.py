def memoize(f):
    """ Memoization decorator for functions taking one or more arguments. """
    class memodict(dict):
        def __init__(self, f):
            self.f = f
        def __call__(self, *args):
            return self[args]
        def __missing__(self, key):
            ret = self[key] = self.f(*key)
            return ret
    return memodict(f)

class NullaryFunction(object):
""" Nullary functions just return some bit of data either gleaned from program source or constant.
    For instance, string literals, character literals, numeric literals, list literals, mathematical constants....
    Since they do not depend on input, we can go ahead and evaluate them while parsing the program, and just return
    the data without evaluation when the program is actually run."""
    def __init__(self, codeword, name, data):
        self.data = data
        self.hasParent = hasParent
        self.codeword = codeword
    
    def __call__(self):
        return self.data
    
    def __len__(self):
    """ Number of arguments in all children of a node """
        return 0
        
class UnaryFunction(object):
""" Unary functions take one input. Memoizing."""
    def __init__(self, codeword, function, argument):
    """ argument is not a value. it is a reference to another callable.
        As you would expect from a functional language.... """
        self.function = memoize(function)
        self.argument = argument
        self.codeword = codeword
        self.length = len(argument)+1
    
    def __call__(self):
        return self.function(self.argument())
    
    def __len__(self):
        return self.length

class BinaryFunction(object):
""" Binary functions take two inputs. Memoizing."""
    def __init__(self, codeword, function, left_argument, right_argument):
        self.function = memoize(function)
        self.left_argument = left_argument
        self.right_argument = right_argument
        self.codeword = codeword
        self.length = len(left_argument) + len(right_argument) + 2
        
    def __call__(self):
        return self.function(self.left_argument(),self.right_argument())
    
    def __len__(self):
        return self.length