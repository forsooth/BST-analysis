import colors
import err
from graphviz import Digraph

# Node — typical node of a BST
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
                if "color" in self.cl and self.cl["color"] is "RED":
                        return colors.t_red + self.v.__str__() + colors.t_nc
                elif "color" in self.cl and self.cl["color"] is "DBLACK":
                        return colors.t_green + self.v.__str__() + colors.t_nc
                return self.v.__str__()

        def __repr__(self):
                return self.v.__str__()


# BSTDataModel - class that represents a binary tree
#         current      - the class provides access to a current node
#                        for tree traversal
#         root         - root of the tree
class BSTDataModel:
        def __init__(self, debug):
                self.root = None
                self.cur = self.root
                self.gcl = {}
                self.debug = debug
                self.graph_num = 0

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
                                nodev = colors.t_yellow + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + colors.t_yellow + str(cur) + (colors.t_green + '║' + colors.t_nc if cur is self.cur else '') + colors.t_gray + ' (' + str(cur.count) + ')' + colors.t_nc

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

        @staticmethod
        def null(node):
                return node is None or node.v is None

        def viz_tree(self):
                self.graph_num += 1
                if self.debug > 0:
                        err.log("Generating DOT for tree diagram number " + str(self.graph_num))

                graph = Digraph()
                graph.format = 'eps'
                graph.body.extend(['size="10,10"', 'fontpath="/home/M/.fonts/"'])
                graph.attr('node', shape='circle')
                graph.attr('node', style='filled')
                graph.attr('node', color='black')
                graph.attr('node', fixedsize='true')
                graph.attr('node', height='0.75')
                graph.attr('node', width='0.75')
                graph.attr('node', fontcolor='white')
                graph.attr('node', fontname='InputMono-Bold')
                graph.attr('edge', arrowhead='none')
                graph.attr('edge', style='filled')

                stack = [self.root]
                nodes = set()
                while len(stack) > 0:
                        self.add_node(stack.pop(), stack, graph, nodes)
                return graph

        def add_node(self, node, stack, graph, nodes, find=None, draw=None):
                
                nodec = 'black'
                if not self.null(node) and "color" in node.cl and node.cl["color"] is "RED":
                        nodec = colors.h_red

                if node == self.root:
                        parent = None
                else:
                        parent = repr(node.p)

                nodev = repr(node)

                # Draw this node (if we haven't seen it before)
                if nodev not in nodes:
                        self.draw_node(graph, nodes, parent, nodev, nodecolor=nodec)

                # To make the diagram look balanced we insert invisible nodes (debug = 2 to see them)
                # Regardless of invisible nodes, we draw the left child if it exists
                if not self.null(node.l):
                        nodec = 'black'
                        if "color" in node.l.cl and node.l.cl["color"] is "RED":
                                nodec = colors.h_red
                        stack.append(node.l)
                        self.draw_node(graph, nodes, nodev, repr(node.l), nodecolor=nodec)
                        if not self.null(node.r):
                                # if the node has two children, insert an invisible node between them
                                self.draw_node(graph, nodes, nodev, "[" + nodev, style_type="invisible")

                # if there's no left child but there is a right one, add an invisible left child
                elif not self.null(node.r):
                                self.draw_node(graph, nodes, nodev, "|" + nodev, style_type="invisible")

                # Regardless of invisible nodes, we draw the right child if it exists
                if not self.null(node.r):
                        nodec = 'black'
                        if "color" in node.r.cl and node.r.cl["color"] is "RED":
                                nodec = colors.h_red
                        stack.append(node.r)
                        self.draw_node(graph, nodes, nodev, repr(node.r), nodecolor=nodec)
                # if there's no right child but there is a left one, draw an invisible right child
                elif not self.null(node.l):
                                self.draw_node(graph, nodes, nodev, "]" + nodev, style_type="invisible")



        def draw_node(self, graph, nodes, parent_name, child_name, nodecolor='white', style_type='filled'):


                if style_type == "invisible":
                        graph.attr('edge', weight='100')
                        graph.attr('edge', color='white')
                        if self.debug > 2:
                                nodecolor = 'blue'
                else:
                        nodes.add(child_name)
                        graph.attr('edge', weight='10')
                        graph.attr('edge', color='black')

                graph.attr('node', color=nodecolor)

                graph.node(child_name)

                if parent_name is not None:
                        graph.edge(parent_name, child_name)

        # Verifies the properties of the Tree
        def verify(self, rb=False):
                ref = self.verify_tree_ref()
                val = self.verify_tree_val()
                rbl = self.verify_rb()
                err.log("Pointers: " + str(ref))
                err.log("Value: " + str(val))
                if rbl: 
                        err.log("RedBlack: " + str(rbl))
                return ref and val and (rbl or not rb)

        # Function verifies that the references to children, parents on all internal
        # and fake leaf nodes are valid. Also ensures each internal node contain a non-None
        # value and external nodes do.
        def verify_tree_ref(self):
                node = self.root
                
                # The parent of the root node should always be root
                if node.p is not node:
                        err.warn("Root's ("+str(node)+") parent isn't root")
                        return False

                # Verify the parent and children pointers are valid for each subtree
                left  = self.verify_tree_ref_helper(node, node.l, True)
                right = self.verify_tree_ref_helper(node, node.r, False)
                
                err.log("Left of Root: " + str(left))
                err.log("Left of Root: " + str(right))
                
                return left and right

        def verify_tree_ref_helper(self, parent, node, left):
                if node is None:
                        return True
                # Check that the parent pointer is pointed to the parent
                parent_is_parent = node.p is parent

                # Ensure that node is the left or right child of the parent
                parent_child_is_node = False

                if left:
                        parent_child_is_node = node.p.l is node
                else:
                        parent_child_is_node = node.p.r is node

                # Ensure that children are valid
                valid_children = False

                # If the value of the node is None then the left and right should be None
                # Base Case:
                if node.v is None:
                        valid_children = node.l is None and node.r is None
                else:
                        # Verify the left and right
                        valid_children = self.verify_tree_ref_helper(node, node.l, True)
                        valid_children = valid_children and self.verify_tree_ref_helper(node, node.r, False)

                # IFF everything is valid:
                return parent_is_parent and parent_child_is_node and valid_children

        # Verify that the BST properties hold
        def verify_tree_val(self):
                node = self.root
                left  = self.verify_tree_val_helper(node, node.l, True ) 
                right = self.verify_tree_val_helper(node, node.r, False)
                return left and right

        # Verify that the value of the node is less or more than the parent
        def verify_tree_val_helper(self, parent, node, isLess):
                # Vacuous Truth
                if node.v is None or node is None:
                        return True
                # Node and parent can't have same value
                # BST data model assumes unique values
                if node.v == parent.v:
                        return False
                # If the value of the node is greater than the parent 
                # and we traversed left (isLess == True) then return False
                # else
                # if the value of the node is less than the parent and we 
                # traversed right (isLess == False) then return False
                if node.v > parent.v is isLess:
                        return False

                # Verify the left and right subtrees
                left  = self.verify_tree_val_helper(node, node.l, True ) 
                right = self.verify_tree_val_helper(node, node.r, False)
                return left and right

        # Verifies the red black tree properties:
        #  - Every node is either red or black
        #  - Every leaf (None) is black.
        #  - If a node is red, then both its children are black.
        #  - Every simple path from a node to a descendant leaf contains the same number of black nodes.
        def verify_rb(self):
                black_or_red = self.verify_black_or_red()
                black_children = self.verify_red_has_black_children()
                black_height = self.verify_black_height() is not -1
                err.log("Each node is Black or Red: " + str(black_or_red))
                err.log("Each Red node has black children: " + str(black_children))
                err.log("Black Heights Match: " + str(black_height))
                return black_height and black_children and black_or_red

        def verify_black_height(self):
                return self.verify_black_height_helper(self.root)

        # Returns -1 if the black height's don't match
        # Returns Black hight otherwise
        def verify_black_height_helper(self, node):
                if node.v is None:
                        return 1

                left  = self.verify_black_height_helper(node.l)
                right = self.verify_black_height_helper(node.r)

                if left is -1 or right is -1:
                        return -1

                if "color" not in node.cl:
                        return 0

                if left is right:
                        if node.cl["color"] is "BLACK":
                                return left + 1
                        else:
                                return left
                else:
                        return -1


        def verify_red_has_black_children(self):
                return self.verify_red_has_black_children_helper(self.root, False)

        # Assumes tree is colored and not None
        # Verifies that each red node has two black children
        def verify_red_has_black_children_helper(self, node, red_parent):
                if node.v is None:
                        return True

                if "color" not in node.cl:
                        return True

                if red_parent and node.cl["color"] is not "BLACK":
                        err.log("Red Node \w red parent: " + str(node.v))
                        return False

                red_parent = node.cl["color"] is "RED"

                left  = self.verify_red_has_black_children_helper(node.l, red_parent)
                right = self.verify_red_has_black_children_helper(node.r, red_parent)
                return left and right

        def verify_black_or_red(self):
                return self.verify_black_or_red_helper(self.root)

        # Verifies the two RB-BST properties listed below
        #  - Every node is either red or black
        #  - Every leaf (None) is black.
        #  - Root is Black
        def verify_black_or_red_helper(self, node):
                # If the color is not set something is wrong
                if "color" not in node.cl:
                        return False

                # Check if the color is RED or BLACK explicitly
                if node.cl["color"] is not "RED" and node.cl["color"] is not "BLACK":
                        return False

                # If the node is the root then it must be colored black:
                if node is self.root and node.cl["color"] is not "BLACK":
                        return False

                # Base Case:
                # If the node is RED or BLACK and the value is None i.e. it is a leaf
                # Ensure it is labeled BLACK
                if node.v is None and node.cl["color"] is not "BLACK":
                        return False

                # If we have recursed to the bottom of the tree
                if node.v is None:
                        return True

                left  = self.verify_black_or_red_helper(node.l)
                right = self.verify_black_or_red_helper(node.r)

                return left and right
