from collections import OrderedDict

#to save memory storing the english model, we add methods to OrderedDict to find adjacent items in constant time.
class SuccessorDict(OrderedDict):
    def next_key(self, key):
        next = self._OrderedDict__map[key][1]
        if next is self._OrderedDict__root:
            raise ValueError("{!r} is the last key".format(key))
        return next[2]
    def prev_key(self, key):
        prev = self._OrderedDict__map[key][0]
        if prev is self._OrderedDict__root:
            raise ValueError("{!r} is the first key".format(key))
    def first_key(self):
        for key in self: return key
        raise ValueError("SuccessorDict is empty.")
    def last_key(self):
        for key in reversed(self): return key
        raise ValueError("SuccessorDict is empty.")
