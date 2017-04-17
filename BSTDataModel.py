

#Node — typical node of a BST
# The node is a recursive data type for a BST, where the parameters left,
# right, and parent are all of type Node. A node has the following data
# members:
#        v  - (any type) the value stored in the node
#        l  - the left child
#        r  - the right child
#        cl - closure for the particular Node (for RB tree, WAVL tree...)
class Node:
        def __init__(self, value, parent, left=None, right=None, closure=None):
                self.v = value
                self.count = 1
                self.p = parent
                self.l = left
                self.r = right
                self.cl = closure

        def __str__(self):
                return self.v.__str__()


# BSTDataModel - class that represents a binary tree
#         current      - the class provides access to a current node
#                        for tree traversal
#         root         - root of the tree
class BSTDataModel:
        def __init__(self):
                self.root = None
                self.cur = self.root
        def __str__(self):
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
                                level[i] = str(elem)

                output = ""
                for level in levels:
                        for elem in level:
                                output += elem + "   "
                        output += '\n'
                return output

# Example:
# bst = BSTDataModel()
# bst.root = Node(4, None, Node(2, None), Node(5, None))
# print(bst)
