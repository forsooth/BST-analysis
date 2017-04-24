import shlex
import err
from api import API
from SimpleBST import SimpleBST
from RedBlackBST import RedBlackBST
from SplayBST import SplayBST
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

        def exec_ops(self, algo, pages, gen_graphs, no_clean, debug):
                logt = []
                logn = []
                opst = []
                opsn = []

                graphs = []

                api = API(logn, logt, gen_graphs, graphs, debug)
                if algo == 'simple':
                        tree = SimpleBST(api)
                elif algo == 'rb':
                        tree = RedBlackBST(api)
                elif algo == 'splay':
                        tree = SplayBST(api)
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
                        if debug > 2:
                                tree_str = str(tree) 
                        if debug > 1:
                                err.log("operation #" + str(time) + ": " + str(op))
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
                                opst.append(time)
                                opsn.append(op.arg)
                                api.set_time(time)
                                api.set_log_on()
                                tree.search(op.arg)
                                api.set_log_off()
                                time += 1
                        elif op.op == 'del':
                                opst.append(time)
                                opsn.append(op.arg)
                                api.set_time(time)
                                api.set_log_on()
                                tree.delete(op.arg)
                                api.set_log_off()
                                time += 1
                        if debug == 2:
                                err.warn(tree)
                        if debug > 2:
                                err.log("Before op, tree was:")
                                err.warn(tree_str)
                                err.log("After op, tree is:")
                                err.warn(tree)
                                err.warn("Beginning tree verification:")
                                if tree.verify_tree():
                                        err.warn("Verified")
                                else:
                                        err.err("Issue found when verifying tree!")
                        if gen_graphs and pages:
                                api.viz()

                if gen_graphs and not pages:
                        api.viz()
                        
                if debug == 1 and len(self.ops) < 50:
                        err.warn(tree)

                plot.plot(logn, logt, opsn, opst, pages, graphs, no_clean, debug)
