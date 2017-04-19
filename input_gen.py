#!/usr/local/bin/python
import err
import random
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Generates random input '
                                             + 'operations, places them in '
                                             + 'the inputs directory, and '
                                             + 'prints them to standard '
                                             + 'output.')

parser.add_argument('-n', '--number', type=int, default='25',
                    help="Number of BST operations to generate.")

parser.add_argument('-t', '--type', type=str, default='int',
                    help="Data type of the operation arguments. Allowed"
                         + " values are 'str', 'int', and 'float'.")

parser.add_argument('-u', '--max', type=int, default='20',
                    help="Maximum value of data. Default is 20.")

parser.add_argument('-l', '--min', type=int, default='1',
                    help="Minimum value of data. Default is 1.")

parser.add_argument('-d', '--distribution', default='random',
                    help="Distribution of the data. Allowed values"
                         + " are 'random', 'gaussian', and 'increasing'.")

parser.add_argument('-o', '--operations', default='i',
                    help="Operations to use in the input. Allowed values"
                         + " are 'i', 'd', and 's', or any combination"
                         + " thereof, e.g. 'ids'")

parser.add_argument('-w', '--write', action='store_true',
                    help="Write the generated input to a file in inputs/.")

args = parser.parse_args()

n = args.number
if n < 1:
        err.err("Number of operations to generate must be at least 1.")

input_type = args.type
if input_type not in ['int', 'float', 'str']:
        err.err("Type of operations must be one of 'int', 'float', or 'str'.")

upper = args.max
lower = args.min

if upper < lower:
        err.err("Maximum value for input must be larger than minimum.")

dist = args.distribution
if dist not in ['random', 'gaussian', 'increasing']:
        err.err("Distribution type must be one of 'random', 'gaussian', 'increasing'.")

op_types = args.operations
insert = False
search = False
delete = False
for c in op_types:
        if c == 'i':
                insert = True
        if c == 's':
                search = True
        if c == 'd':
                delete = True

ops = []
if insert:
        ops.append('ins')
if search:
        ops.append('sea')
if delete:
        ops.append('del')

data = []
if input_type == 'int':
        for i in range(0, n):
                a = random.randint(lower, upper)
                op = ops[random.randint(0, len(ops) - 1)]
                data.append(op + " " + str(a))
if input_type == 'float':
        for i in range(0, n):
                a = random.random() * upper + lower
                op = ops[random.randint(0, len(ops) - 1)]
                data.append(op + " " + str(a))
if input_type == 'str':
        alph = "abcdefghijklmnopqrstuvwxyz"
        for i in range(0, n):
                a = ""
                for i in range(0, 5):
                        r = random.randint(0, len(alph) - 1)
                        a += alph[r]

                op = ops[random.randint(0, len(ops) - 1)]
                data.append(op + " " + str(a))

for line in data:
        print(line)

write = args.write

if write:
        outf = open('inputs/' + str(datetime.now()) + ".ops", 'w')
        for line in data:
                outf.write(line + '\n')
        outf.close()

