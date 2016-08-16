# This is the hardest part of the whole thing...
import huffmantree
import pulp

def encode(prog_ast,encoding,excluded_chars=None):
""" Create an optimized binary encoding of the input program. """
    encodings = ['mathcounts.txt','stringcounts.txt','matrixcounts.txt','interactivecounts.txt','graphcounts.txt','listcounts.txt','drawingcounts.txt','solvecounts.txt']
    enccounts = encodings[encoding]
    code_table = {}
    with open(enccounts,'r') as func_counts:
        for line in func_counts:
            func, count = line.split()
            code_table[func] = int(count)

    h = HuffmanTree(code_table)
            
    