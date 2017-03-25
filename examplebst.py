import AbstractBST
import API

class ExampleBST(AbstractBST.AbstractBST):
        # ExampleBST - example of concrete implementation of AbstractBST
        def __init__(self):
                super(ExampleBST, self).__init__()
                self.__api = API()

        def insert(self, value): # WEIRD!! API lets us do insert non-recursivly
                # Assume we start on the root
                while not self.__api.is_null():
                        node_value = self.__api.read_value()
                        if value < node_value:
                                self.__api.move_left()
                        elif value > node_value:
                                self.__api.move_right()
                        elif value == node_value:
                                self.__api.inc_count()
                                break
                if self.__api.is_null():
                        self.__api.add(value)
                        

        def delete(self, value):
                if self.__api.is_null():
                        return False
                elif value == self.__api.read_value():
                        self.__api.std_remove(value)
                        return True
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.move_right()
                return delete(self, value)

                
        def search(self, value):
                if self.__api.is_null():
                        return False
                elif value == self.__api.read_value():
                        return True
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.move_right()
                return search(self, value)

x = ExampleBST()

