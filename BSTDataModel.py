

#Node — typical node of a BST
# The node is a recursive data type for a BST, where the parameters left,
# right, and parent are all of type Node. A node has the following data
# members:
#        v  - (any type) the value stored in the node
#        l  - the left child
#        r  - the right child
#        cl - closure for the particular Node (for RB tree, WAVL tree...)
class Node:
        def __init__(self, value, parent, left=None, right=None, closure=[]):
                self.v = value
                self.count = 1
                self.p = parent
                self.l = left
                self.r = right
                self.cl = {}

        def __str__(self):
                if "color" in self.cl.keys() and self.cl["color"] is "RED":
                        return '\033[38;5;203m' + self.v.__str__() + '\033[00m'
                return self.v.__str__()

        def __repr__(self):
                return self.v.__str__() 


# BSTDataModel - class that represents a binary tree
#         current      - the class provides access to a current node
#                        for tree traversal
#         root         - root of the tree
class BSTDataModel:
        def __init__(self):
                self.root = None
                self.cur = self.root
                self.gcl = {}

        def __str__2(self):
                levels = []
                this_level = [self.root]
                next_level = []
                empty_level = False
                while not empty_level:
                        empty_level = True
                        next_level = []
                        for node in this_level:
                                if node:
                                        empty_level = False
                                        next_level.append(node.l)
                                        next_level.append(node.r)
                                else:
                                        next_level.append(None)
                                        next_level.append(None)
                        if not empty_level:
                                levels.append(this_level)
                        this_level = next_level

                for level in levels:
                        for i, elem in enumerate(level):
                                if elem is None:
                                        level[i] = " "
                                        continue
                                level[i] = str(elem)

                output = ""
                for level in levels:
                        for elem in level:
                                output += elem + "   "
                        output += '\n'
                return output

        def __str__(self):
                output = ""
                nodes = [self.root]
                levels = [0]
                while len(nodes) > 0:
                        cur = nodes.pop()
                        level = levels.pop()
                        if cur.r != None:
                                nodes.append(cur.r)
                                levels.append(level + 1)
                        if cur.l != None:
                                nodes.append(cur.l)
                                levels.append(level + 1)

                        indent = ""
                        for i in range(1, level):
                                if i in levels:
                                        indent += '│  '
                                else:
                                        indent += '   '
                        if len(levels) == 0:
                                first_child = False
                        else:
                                first_child = (level in levels)
                        if level == 0:
                                output += str(cur.v) + '\n'
                        elif not first_child:
                                output += indent + '└' + '─'
                                output += ' ' + str(cur.v) + '\n'
                        else:
                                output += indent + '├' + '─'
                                output += ' ' + str(cur.v) + '\n'

                return output


# Example:
# bst = BSTDataModel()
# bst.root = Node(4, None, Node(2, None), Node(5, None))
# print(bst)

#            a
#        b       c
#     d    e   f    g
# 
# 
# 1 a
# 2 bc
# 3 dec
# 4 nnec
# 4 nec
# 3 ec
# 4 nnc
# 4 nc
# 2 c
# 3 fg
# 4 nng
# 4 ng
# 3 g
# 4 nn
# 4 n
