# This is the hardest part of the whole thing (is it? that arithmetic codec was pretty hard, and the UI will be too)...
import huffmantree
import json
import pulp
from collections import defaultdict as ddict

with open('command_counts.json','r') as f:
    comcounts = json.load(f)
    
def encode(prog_ast,encoding,bq=None):
""" Create an optimized binary encoding of the input program in a BitQueue. """
    if bq is None: bq=bitqueue.BitQueue()
    
    code_table = ddict(int)
    
    #comcounts is an encoding dictionary of a list of function dictionaries.
    enccounts0,enccounts1,enccounts2 = comcounts[encoding]

    #then, group up functions based on rank within arity and across signatures of the same arity, and create a mapping from the "group name" to their combined counts, and likewise from a signature to its groupname. from this combined list, make a new huffman tree.
    
    #handle nullary functions first (they go straight in the table because they take no arguments and are already in the right format)
    code_table.update(enccounts0)
    
    #now unary functions
    #enccounts1 maps argumenttypestr to dictionaries which map function names to counts.
    unarygroupmap = ddict(int)
    for astr,funcmap in enccounts1.items():
        for i,func in enumerate(sorted(list(funcmap),key=lambda x: funcmap[x])):
            code_table["unarygroup"+str(i)]+=funcmap[func]
            unarygroupmap[func].append(i)
    
    #now binary functions
    binarygroupmap = ddict(int)
    for astr,funcmap in enccounts2.items():
        for i,func in enumerate(sorted(list(funcmap),key=lambda x: funcmap[x])):
            code_table["binarygroup"+str(i)]+=funcmap[func]
            unarygroupmap[func].append(i)
    
    h = HuffmanTree(code_table)
            
    #now that we have the huffman tree built, we need to find the ideal positions of everything in the output program
    