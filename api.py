import BSTDataModel


# TODO: re-implement things like 'move' and 'add' in terms of other operations,
# or keep track of the operations occuring and write them to the log
# separately.
class API():
        def __init__(self):
                self.__bst = BSTDataModel.BSTDataModel()
                root = BSTDataModel.Node(None, None)
                root.p = root
                self.__bst.root = root
                self.__bst.cur = root

        # Adds a node with value 'value' to the tree at the current location,
        # if and only if the value of the current node is 'None'.
        def add(self, value):
                if value is None or self.__bst.current is None:
                        return False
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
                if self.__bst.cur is None:
                        return False
                elif self.__bst.cur.l.v is not None and self.__bst.cur.r.v is not None:
                        # Identify a successor
                        s = self.__bst.cur.r
                        while s.l is not None:
                                s = s.l
                        s = s.p
                        # Grab current node's children and parent
                        lc = self.__bst.cur.l
                        rc = self.__bst.cur.r
                        p = self.__bst.cur.p
                        # Deal with any children of the successor
                        # TODO: fix this, as it wont work until std_remove is
                        # implemented in terms of other operations
                        std_remove(s)
                        # Set the successor's parent and children
                        s.p = p
                        s.l = lc
                        s.r = rc
                        lc.p = s
                        rc.p = s
                        # Set the parent's child to be 's' instead of 'bst.cur'
                        if p.l == self.__bst.cur:
                                p.l = s
                        else:
                                p.r = s
                        return True
                # If there is only a left successor, then go to the parent;
                # if the node to be removed is the parent's left child, link
                # the parents left child to the successor. Otherwise, link
                # the parent's right child to the successor. In either case,
                # tell the successor about its new parent.
                elif self.__bst.cur.l is not None:
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.l
                        else:
                                p.r = self.__bst.cur.l
                        self.__bst.cur.l.p = p
                        return True
                # Same but if only a right successor exists.
                # TODO: Merge these two conditions, e.g.
                #(successor = bst.cur.l == None ? bst.cur.l : bst.cur.r)
                # ...
                elif self.__bst.cur.r is not None:
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = self.__bst.cur.r
                        else:
                                p.r = self.__bst.cur.r
                        self.__bst.cur.r.p = p
                        return True
                # Find out which side of the parent the node-to-delete is on,
                # and set it to 'None'
                else:
                        p = self.__bst.cur.p
                        if p.l == self.__bst.cur:
                                p.l = None
                        else:
                                p.r = None
                        return True

        def read_closure(self):
                pass # returns the closure for the node you are currently on

        def write_closure(self, cl):
                pass # sets the closure for the current node

        def read_gclosure(self):
                pass # reads the global closure

        def write_gclosure(self, cl):
                pass # writes the closure

        def is_null(self):
                return self.__bst.cur is None

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
