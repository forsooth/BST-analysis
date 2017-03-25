import shlex
import err


class Operation():
        def __init__(self, op, arg):
                self.op = op
                self.arg = arg

        def __str__(self):
                return self.op + ": " + self.arg

class Operations():
        def __init__(self):
                self.allowed = {'ins', 'del', 'sea'}
                self.ops = []
                self.files = []

        def read_ops(self, filename):
                self.files.append(filename)
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
                                        new_op = Operation(op, elems[1])
                                        self.ops.append(new_op)
                                        break
                        else:
                                err.err("Badly formatted line: '" + line
                                        + "'. Unrecognized operation '"
                                        + elems[0] + "'.")
                f.close()

        def exec_ops(self):
                for op in self.ops:
                        print(op)
