import AbstractBST
from api import API


class AVLBST(AbstractBST.AbstractBST):
        # AVLBST - example of concrete implementation of AbstractBST
        def __init__(self, api):
                super(AVLBST, self).__init__()
                self.__api = api
                api.tree_type = "avl"

        def __str__(self):
                return self.__api.__str__()
        
        def get_child_height(self, left):
                self.__api.move(left)
                height = 0 if self.__api.is_null() else self.__api.read_closure("height")
                self.__api.move_parent()
                return height

        def get_child_value(self, left):
                self.__api.move(left)
                value = self.__api.read_value()
                self.__api.move_parent()
                return value

        def calculate_height(self):
                left = self.get_child_height("l")
                right = self.get_child_height("r")
                return max(left, right) + 1

        def calculate_balance(self):
                if self.__api.is_null():
                        return 0
                return self.get_child_height("l") - self.get_child_height("r")

        def insert(self, value):
                self.__api.reset()
                return self.insert_help(value)

        def insert_help(self, value):
                while not self.__api.is_null():
                        if value < self.__api.read_value():
                                self.__api.move_left()
                        elif value > self.__api.read_value():
                                self.__api.move_right()
                        elif value == self.__api.read_value():
                                self.__api.inc_count()
                                return True

                self.__api.add(value)
                self.__api.write_closure("height", 1)
                
                while not self.__api.is_root():

                        self.__api.move_parent()

                        self.__api.write_closure("height", self.calculate_height())

                        balance = self.calculate_balance()

                        if balance >  1 and value < self.get_child_value("l"): # Left Left Case
                                self.rotate("r")

                        elif balance < -1 and value > self.get_child_value("r"): # Right Right
                                self.rotate("l")

                        elif balance >  1 and value > self.get_child_value("l"): # Left Right Case
                                self.__api.move_left()
                                self.rotate("l")
                                self.__api.move_parent()
                                self.rotate("r")

                        elif balance < -1 and value < self.get_child_value("r"): # Right Left Case
                                self.__api.move_right()
                                self.rotate("r")
                                self.__api.move_parent()
                                self.rotate("l")
                        elif balance == 0:
                                break
                return True

        def rotate(self, right):
                self.__api.rotate(right)
                # Re-calculate the new child node first 
                self.__api.move(right)
                self.__api.write_closure("height", self.calculate_height())
                # Re-calculate the parent
                self.__api.move_parent()
                self.__api.write_closure("height", self.calculate_height())
                        
        # Returns true if current is a left child
        def is_left_child(self):
                l = self.__api.move_parent()
                self.__api.move(l)
                return l is "l"

        def has_children(self):
                children = ""

                # Left Child
                if not self.__api.is_null():
                        self.__api.move_left()
                        if not self.__api.is_null():
                                children += "l"
                        self.__api.move_parent()

                # Right Child
                if not self.__api.is_null():
                        self.__api.move_right()
                        if not self.__api.is_null():
                                children += "r"
                        self.__api.move_parent()
                
                return children

        # Returns the value and count of the successor
        # Sets the successor's count to 1
        # Maintains location of cur
        # For use with moving successor into the node and deleting the successor
        def successor(self):
                # count the 1's move to the right
                moves = 1
                self.__api.move_right()
                
                # move all the way left to the successor
                while "l" in self.has_children():
                        self.__api.move_left()
                        moves = moves + 1
                
                # Get the value and the count
                s = (self.__api.read_value(), self.__api.get_count())
                
                # Set the count to 1 -- prep for deletion
                self.__api.set_count(1)
                
                # Move back to the original node
                for i in range(0, moves):
                        self.__api.move_parent()
                
                return s

        def delete(self, value):
                self.__api.reset()
                
                self.__api.std_search(value)
                
                if self.__api.is_null(): return False

                (sv, sc) = self.successor()

                if sv is not None:
                        self.__api.write_value(sv)
                        self.__api.set_count(sc)
                        self.__api.move_right()
                        self.__api.std_search(sv)
                
                return self.delete_help()
                
        def delete_help(self):
                if not self.__api.std_remove():
                        return False

                while not self.__api.is_root():
                        self.__api.move_parent()
                        self.__api.write_closure("height", self.calculate_height())

                        balance = self.calculate_balance()

                        self.__api.move_left()
                        l_b = self.calculate_balance()
                        self.__api.move_parent()

                        self.__api.move_right()
                        r_b = self.calculate_balance()
                        self.__api.move_parent()

                        if   balance >  1 and l_b >= 0: # Left Left Case
                                self.rotate("r")

                        elif balance > 1 and l_b < 0: # Left Right Case
                                self.__api.move_left()
                                self.rotate("l")
                                self.__api.move_parent()
                                self.rotate("r")

                        elif balance < -1 and r_b <= 0: # Right Right Case
                                self.rotate("l")

                        elif balance < -1 and r_b > 0: # Right Left Case
                                self.__api.move_right()
                                self.rotate("r")
                                self.__api.move_parent()
                                self.rotate("l")
                return True

        def search(self, value):
                return self.__api.std_search(value)

        def verify_tree(self):
                return self.__api.verify_tree()
