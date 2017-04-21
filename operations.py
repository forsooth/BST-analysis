import shlex
import err
from api import API
from SimpleBST import SimpleBST
from RedBlackBST import RedBlackBST
import plot
import sys

def is_float(string):
        try:
                return float(string) and '.' in string
        except ValueError:
                return False


class Operation():
        def __init__(self, op, arg):
                self.op = op
                self.arg = arg

        def __str__(self):
                return self.op + " " + str(self.arg)


class Operations():
        def __init__(self):
                self.allowed = {'ins', 'del', 'sea'}
                self.ops = []
                self.files = []

        def read_ops(self, filename):
                self.files.append(filename)
                if filename == '-':
                        f = sys.stdin
                else:
                        f = open(filename, 'r')
                for line in f:
                        if line.isspace() or line[0] == '#':
                                continue
                        line = line.replace('\n', '')
                        elems = shlex.split(line)
                        if len(elems) > 2:
                                err.err("Badly formatted line: '" + line
                                        + "'. Too many arguments to "
                                        + "operation.")
                        elif len(elems) < 2:
                                err.err("Badly formatted line: '" + line
                                        + "'. No argument to operation.")
                        for op in self.allowed:
                                if op == elems[0]:
                                        hyphen = (elems[1][0] == '-')
                                        if elems[1].isnumeric() or (hyphen and elems[1][1:].isnumeric()):
                                                new_op = Operation(op, int(elems[1]))
                                        elif is_float(elems[1]):
                                                new_op = Operation(op, float(elems[1]))
                                        else:
                                                new_op = Operation(op, elems[1])
                                        self.ops.append(new_op)
                                        break
                        else:
                                err.err("Badly formatted line: '" + line
                                        + "'. Unrecognized operation '"
                                        + elems[0] + "'.")
                if f is not sys.stdin:
                        f.close()

        def exec_ops(self, algo, pages, debug):
                logt = []
                logn = []
                opst = []
                opsn = []
                api = API(logn, logt, debug)
                if algo == 'simple':
                        tree = SimpleBST(api)
                elif algo == 'rb':
                        tree = RedBlackBST(api)
                elif algo == 'splay':
                        err.err("Algorithm not yet implemented")
                elif algo == 'avl':
                        err.err("Algorithm not yet implemented")
                elif algo == 'wavl':
                        err.err("Algorithm not yet implemented")
                elif algo == 'tango':
                        err.err("Algorithm not yet implemented")
                elif algo == 'static':
                        err.err("Algorithm not yet implemented")

                time = 1
                for op in self.ops:
                        if debug:
                                err.log("step " + str(time) + ": " + str(op))
                        api.reset()
                        if op.op == 'ins':
                                opst.append(time)
                                opsn.append(op.arg)
                                api.set_time(time)
                                api.set_log_on()
                                tree.insert(op.arg)
                                api.set_log_off()
                                time += 1
                        elif op.op == 'sea':
                                tree.search(op.arg)
                        elif op.op == 'del':
                                tree.delete(op.arg)
                        if debug:
                                err.warn(tree)

                #api.viz()

                plot.plot(logn, logt, opsn, opst, pages)
