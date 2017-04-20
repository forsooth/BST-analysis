#!/usr/local/bin/python
import argparse
import err
from operations import Operations

parser = argparse.ArgumentParser(description='Generates 2D geometric represen'
                                 + 'tations of BSTs given input op'
                                 + 'erations and a BST variant.')

parser.add_argument('operations', type=str, nargs='+', 
                    help="Paths to files which list the the operations which "
                    + "the BST will perform. Default is standard input.")

parser.add_argument('-o', '--output', type=str, default='-',
                    help="Output location for BST instruction log file."
                         + " Default is standard output.")

parser.add_argument('-a', '--algorithm', type=str, default='simple',
                    help="Algorithm to use in performing the desired"
                         "operations. Default is to use a naïve BST.")

parser.add_argument('-d', '--debug', action='store_true',
                    help="Enables debug mode.")

args = parser.parse_args()

ops = Operations()

for file in args.operations:
        ops.read_ops(file)

algs = ['simple', 'rb', 'splay', 'avl', 'wavl', 'tango', 'static']

algo = ""
algarg = args.algorithm.lower().replace(' ', '')

if algarg in {'simple', 'bst', 'simplebst'}:
        algo = algs[0]

elif algarg in {'rb', 'redblack', 'redblacktree'}:
        algo = algs[1]

elif algarg in {'splay', 'splaytree'}:
        algo = algs[2]

elif algarg in {'avl', 'avltree'}:
        algo = algs[3]

elif algarg in {'wavl', 'wavltree', 'weakavl', 'weakavltree'}:
        algo = algs[4]

elif algarg in {'tango', 'tangotree'}:
        algo = algs[5]

elif algarg in {'static', 'osbst', 'optimalstatic', 'opt', 'optbst', 'optimalstaticbst'}:
        algo = algs[6]

else:
        err.err("Algorithm not recognized.")

ops.exec_ops(algo, args.debug)
