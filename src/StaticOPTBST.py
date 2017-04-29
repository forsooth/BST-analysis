import AbstractBST
from api import API


class StaticOPTBST(AbstractBST.AbstractBST):
        # WeakAVLBST - example of concrete implementation of AbstractBST
        def __init__(self, api):
                super(StaticOPTBST, self).__init__()
                self.__api = api
                api.tree_type = "staticopt"

        def __str__(self):
                return self.__api.__str__()
        

        def insert(self, value):
                pass

        def delete(self, value):
                pass

        def search(self, value):
                return self.__api.std_search(value)

        def verify_tree(self):
                return self.__api.verify_tree()
