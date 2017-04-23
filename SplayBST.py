import AbstractBST
from api import API


class SplayBST(AbstractBST.AbstractBST):
        # SplayBST
        def __init__(self, api):
                super(SplayBST, self).__init__()
                self.__api = api

        def __str__(self):
                return self.__api.__str__()
                
        def insert(self, value): 
                self.__api.std_insert(value)
                self.splay()        

        def delete(self, value):
                s = self.__api.std_remove(value)
                if self.__api.is_null():
                        self.__api.move_parent()
                self.splay()
                return s
                
        def search(self, value):
                s = self.__api.std_search(value)
                if self.__api.is_null():
                        self.__api.move_parent()
                self.splay()
                return s

        def splay(self):
                if self.__api.is_root():
                        return
                if self.__api.is_null():
                        print("Error -- can't splay None Node")
                        return
                path = self.__api.move_parent()
                if self.__api.is_root():
                        if path is "l":
                                self.__api.rotate_right()
                        else:
                                self.__api.rotate_left()
                        return
                path += self.__api.move_parent()
                # zig-zig case
                if path[0] == path[1]:
                        if path[0] is "l":
                                self.__api.rotate_right() # Rotate grand-parent -- Placing parent at cur
                                self.__api.rotate_right() # Rotate Parent -- Placing node to splay at cur
                        else:
                                self.__api.rotate_left()
                                self.__api.rotate_left()
                # zig-zag case
                else:
                        self.__api.move(path[1]) # move to parent
                        if path[1] is "l":
                                self.__api.rotate_left()
                                self.__api.move_parent()
                                self.__api.rotate_right()
                        else:
                                self.__api.rotate_right()
                                self.__api.move_parent()
                                self.__api.rotate_left()
                self.splay()

        def verify_tree(self):
                return self.__api.verify_tree(False)
