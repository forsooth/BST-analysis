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
                if self.debug == 1:
                        err.log("Generating DOT for tree diagram number " + str(self.graph_num))

                graph = Digraph()
                graph.format = 'pdf'
                # graph.body.extend(['size="10,10"', 'dpi="600"'])
                graph.body.extend(['size="5,5"'])
                graph.attr('graph', fontname='InputMono')
                graph.attr('node', shape='circle')
                graph.attr('node', style='filled')
                graph.attr('node', color='black')
                graph.attr('node', fixedsize='true')
                graph.attr('node', height='0.75')
                graph.attr('node', width='0.75')
                graph.attr('node', fontcolor='white')
                graph.attr('node', fontname='InputMono')
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
                        if self.debug == 2:
                                nodecolor = 'blue'
                else:
                        nodes.add(child_name)
                        graph.attr('edge', weight='10')
                        graph.attr('edge', color='black')

                graph.attr('node', color=nodecolor)

                graph.node(child_name)

                if parent_name is not None:
                        graph.edge(parent_name, child_name)

