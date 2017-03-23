class Node:
        """
        Node - typical node of a BST
                v  - (any type) the value stored in the node
                l  - the left child
                r  - the right child
                cl - closure for the particular Node (for RB tree, WAVL tree...)
        """
        def __init__(self, val, parent, left = None, right = None, cl = None):
                self.v = val
                self.l = left
                self.r = right
                self.cl = cl
        def __str__(self):
                return self.v.__str__()
        

class BSTDataModel:
        """
        BSTDataModel - class that represents a binary tree
                current      - the class provides access to a current node 
                               for tree traversal
                root         - root of the tree
        """
        def __init__(self):
                self.root = None
                self.current = self.root
        def __str__(self):
                levels = []                     # list of levels
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
                return levels.__str__()         # can be prettified up later

# Example: 
# bst = BSTDataModel()
# bst.root = Node(4, None, Node(2, None), Node(5, None))
# print(bst)