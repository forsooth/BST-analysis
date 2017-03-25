import AbstractBST
import API

class ExampleBST(AbstractBST.AbstractBST):
        # ExampleBST - example of concrete implementation of AbstractBST
        def __init__(self):
                super(ExampleBST, self).__init__()
                self.__api = API()

        def insert(self, value):
                # Assume we start on the root
                while not self.__api.is_null():
                        node_value = self.__api.read_value()
                        if value < node_value:
                                self.__api.move_left()
                        elif value > node_value:
                                self.__api.move_right()
                        elif value = node_value:
                                self.__api.inc_count()
                                break
                if self.__api.is_null():
                        self.__api.add(value)
                        

        def delete(self, value):
                print("Deleted " + str(value))

        def search(self, value):
                print("Found " + str(value))

x = ExampleBST()

