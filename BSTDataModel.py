import colors
from pydotplus import graphviz as pydot

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

        def viz_tree(self):
                graph = pydot.Dot(graph_type='digraph', nodesep=.5, pad=.3, size="10, 10", dpi=720, fontpath='/home/M/.fonts/')
                graph.set_node_defaults(style="filled", fillcolor="grey")
                graph.set_edge_defaults(color="black", arrowhead="vee")
                stack = [self.root]
                nodes = dict()
                while len(stack) > 0:
                        self.sketchTree(stack.pop(), stack, graph, nodes)
                return graph

        def sketchTree(self, node, stack, graph, nodes, find=None, draw=None):
                fillcolor = "black"
                if node != None:
                        if "color" in node.cl.keys() and node.cl["color"] is "RED":
                                fillcolor = colors.h_red

                self.draw(graph, nodes, None, repr(node), fill_color=fillcolor)

                if node.l != None and node.l.v != None:
                        self.draw(graph, nodes, repr(node), repr(node.l), fill_color=fillcolor)
                        stack.append(node.l)
                        if node.r != None and node.r.v != None:
                                # insert invisible third node in-between left and right nodes
                                self.draw(graph, nodes, repr(node), ":"+repr(node), fill_color=fillcolor, style_type="invisible")
                elif node.r != None and node.r.v != None:
                        # draw any missing left branches as invisible nodes/edges with dummy unique labels 
                        self.draw(graph, nodes, repr(node), ":"+repr(node), fill_color=fillcolor, style_type="invisible")
               
                if node.r != None and node.r.v != None:
                        self.draw(graph, nodes, repr(node), repr(node.r), fill_color=fillcolor)
                        stack.append(node.r)
                elif node.l != None and node.l.v != None:
                        # draw any missing right branches as invisible nodes/edges with dummy unique labels 
                        self.draw(graph, nodes, repr(node), ";"+repr(node), fill_color=fillcolor, style_type="invisible")


        def draw(self, graph, nodes, parent_name, child_name, fill_color, style_type='filled', font_color='white'):
                if style_type == "invisible":
                        # save original edge defaults
                        weight_ = "100"
                        saveEdgeDefaults = graph.get_edge_defaults()[0]
                        graph.set_edge_defaults(style=style_type, color="white", arrowhead="none") 
                else:
                        weight_ = "3"

                if parent_name is not None:
                        edge = pydot.Edge(parent_name, child_name, style=style_type, weight=weight_)
                        graph.add_edge(edge)  
                        if style_type == "invisible":
                                graph.set_edge_defaults(**saveEdgeDefaults)
        
                        if not nodes:
                                nodes[parent_name] = pydot.Node(parent_name, label=parent_name, fillcolor=fill_color, style=style_type, fontcolor=font_color, shape='circle', fontname='InputMono-Regular.ttf')
                                graph.add_node(nodes[parent_name]) 
                        if (parent_name not in nodes):    
                                nodes[parent_name] = pydot.Node(parent_name, label=parent_name, fillcolor=fill_color, style=style_type, fontcolor=font_color, shape='circle', fontname='InputMono-Regular.ttf')
                                graph.add_node(nodes[parent_name])
                        if child_name not in nodes:
                                nodes[child_name] = pydot.Node(child_name, label=child_name, fillcolor=fill_color, style=style_type, fontcolor=font_color, shape='circle', fontname='InputMono-Regular.ttf')
                                graph.add_node(nodes[child_name])
                else:
                        nodes[child_name] = pydot.Node(child_name, label=child_name, fillcolor=fill_color, style=style_type, fontcolor=font_color, shape='circle', fontname='InputMono-Regular.ttf')
                        graph.add_node(nodes[child_name])

