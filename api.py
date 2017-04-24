import BSTDataModel
import err


class API():
        def __init__(self, logn, logt, gen_graphs, graphs, debug):
                self.__bst = BSTDataModel.BSTDataModel(debug)
                root = BSTDataModel.Node(None, None)
                root.p = root
                self.debug = debug
                self.graphs = graphs
                self.gen_graphs = gen_graphs
                self.__bst.root = root
                self.__bst.cur = root
                self.__bst.count = 0
                self.__log = False
                self.__t = 0
                self.__logn = logn
                self.__logt = logt

        def __str__(self):
                return self.__bst.__str__()

        def viz(self):
                if self.gen_graphs:
                        self.graphs.append(self.__bst.viz_tree())

        def set_log_on(self):
                self.__log = True

        def set_log_off(self):
                self.__log = False

        def set_time(self, t):
                self.__t = t

        def log_on(self):
                return self.__log

        def log(self, n, t):
                self.__logn.append(n)
                self.__logt.append(t)

        def t(self):
                return self.__t

        def value(self):
                return self.__bst.cur.v

        def left(self):
                return self.__bst.cur.l

        def right(self):
                return self.__bst.cur.r

        def parent(self):
                return self.__bst.cur.p

        def reset(self):
                self.__bst.cur = self.__bst.root

        def set_value(self, v):
                self.__bst.cur.v = v

        def set_left(self, l):
                self.__bst.cur.l = l

        def set_right(self, r):
                self.__bst.cur.r = r

        def set_parent(self, p):
                self.__bst.cur.p = p

        def reset(self):
                self.__bst.cur = self.__bst.root

        @staticmethod
        def null(node):
                # Returns True if the current node is None or its value is
                # i.e. if the current node can be added (self.__bst.cur should never be None)
                return node is None or node.v is None

        def is_null(self):
                # Returns True if the current node is None or its value is
                # i.e. if the current node can be added (self.__bst.cur should never be None)
                return self.__bst.cur is None or self.__bst.cur.v is None

        def is_root(self):
                return self.__bst.cur is self.__bst.root

        # Adds a node with value 'value' to the tree at the current location,
        # if and only if the value of the current node is 'None'.
        def add(self, value):
                if value is None or self.__bst.cur is None:
                        return False

                if self.__bst.cur.v is value:
                        self.inc_count()
                else:
                        self.__bst.count = 1

                self.write_value(value)

                lc = BSTDataModel.Node(None, self.__bst.cur)
                rc = BSTDataModel.Node(None, self.__bst.cur)
                self.__bst.cur.l = lc
                self.__bst.cur.r = rc

                if self.log_on() and self.__bst.cur.v is not None:
                        self.log(self.__bst.cur.v, self.t())

                return True

        # Performs a standard BST removal, replacing the current node with
        # its positive successor. If the node to be removed is 'None',
        # the function returns 'False'. The current node at the end of the
        # operation is at the location of node removed from the tree. If the
        # node removed was a leaf, the None node which replaced it is current.
        def std_remove(self, ignore_count=False):
                if self.null(self.__bst.cur):
                        return False
                elif self.__bst.cur.count > 1 and not ignore_count:
                        self.__bst.cur.count -= 1
                        return True
                elif not self.null(self.__bst.cur.l) and not self.null(self.__bst.cur.r):

                        # Grab current node's right child
                        rc = self.__bst.cur.r

                        self.move_right()

                        while not self.null(self.__bst.cur.l):
                                self.move_left()

                        s = self.__bst.cur.v
                        sc = self.__bst.cur.count
                        # scl = self.__bst.cur.cl

                        if self.__bst.cur is rc:
                                self.std_remove(True)
                        else:
                                self.std_remove(True)
                                while self.__bst.cur.p is not rc:
                                        self.move_parent()
                                self.move_parent()

                        self.move_parent()
                        self.__bst.cur.v = s
                        self.__bst.cur.count = sc
                        # self.__bst.cur.scl = scl

                        return True
                # If there is only a left successor, then go to the parent;
                # if the node to be removed is the parent's left child, link
                # the parents left child to the successor. Otherwise, link
                # 1the parent's right child to the successor. In either case,
                # tell the successor about its new parent.
                elif self.null(self.__bst.cur.l):
                        if self.is_root():
                                self.__bst.root = self.__bst.cur.r
                                self.__bst.cur = self.__bst.root
                                return True
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.r
                        else:
                                p.r = self.__bst.cur.r
                        self.__bst.cur.r.p = self.__bst.cur.p
                        # Explicitly Ensure we end up on the None where node was
                        self.__bst.cur = self.__bst.cur.r 
                        return True
                # Same but if only a right successor exists.
                # TODO: Merge these two conditions, e.g.
                #(successor = bst.cur.l == None ? bst.cur.l : bst.cur.r)
                # ...
                elif self.null(self.__bst.cur.r):
                        if self.is_root():
                                self.__bst.root = self.__bst.cur.l
                                self.__bst.cur = self.__bst.root
                                return True
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.l
                        else:
                                p.r = self.__bst.cur.l
                        self.__bst.cur.l.p = self.__bst.cur.p
                        # Explicitly Ensure we end up on the parent
                        self.__bst.cur = self.__bst.cur.l
                        return True
                # Find out which side of the parent the node-to-delete is on,
                # and set it to 'None'
                else:
                        self.remove()
                        return True

        def remove(self):
                if self.__bst.cur is None:
                        return False
                if self.__bst.cur.v is None:
                        self.__bst.cur = None
                        return True
                self.__bst.cur.v = None
                self.__bst.cur.l.p = None
                self.__bst.cur.r.p = None
                self.__bst.cur.l = None
                self.__bst.cur.r = None
                return True
        
        # Preforms a standard insert on a BST. Traverses the tree to an empty 
        # leaf node or to the value and adds to the BST.
        def std_insert(self, value):
                while not self.is_null():
                        node_value = self.read_value()
                        if value < node_value:
                                self.move_left()
                        elif value > node_value:
                                self.move_right()
                        elif value == node_value:
                                self.inc_count()
                                break
                if self.is_null():
                        self.add(value)

        # Preforms a standard search on the tree. 
        # Traverses the tree to the value if the value is in the tree or
        # to a None leaf node found in the standard traversal.
        # Returns False if not found and True if found.
        def std_search(self, value):
                if self.is_null():
                        return False
                elif value == self.read_value():
                        return True
                elif value < self.read_value():
                        self.move_left()
                elif value > self.read_value():
                        self.move_right()
                return self.std_search(value)

        def read_closure(self, key):
                # returns the closure for the node you are currently on
                return self.__bst.cur.cl[key]

        def write_closure(self, key, val):
                self.__bst.cur.cl[key] = val # sets the closure for the current node

        def read_gclosure(self, key):
                return self.__bst.gcl[key] # reads the global closure

        def write_gclosure(self, key, val):
                self.__bst.gcl[key] = val # writes the closure

        def read_value(self):
                if self.log_on() and self.__bst.cur.v is not None:
                        self.log(self.__bst.cur.v, self.t())
                return self.__bst.cur.v

        def write_value(self, value):
                if value is None:
                        return False
                self.__bst.cur.v = value
                if self.log_on():
                        self.log(self.__bst.cur.v, self.t())
                return True

        def inc_count(self):
                self.__bst.cur.count += 1

        def get_count(self):
                return self.__bst.cur.count

        def dec_count(self):
                self.__bst.cur.count -= 1

        def set_count(self, v):
                self.__bst.cur.count = v
                
        def move_right(self):
                if self.debug > 1:
                        err.log(str(self.t()) + " Moving right on " + str(self.__bst.cur))
                if self.__bst.cur.v is not None:
                        if self.log_on():
                                self.log(self.__bst.cur.v, self.t())
                        self.__bst.cur = self.__bst.cur.r

        def move_left(self):
                if self.debug > 1:
                        err.log(str(self.t()) + " Moving left on " + str(self.__bst.cur))
                if self.__bst.cur.v is not None:
                        if self.log_on():
                                self.log(self.__bst.cur.v, self.t())
                        self.__bst.cur = self.__bst.cur.l

        def move_parent(self):
                if self.debug > 1:
                        err.log(str(self.t()) + " Moving to parent on " + str(self.__bst.cur))
                moved = ""
                if self.__bst.cur is self.__bst.root:
                        return moved
                if self.__bst.cur.p is not None and self.__bst.cur.p.l == self.__bst.cur:
                        moved = "l"
                elif self.__bst.cur.p is not None:
                        moved = "r"
                self.__bst.cur = self.__bst.cur.p
                return moved

        def move_grand_parent(self):
                return str(self.move_parent() + self.move_parent())[::-1]
        
        def move(self, moves):
                for c in moves:
                        if c is "l":
                                self.move_left()
                        elif c is "r":
                                self.move_right()
                        elif c is 'p':
                                self.move_parent()
                        else:
                                continue

        def rotate_left(self):
                # print("------------ROTATE LEFT---------------")
                # print("Valid Tree: " + str( self.verify_tree()))
                if self.debug > 1:
                        err.log(str(self.t()) + " Left rotate on " + str(self.__bst.cur))
                if self.is_null():
                        return False
                # print("Left ROTATE on " + str(self.__bst.cur) + ": ")
                # print(self.__bst)

                # Save each node and sub-trees
                # parent = self.__bst.cur.p
                
                p = self.__bst.cur
                q = p.r
                b = q.l

                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                # Re-assign to preform a rotation
                if self.__bst.cur is self.__bst.root:
                        self.__bst.root = q
                        self.__bst.root.p = self.__bst.root
                elif self.__bst.cur is self.__bst.cur.p.l:
                        parent = self.__bst.cur.p
                        parent.l = q
                        q.p = parent
                else:
                        parent = self.__bst.cur.p
                        parent.r = q
                        q.p = parent

                ## print("Q: " + str(q))
                ## print("P: " + str(p))
                ## print("B: " + str(b))

                ## print("Q.p: " + str(q.p))
                ## print("P.p: " + str(p.p))
                ## print("B.p: " + str(b.p))

                # print("q.l = p\np.p = q")
                q.l = p
                p.p = q

                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                p.r = b
                b.p = p

                # print(str(self))
                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                self.__bst.cur = q
                # print("CURRENT")
                # print(self)
                # print("Still Valid?: " + str( self.verify_tree()))
                # print("------------ROTATE LEFT END---------------")
                

        def rotate_right(self):
                # print("------------ROTATE RIGHT---------------")
                # print("Valid Tree: " + str( self.verify_tree()))
                if self.debug > 1:
                        err.log(str(self.t()) + " Right rotate on " + str(self.__bst.cur))
                if self.is_null():
                        return False
                # print("RIGHT ROTATE on " + str(self.__bst.cur) + ": ")
                # print(self.__bst)

                # Save each node and sub-trees
                # parent = self.__bst.cur.p
                
                q = self.__bst.cur
                p = q.l
                b = p.r

                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                # Re-assign to preform a rotation
                if self.__bst.cur is self.__bst.root:
                        self.__bst.root = p
                        self.__bst.root.p = self.__bst.root
                elif self.__bst.cur is self.__bst.cur.p.l:
                        parent = self.__bst.cur.p
                        parent.l = p
                        p.p = parent
                else:
                        parent = self.__bst.cur.p
                        parent.r = p
                        p.p = parent

                ## print("Q: " + str(q))
                ## print("P: " + str(p))
                ## print("B: " + str(b))

                ## print("Q.p: " + str(q.p))
                ## print("P.p: " + str(p.p))
                ## print("B.p: " + str(b.p))

                # print("q.l = p\np.p = q")
                p.r = q
                q.p = p

                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                q.l = b
                b.p = q

                # print(str(self))
                # print("Q: " + str(q))
                # print("P: " + str(p))
                # print("B: " + str(b))

                # print("Q.p: " + str(q.p))
                # print("P.p: " + str(p.p))
                # print("B.p: " + str(b.p))

                self.__bst.cur = p
                # print("CURRENT")
                # print(self)
                # print("Still Valid?: " + str( self.verify_tree()))
                # print("------------ROTATE RIGHT END---------------")

        def verify_tree(self, rb=False):
                return self.__bst.verify(rb)
