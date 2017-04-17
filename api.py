import BSTDataModel

class API():
        def __init__(self):
                self.__bst = BSTDataModel.BSTDataModel()
                root = BSTDataModel.Node(None, None)
                root.p = root
                self.__bst.root = root
                self.__bst.cur = root
                self.__bst.count = 0

        def __str__(self):
                return self.__bst.__str__()

        # Adds a node with value 'value' to the tree at the current location,
        # if and only if the value of the current node is 'None'.
        def add(self, value):
                if value is None or self.__bst.cur is None:
                        return False
                if self.__bst.cur.v is None:
                        self.inc_count()
                self.__bst.cur.v = value
                lc = BSTDataModel.Node(None, self.__bst.cur)
                rc = BSTDataModel.Node(None, self.__bst.cur)
                self.__bst.cur.l = lc
                self.__bst.cur.r = rc
                return True

        # Performs a standard BST removal, replacing the current node with
        # its positive successor. If the node to be removed is 'None',
        # the function returns 'False'.
        def std_remove(self):
                if self.null(self.__bst.cur):
                        return False
                elif not self.null(self.__bst.cur.l) and not self.null(self.__bst.cur.r):

                        # Grab current node's right child
                        rc = self.__bst.cur.r

                        self.move_right()

                        while not self.null(self.__bst.cur.l):
                                self.move_left()

                        s = self.__bst.cur.v

                        if self.__bst.cur is rc:
                                self.std_remove()
                        else:
                                self.std_remove()
                                while self.__bst.cur.p is not rc:
                                        self.move_parent()
                                self.move_parent()

                        self.move_parent()
                        self.__bst.cur.v = s

                        return True
                # If there is only a left successor, then go to the parent;
                # if the node to be removed is the parent's left child, link
                # the parents left child to the successor. Otherwise, link
                # 1the parent's right child to the successor. In either case,
                # tell the successor about its new parent.
                elif self.null(self.__bst.cur.l):
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.r
                        else:
                                p.r = self.__bst.cur.r
                        self.__bst.cur.l.p = self.__bst.cur.p
                        return True
                # Same but if only a right successor exists.
                # TODO: Merge these two conditions, e.g.
                #(successor = bst.cur.l == None ? bst.cur.l : bst.cur.r)
                # ...
                elif self.null(self.__bst.cur.r):
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.l
                        else:
                                p.r = self.__bst.cur.l
                        self.__bst.cur.r.p = self.__bst.cur.p
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

        def read_closure(self):
                pass # returns the closure for the node you are currently on

        def write_closure(self, cl):
                pass # sets the closure for the current node

        def read_gclosure(self):
                pass # reads the global closure

        def write_gclosure(self, cl):
                pass # writes the closure

        def read_value(self):
                return self.__bst.cur.v

        def write_value(self, value):
                if value is None:
                        return False
                self.__bst.cur.v = value
                return True

        def inc_count(self):
                self.__bst.cur.count += 1

        def move_right(self):
                if self.__bst.cur.v is not None:
                        self.__bst.cur = self.__bst.cur.r

        def move_left(self):
                if self.__bst.cur.v is not None:
                        self.__bst.cur = self.__bst.cur.l

        def move_parent(self):
                self.__bst.cur = self.__bst.cur.p

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
