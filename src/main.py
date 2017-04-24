#!/usr/local/bin/python
import argparse
import err
from operations import Operations
import signal


def interrupt_catch(signal, frame):
        err.err('Keyboard interrupt detected. Exiting.')

signal.signal(signal.SIGINT, interrupt_catch)

parser = argparse.ArgumentParser(description='Generates 2D geometric represen'
                                 + 'tations of BSTs given input op'
                                 + 'erations and a BST variant.')

parser.add_argument('operations', type=str, nargs='+', 
                    help="Paths to files which list the the operations which "
                    + "the BST will perform. Default is standard input.")

# parser.add_argument('-o', '--output', type=str, default='-',
#                     help="Output location for BST instruction log file."
#                          + " Default is standard output.")

parser.add_argument('-a', '--algorithm', type=str, default='simple',
                    help="Algorithm to use in performing the desired"
                         "operations. Default is to use a naïve BST.")

parser.add_argument('-d', '--debug', action='store_true',
                    help="Enables debug mode.")

parser.add_argument('-l', '--debug_level', type=int, default='0',
                    help="Enables a certain level of debugging.")

parser.add_argument('-p', '--pages', action='store_true',
                    help="Enable full multi-page animated PDF.")

parser.add_argument('-g', '--graphs', action='store_true',
                    help="Enable addition of tree image to data output.")

parser.add_argument('-c', '--clean_off', action='store_true',
                    help="Disable cleanup of temporary files.")


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

debug = args.debug_level

if args.debug and debug == 0:
        debug = 1

if debug == 1:
        err.warn("Debug mode is set to: SIMPLE")
elif debug == 2:
        err.warn("Debug mode is set to: VERBOSE")
elif debug == 3:
        err.warn("Debug mode is set to: VERIFY")

ops.exec_ops(algo, args.pages, args.graphs, args.clean_off, debug)
