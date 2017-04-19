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
                    help="Number of each BST operations to generate.")

parser.add_argument('-t', '--type', type=str, default='int',
                    help="Data type of the operation arguments. Allowed"
                         + " values are 'str', 'int', and 'float'.")

parser.add_argument('-u', '--max', type=int, default='20',
                    help="Maximum value of data. Default is 20.")

parser.add_argument('-l', '--min', type=int, default='1',
                    help="Minimum value of data. Default is 1.")

parser.add_argument('-id', '--ins_distribution', default='random',
                    help="Distribution of the insert data. Allowed values"
                         + " are 'random', 'gaussian', and 'increasing'.")

parser.add_argument('-sd', '--sea_distribution', default='random',
                    help="Distribution of the search data. Allowed values"
                         + " are 'random', 'gaussian', and 'increasing'.")

parser.add_argument('-dd', '--del_distribution', default='random',
                    help="Distribution of the delete data. Allowed values"
                         + " are 'random', 'gaussian', and 'increasing'.")

parser.add_argument('-p', '--pattern', default='Ids',
                    help="Summarized form of --insert, --delete, and --search "
                         + "options, for faster operation selection. Specifies all"
                         + "operations to use in the input. Allowed values"
                         + " are 'i'/'I', 'd'/'D', and 's'/'S', or any combination"
                         + " thereof, e.g. 'ids'. Order matters unless"
                         + " the letter is lowercase. Default is 'Ids'.")

parser.add_argument('-w', '--write', action='store_true',
                    help="Write the generated input to a file in inputs/.")

args = parser.parse_args()

n = args.number
if n < 1:
        err.err("Number of operations to generate must be at least 1.")

input_type = args.type
types = ['int', 'float', 'str']
if input_type not in types:
        err.err("Type of operations must be one of " + str(types) + ".")

upper = args.max
lower = args.min

if upper < lower:
        err.err("Maximum value for input must be larger than minimum.")

idist = args.ins_distribution
sdist = args.sea_distribution
ddist = args.del_distribution

dists = ['random', 'increasing', 'decreasing', 'balanced']
if idist not in dists:
        err.err("Insert distribution type must be one of " + str(dists) + ".")
if sdist not in dists:
        err.err("Search distribution type must be one of " + str(dists) + ".")
if ddist not in dists:
        err.err("Delete distribution type must be one of " + str(dists) + ".")

op_types = args.pattern

ops = []

for c in op_types:
        if c == 'i':
                ops.append(('r', 'ins'))
        elif c == 'I':
                ops.append(('d', 'ins'))
        elif c == 'd':
                ops.append(('r', 'del'))
        elif c == 'D':
                ops.append(('d', 'del'))
        elif c == 's':
                ops.append(('r', 'sea'))
        elif c == 'S':
                ops.append(('d', 'sea'))

data = []
cur_ops = []

# for 'increasing' distribution
try:
        ins_slope = (upper - lower + 1) / (n * len(args.pattern.lower().replace('s', '').replace('d', '')))
except ZeroDivisionError:
        ins_slope = 0
try:
        sea_slope = (upper - lower + 1) / (n * len(args.pattern.lower().replace('i', '').replace('d', '')))
except ZeroDivisionError:
        sea_slope = 0
try:
        del_slope = (upper - lower + 1) / (n * len(args.pattern.lower().replace('i', '').replace('s', '')))
except ZeroDivisionError:
        del_slope = 0

ins_cur = lower
sea_cur = lower
del_cur = lower
if idist == 'decreasing':
        ins_cur = upper
if sdist == 'decreasing':
        sea_cur = upper
if ddist == 'decreasing':
        del_cur = upper

ins_i = 0.0
sea_i = 0.0
del_i = 0.0

ins_inc = 1
sea_inc = 1
del_inc = 1
if idist == 'decreasing':
        ins_inc = -1
if sdist == 'decreasing':
        sea_inc = -1
if ddist == 'decreasing':
        del_inc = -1

num = 1
denom = 2

for i, (op_type, op) in enumerate(ops):
        if op_type == 'r':
                cur_ops.append(op)
                if i + 1 < len(ops) and ops[i+1][0] == 'r':
                        continue
        else:
                cur_ops.append(op)

        for j in range(0, len(cur_ops) * n):

                op = cur_ops[random.randint(0, len(cur_ops) - 1)]

                if input_type == 'int':
                        if op == 'ins':
                                if idist == 'random':
                                        a = random.randint(lower, upper)
                                elif idist == 'increasing' or idist == 'decreasing':
                                        a = ins_cur
                                        ins_i += ins_slope
                                        while ins_i >= 1:
                                                ins_cur += ins_inc
                                                ins_i -= 1
                                elif idist == 'balanced':
                                        a = lower + num * (upper - lower) // denom
                                        if num == denom - 1:
                                                denom *= 2
                                                num = 1
                                        else:
                                                num += 2

                        elif op == 'sea':
                                if sdist == 'random':
                                        a = random.randint(lower, upper)
                                elif sdist == 'increasing' or sdist == 'decreasing':
                                        a = sea_cur
                                        sea_i += sea_slope
                                        while sea_i >= 1:
                                                sea_cur += sea_inc
                                                sea_i -= 1
                        elif op == 'del':
                                if ddist == 'random':
                                        a = random.randint(lower, upper)
                                elif ddist == 'increasing' or ddist == 'decreasing':
                                        a = del_cur
                                        del_i += del_slope
                                        while del_i >= 1:
                                                del_cur += del_inc
                                                del_i -= 1


                                
                elif input_type == 'float':
                        a = random.random() * upper + lower
                elif input_type == 'str':
                        ALPH = "abcdefghijklmnopqrstuvwxyz"
                        STRLEN = 5
                        a = "\""
                        for k in range(0, STRLEN):
                                r = random.randint(0, len(ALPH) - 1)
                        a += ALPH[r]
                        a += "\""

                data.append(op + " " + str(a))

        cur_ops = []

for line in data:
        print(line)

write = args.write

if write:
        outf = open('inputs/' + str(datetime.now()) + ".ops", 'w')
        for line in data:
                outf.write(line + '\n')
        outf.close()

outf = open('inputs/last_run.ops', 'w')
for line in data:
        outf.write(line + '\n')
outf.close()