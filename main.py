import argparse
import err
from operations import Operations

parser = argparse.ArgumentParser(description='Generates 2D geometric represen'
                                 + 'tations of BSTs given input op'
                                 + 'erations and a BST variant.')

parser.add_argument('operations', type=str, nargs='+',
                    help="Path to file which list the the operations which "
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

err.log(str(args.operations))
err.log(args.output)
err.log(args.algorithm)
err.log(str(args.debug))

ops = Operations()

for file in args.operations:
        ops.read_ops(file)

ops.exec_ops()
