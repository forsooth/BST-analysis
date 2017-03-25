import AbstractBST
from api import API

class ExampleBST(AbstractBST.AbstractBST):
        # ExampleBST - example of concrete implementation of AbstractBST
        def __init__(self):
                super(ExampleBST, self).__init__()
                self.__api = API()

        def __str__(self):
                return self.__api.__str__()
                
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
                        self.__api.std_remove()
                        return True
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.move_right()
                return self.delete(value)

                
        def search(self, value):
                if self.__api.is_null():
                        return False
                elif value == self.__api.read_value():
                        return True
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.__api.move_right()
                return self.search(value)

x = ExampleBST()
print(x.insert(2))
print(x.insert(3))
print(x)
print(x.delete(3))
print(x)
print(x.search(3))
