import colors

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
                        return colors.t_red + self.v.__str__() + colors.t_nc
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

                        indent = colors.t_blue
                        if cur.v == None:
                                nodev = colors.t_gray + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + str(cur) + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + colors.t_nc
                        else:
                                nodev = colors.t_yellow + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + str(cur)  + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + colors.t_gray + ' (' + str(cur.count) + ')' + colors.t_nc

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
                                output += nodev + '\n'
                        elif not first_child:
                                output += indent + '└' + '─'
                                output += ' ' + nodev + '\n'
                        else:
                                output += indent + '├' + '─'
                                output += ' ' + nodev + '\n'

                return output

