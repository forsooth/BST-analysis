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
                # Assume we start on the root -- except we don't
                # TODO: reset to root in run_opts??
                self.__api.reset()
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
                self.__api.reset()
                return self.delete_help(value)
                
        def delete_help(self, value):
                if self.__api.is_null():
                        return False
                elif value == self.__api.read_value():
                        return self.__api.std_remove()
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.__api.move_right()
                return self.delete_help(value)

        def search(self, value):
                self.__api.reset()
                return self.search_help(value)
                
        def search_help(self, value):
                if self.__api.is_null():
                        return False
                elif value == self.__api.read_value():
                        return True
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.__api.move_right()
                return self.search_help(value)

x = ExampleBST()

for i in [5, 3, 7, 4, 8, 6, 2]:
        print("insert: " + str(i))
        x.insert(i)

print(x)
print("search  5: " + str(x.search(5)))
print("search  2: " + str(x.search(2)))
print("search  4: " + str(x.search(4)))
print("search 10: " + str(x.search(10)))
print("search  1: " + str(x.search(1)))


# Delete (using std_remove --  Not Implemented) 
# print("delete: " + str(x.delete(2)))
# print(x)
