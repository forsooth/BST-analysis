#!/usr/local/bin/python
import err
import random
import argparse
from datetime import datetime
import os
import sys

cwd = sys.path[0]

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

dists = ['random', 'increasing', 'decreasing', 'balanced', 'nearly_increasing', 'nearly_decreasing', 'spider', 'gaussian']
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

num_ins = n * len(args.pattern.lower().replace('s', '').replace('d', ''))
num_sea = n * len(args.pattern.lower().replace('i', '').replace('d', ''))
num_del = n * len(args.pattern.lower().replace('i', '').replace('s', ''))

# for 'increasing' distribution
try:
        ins_slope = (upper - lower + 1) / (num_ins)
except ZeroDivisionError:
        ins_slope = 0
try:
        sea_slope = (upper - lower + 1) / (num_sea)
except ZeroDivisionError:
        sea_slope = 0
try:
        del_slope = (upper - lower + 1) / (num_del)
except ZeroDivisionError:
        del_slope = 0

ins_cur = lower
sea_cur = lower
del_cur = lower
if idist == 'decreasing' or idist == 'nearly_decreasing':
        ins_cur = upper
if sdist == 'decreasing' or sdist == 'nearly_decreasing':
        sea_cur = upper
if ddist == 'decreasing' or ddist == 'nearly_decreasing':
        del_cur = upper

ins_i = 0.0
sea_i = 0.0
del_i = 0.0

ins_inc = 1
sea_inc = 1
del_inc = 1
if idist == 'decreasing' or idist == 'nearly_decreasing':
        ins_inc = -1
if sdist == 'decreasing' or sdist == 'nearly_decreasing':
        sea_inc = -1
if ddist == 'decreasing' or ddist == 'nearly_decreasing':
        del_inc = -1

ins_num = 1
ins_denom = 2
sea_num = 1
sea_denom = 2
del_num = 1
del_denom = 2

ins_spider_i1 = num_ins // 5
ins_spider_i2 = 4 * num_ins // 5
ins_spider_count = 0

sea_spider_i1 = num_sea // 5
sea_spider_i2 = 4 * num_sea // 5
sea_spider_count = 0

del_spider_i1 = num_del // 5
del_spider_i2 = 4 * num_del // 5
del_spider_count = 0

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
                                elif idist == 'gaussian':
                                        if j == len(cur_ops) * n // 2:
                                                a = lower
                                        elif j == len(cur_ops) * n // 2 + 1:
                                                a = upper
                                        else:
                                                a = lower + int(random.gauss((upper + lower) // 2, (upper + lower) // 10))
                                                if a < lower:
                                                        a = lower
                                                elif a > upper:
                                                        a = upper
                                elif idist == 'increasing' or idist == 'decreasing':
                                        a = ins_cur
                                        ins_i += ins_slope
                                        while ins_i >= 1:
                                                ins_cur += ins_inc
                                                ins_i -= 1
                                elif idist == 'nearly_increasing' or idist == 'nearly_decreasing':
                                        a = ins_cur
                                        jitter = random.randint(-3, 3)
                                        ins_i += ins_slope
                                        while ins_i >= 1:
                                                ins_cur += ins_inc + jitter
                                                if ins_cur < lower:
                                                        ins_cur = lower
                                                elif ins_cur > upper:
                                                        ins_cur = upper
                                                ins_i -= 1
                                elif idist == 'balanced':
                                        a = lower + ins_num * (upper - lower) // ins_denom
                                        if ins_num == ins_denom - 1:
                                                ins_denom *= 2
                                                ins_num = 1
                                        else:
                                                ins_num += 2
                                elif idist == 'spider':
                                        if ins_spider_count < ins_spider_i1:
                                                a = random.randint(lower, lower + ins_spider_i1 * upper // num_ins)
                                        elif ins_spider_count == ins_spider_i1:
                                                ins_cur = lower + ins_spider_i1 * upper // num_ins
                                                a = ins_cur
                                        elif ins_spider_count > ins_spider_i1 and ins_spider_count < ins_spider_i2:
                                                a = ins_cur
                                                ins_i += ins_slope
                                                while ins_i >= 1:
                                                        ins_cur += ins_inc
                                                        ins_i -= 1
                                        elif ins_spider_count >= ins_spider_i2:
                                                a = random.randint(ins_spider_i2 * upper // num_ins, upper)
                                        ins_spider_count += 1


                        elif op == 'sea':
                                if sdist == 'random':
                                        a = random.randint(lower, upper)
                                elif sdist == 'gaussian':
                                        if j == len(cur_ops) * n // 2:
                                                a = lower
                                        elif j == len(cur_ops) * n // 2 + 1:
                                                a = upper
                                        else:
                                                a = lower + int(random.gauss((upper + lower) // 2, (upper + lower) // 10))
                                                if a < lower:
                                                        a = lower
                                                elif a > upper:
                                                        a = upper
                                elif sdist == 'increasing' or sdist == 'decreasing':
                                        a = sea_cur
                                        sea_i += sea_slope
                                        while sea_i >= 1:
                                                sea_cur += sea_inc
                                                sea_i -= 1
                                elif sdist == 'nearly_increasing' or sdist == 'nearly_decreasing':
                                        a = sea_cur
                                        jitter = random.randint(-3, 3)
                                        sea_i += sea_slope
                                        while sea_i >= 1:
                                                sea_cur += sea_inc + jitter
                                                if sea_cur < lower:
                                                        sea_cur = lower
                                                elif sea_cur > upper:
                                                        sea_cur = upper
                                                sea_i -= 1
                                elif sdist == 'balanced':
                                        a = lower + sea_num * (upper - lower) // sea_denom
                                        if sea_num == sea_denom - 1:
                                                sea_denom *= 2
                                                sea_num = 1
                                        else:
                                                sea_num += 2
                                elif sdist == 'spider':
                                        if sea_spider_count < sea_spider_i1:
                                                a = random.randint(lower, lower + sea_spider_i1 * upper // num_sea)
                                        elif sea_spider_count == sea_spider_i1:
                                                sea_cur = lower + sea_spider_i1 * upper // num_sea
                                                a = sea_cur
                                        elif sea_spider_count > sea_spider_i1 and sea_spider_count < sea_spider_i2:
                                                a = sea_cur
                                                sea_i += sea_slope
                                                while sea_i >= 1:
                                                        sea_cur += sea_inc
                                                        sea_i -= 1
                                        elif sea_spider_count >= sea_spider_i2:
                                                a = random.randint(sea_spider_i2 * upper // num_sea, upper)
                                        sea_spider_count += 1

                        elif op == 'del':
                                if ddist == 'random':
                                        a = random.randint(lower, upper)
                                elif ddist == 'gaussian':
                                        if j == len(cur_ops) * n // 2:
                                                a = lower
                                        elif j == len(cur_ops) * n // 2 + 1:
                                                a = upper
                                        else:
                                                a = lower + int(random.gauss((upper + lower) // 2, (upper + lower) // 10))
                                                if a < lower:
                                                        a = lower
                                                elif a > upper:
                                                        a = upper
                                elif ddist == 'increasing' or ddist == 'decreasing':
                                        a = del_cur
                                        jitter = random.randint(-3, 3)
                                        del_i += del_slope
                                        while del_i >= 1:
                                                del_cur += del_inc
                                                del_i -= 1
                                elif ddist == 'nearly_increasing' or ddist == 'nearly_decreasing':
                                        a = ins_cur
                                        jitter = random.randint(-3, 3)
                                        del_i += del_slope
                                        while del_i >= 1:
                                                del_cur += del_inc + jitter
                                                if del_cur < lower:
                                                        del_cur = lower
                                                elif del_cur > upper:
                                                        del_cur = upper
                                                del_i -= 1
                                elif ddist == 'balanced':
                                        a = lower + del_num * (upper - lower) // del_denom
                                        if del_num == del_denom - 1:
                                                del_denom *= 2
                                                del_num = 1
                                        else:
                                                del_num += 2
                                elif ddist == 'spider':
                                        if del_spider_count < del_spider_i1:
                                                a = random.randint(lower, lower + del_spider_i1 * upper // num_del)
                                        elif del_spider_count == del_spider_i1:
                                                del_cur = lower + del_spider_i1 * upper // num_del
                                                a = del_cur
                                        elif del_spider_count > del_spider_i1 and del_spider_count < del_spider_i2:
                                                a = del_cur
                                                del_i += del_slope
                                                while del_i >= 1:
                                                        del_cur += del_inc
                                                        del_i -= 1
                                        elif del_spider_count >= del_spider_i2:
                                                a = random.randint(del_spider_i2 * upper // num_del, upper)
                                        del_spider_count += 1


                                
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
        outf = open(cwd + '/../inputs/' + str(datetime.now()) + ".ops", 'w')
        for line in data:
                outf.write(line + '\n')
        outf.close()

outf = open(cwd + '/../inputs/last_run.ops', 'w')
for line in data:
        outf.write(line + '\n')
outf.close()
