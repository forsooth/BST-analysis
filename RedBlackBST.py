import AbstractBST
from api import API

class RedBlackBST(AbstractBST.AbstractBST):
        # RedBlackBST
        def __init__(self, api):
                super(RedBlackBST, self).__init__()
                self.__api = api

        def __str__(self):
                return self.__api.__str__()
                
        def insert(self, value):
                self.__api.reset()
                self.insert_help(value)
                
        def insert_help(self, value):
                y = None
                while not self.__api.is_null():
                        if value < self.__api.read_value():
                                self.__api.move_left()
                        elif value > self.__api.read_value():
                                self.__api.move_right()
                        else:
                                self.__api.inc_count()
                                return

                self.__api.add(value)
                self.__api.write_closure("color", "RED")
                # Color the children "dummy nodes" black
                self.__api.move_left()
                self.__api.write_closure("color", "BLACK")
                self.__api.move_parent()
                self.__api.move_right()
                self.__api.write_closure("color", "BLACK")
                self.__api.move_parent()
                self.insert_fix()

        def has_children(self):
                children = ""
                self.__api.move_left()
                if not self.__api.is_null():
                        children += "l"
                self.__api.move_parent()
                self.__api.move_right()
                if not self.__api.is_null():
                        children += "r"
                self.__api.move_parent()
                return children

        def successor(self):
                moves = 1
                self.__api.move_right()
                while "l" in self.has_children():
                        self.__api.move_left()
                        moves = moves + 1
                s = (self.__api.read_value(), self.__api.get_count())
                for i in range(0, moves):
                        self.__api.move_parent()
                return s
                
        def child_color(self, left_or_right):
                if left_or_right is "l":
                        self.__api.move_left()
                else:
                        self.__api.move_right()
                color = self.__api.read_closure("color")
                self.__api.move_parent()
                return color

        def sibling_color(self):
                m = self.__api.move_parent()
                if m is "l":
                        self.__api.move_right()
                else:
                        self.__api.move_left()
                c = [self.__api.read_closure("color"), self.child_color("l"), self.child_color("r")]
                self.__api.move_parent()
                self.__api.move(m)
                return c
                
        def parent_color(self):
                m = self.__api.move_parent()
                if m is "":
                        return None
                parent_color = self.__api.read_closure("color")
                self.__api.move(m)
                return parent_color

        def color_parent(self, color):
                m = self.__api.move_parent()
                self.__api.write_closure("color", color)
                self.__api.move(m)
                
        def grand_parent_color(self):
                m = self.__api.move_grand_parent()
                if m is "":
                        return None
                grand_parent_color = self.__api.read_closure("color")
                self.__api.move(m)
                return grand_parent_color

        def color_grand_parent(self, color):
                m = self.__api.move_grand_parent()
                self.__api.write_closure("color", color)
                self.__api.move(m)
                
        def uncle_color(self):
                # Move to the grand-parent
                m = self.__api.move_grand_parent()
                if m is "":
                        return None
                # Move to the uncle
                self.__api.move("r" if m[0] == "l" else "l")
                uncle_color = self.__api.read_closure("color")
                self.__api.move_parent()
                self.__api.move(m)
                return uncle_color

        def color_uncle(self, color):
                # Move to the grand-parent
                m = self.__api.move_grand_parent()
                # Move to the uncle
                self.__api.move("r" if m[0] == "l" else "l")
                uncle_color = self.__api.write_closure("color", color)
                self.__api.move_parent()
                self.__api.move(m)

                
        def repeat_case(self, c):
                self.__api.move_grand_parent()
                if c is "l":
                        self.__api.rotate_right()
                else:
                        self.__api.rotate_left()
                color = self.__api.read_closure("color")
                if c is "l":
                        self.__api.move_right()
                else:
                        self.__api.move_left()
                color2 = self.__api.read_closure("color")
                self.__api.write_closure("color", color)
                self.__api.move_parent()
                self.__api.write_closure("color", color2)
                if c is "l":
                        self.__api.move_left()
                else:
                        self.__api.move_right()
                                        
        def insert_fix(self):
                if self.__api.is_root():
                        self.__api.write_closure("color", "BLACK")
                while self.parent_color() is "RED":
                        if self.uncle_color() is "RED":
                                self.color_parent("BLACK")
                                self.color_uncle("BLACK")
                                self.color_grand_parent("RED")
                                self.__api.move_grand_parent()
                                self.insert_fix()
                        else: # uncle_color is BLACK
                                case = self.__api.move_grand_parent()
                                self.__api.move(case)
                                if case[0] == "l" and case[1] == "l":
                                        self.repeat_case("l")
                                elif case[0] == "l" and case[1] == "r":
                                        self.__api.move_parent()
                                        self.__api.rotate_left()
                                        color = self.__api.read_closure("color")
                                        self.__api.move_parent()
                                        self.__api.rotate_right()
                                        self.__api.move_right()
                                        color2 = self.__api.read_closure("color")
                                        self.__api.write_closure("color", color)
                                        self.__api.move_parent()
                                        self.__api.write_closure("color", color2)
                                elif case[0] == "r" and case[1] == "r":
                                        self.repeat_case("r")
                                elif case[0] == "r" and case[1] == "l":
                                        self.__api.move_parent()
                                        self.__api.rotate_right()
                                        color = self.__api.read_closure("color")
                                        self.__api.move_parent()
                                        self.__api.rotate_left()
                                        self.__api.move_left()
                                        color2 = self.__api.read_closure("color")
                                        self.__api.write_closure("color", color)
                                        self.__api.move_parent()
                                        self.__api.write_closure("color", color2)
                

        def delete(self, value):
                self.__api.reset()
                return self.delete_help(value)
                
        def delete_help(self, value):
                if self.__api.is_null():
                        return False
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.__api.move_right()
                elif value == self.__api.read_value():
                        print(value)
                        return self.delete_cases(True)
                return self.delete_help(value)

        def delete_cases(self, delete):
                print("In delete cases")
                if len(self.has_children()) is 2:
                        # Case 1
                        print("Case 1")
                        (v, count) = self.successor()
                        print(self.__api.read_value())
                        print(v)
                        print(self)
                        self.__api.write_value(v)
                        self.__api.set_count(count)
                        print(self)
                        self.__api.move_right()
                        return self.delete_help(v)
                if self.child_color("l") is "RED" or self.child_color("r") is "RED" or self.__api.read_closure("color") is "RED":
                        # Case 2 -- one child; only of child or self is red
                        print("Case 2 -- Delete: " + str(delete))
                        print(self)
                        if delete: self.__api.std_remove()
                        print(self)
                        self.__api.write_closure("color", "BLACK")
                else:
                        # Case 3.3
                        if self.__api.is_root() and self.__api.read_closure("color") is "DBLACK":
                                print("Case 3.3")
                                self.__api.write_closure("color", "BLACK")
                                return
                        # Case 3 -- one child; both are black
                        print("Case 3")
                        print(self)
                        if delete: self.__api.std_remove()
                        # Case 3.1
                        print("Case 3.1")
                        print(self)
                        self.__api.write_closure("color", "DBLACK")
                        # Case 3.2 reduce DBLACK to BLACK
                        while self.__api.read_closure("color") is "DBLACK" and not self.__api.is_root():
                                print("Case 3.2")
                                # (a) is the sibling is black
                                sib = self.sibling_color()
                                if sib[0] is "BLACK" and (sib[1] is "RED" or sib[2]is "RED"):
                                        print("Case 3.2 a")
                                        # Left Left Case
                                        # Left Right Case
                                        # Right Right Case
                                        # Right Left Case
                                        case1 = self.__api.move_parent()
                                        if case1 is "r": # implies s is left child
                                                print("Left")
                                                self.__api.move_left()
                                                # Left left Case
                                                self.__api.move_left()
                                                if self.__api.read_closure("color") is "RED":
                                                        print("Left Case")
                                                        self.__api.move_grand_parent()
                                                        self.__api.move_right()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_right()
                                                        self.__api.move_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                        continue
                                                self.__api.move_parent()
                                                self.__api.move_right()
                                                # Left Right Case
                                                if self.__api.read_closure("color") is "RED":
                                                        print("Right Case")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.move_right()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_right()
                                                        continue
                                        else:
                                                print("Right")
                                                self.__api.move_right()
                                                # Right Right Case
                                                self.__api.move_right()
                                                if self.__api.read_closure("color") is "RED":
                                                        print("Right Case")
                                                        self.__api.move_grand_parent()
                                                        self.__api.move_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_left()
                                                        self.__api.move_right()
                                                        self.__api.write_closure("color", "BLACK")
                                                        continue
                                                self.__api.move_parent()
                                                self.__api.move_left()
                                                # Right Left Case
                                                if self.__api.read_closure("color") is "RED":
                                                        print("Left Case")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_right()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.move_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_left()
                                                        continue
                                # (b) sibling and both children are black
                                elif sib[0] is "BLACK":
                                        print("3.2 (b)")
                                        m = self.__api.move_parent()
                                        c = self.__api.read_closure("color")
                                        self.__api.write_closure("color", ("D" if c is "BLACK" else "") + "BLACK")
                                        self.__api.move("l" if m is "r" else "r")
                                        self.__api.write_closure("color", "RED")
                                        self.__api.move_parent()
                                        if self.__api.read_closure("color") is "DBLACK":
                                                return self.delete_cases(False)
                                # (c) if sibling is red
                                else:
                                        if delete: self.__api.std_remove()
                                        m = self.__api.move_parent()
                                        self.__api.write_closure("color", "RED")
                                        if m is "l":
                                               self.__api.rotate_left()
                                        else:
                                                self.__api.rotate_right()
                                        self.__api.write_closure("color", "BLACK")
                                        self.__api.move(m)
                                        self.__api.move(m)
                                        return self.delete_cases(False)

                        if self.__api.is_root() and self.__api.read_closure("color") is "DBLACK":
                                print("Case 3.3")
                                self.__api.write_closure("color", "BLACK")

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

#l1 = []
#l2 = []
#a = API(l1, l2)
#x = RedBlackBST(a)
# 
#for i in [5, 3, 7, 4, 8, 6, 2]:
#for i in [1, 2, 3, 4, 5, 6, 7, 8]:
#        print("insert: " + str(i))
#        x.insert(i)
#        print(x)
# print("search  5: " + str(x.search(5)))
# print("search  2: " + str(x.search(2)))
# print("search  4: " + str(x.search(4)))
# print("search 10: " + str(x.search(10)))
# print("search  1: " + str(x.search(1)))
# 
# 
# print("delete: " + str(x.delete(2)))
# print(x)
# 
# # Delete (using std_remove --  Not Implemented) 
# print("delete: " + str(x.delete(5)))
# print(x)
# print("delete: " + str(x.delete(6)))
# print(x)
# print("delete: " + str(x.delete(7)))
# print(x)
