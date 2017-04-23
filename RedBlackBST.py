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

        # Returns the value and count of the successor
        # Sets the successor's count to 0
        # Maintains location of cur
        def successor(self):
                moves = 1
                self.__api.move_right()
                while "l" in self.has_children():
                        self.__api.move_left()
                        moves = moves + 1
                s = (self.__api.read_value(), self.__api.get_count())
                self.__api.set_count(1)
                for i in range(0, moves):
                        self.__api.move_parent()
                return s

        def move_successor(self):
                self.__api.move_right()

                while not self.__api.is_null():
                        print(self.__api.read_value())
                        self.__api.move_left()

                self.__api.move_parent()

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

        def color_sibling(self, c):
                m = self.__api.move_parent()
                if m is "l":
                        self.__api.move_right()
                else:
                        self.__api.move_left()
                self.__api.write_closure("color", c)
                self.__api.move_parent()
                self.__api.move(m)
                
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

        def is_left_child(self):
                l = self.__api.move_parent()
                self.__api.move(l)
                return l is "l"

        def color_uncle(self, color):
                # Move to the grand-parent
                m = self.__api.move_grand_parent()
                # Move to the uncle
                self.__api.move("r" if m[0] == "l" else "l")
                uncle_color = self.__api.write_closure("color", color)
                self.__api.move_parent()
                self.__api.move(m)
                
        def repeat_case(self, c):
                print("REPEAT_CASE " + str(self.__api.read_value()))
                print("Move Grand-Parent")
                print(self)
                self.__api.move_parent()
                print("1")
                self.__api.move_parent()
                print(self)
                if c is "l":
                        self.__api.rotate_right()
                else:
                        self.__api.rotate_left()
                print(self)
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
                print("INSERT FIX")
                if self.__api.is_root():
                        print("IS ROOT")
                        self.__api.write_closure("color", "BLACK")
                while self.parent_color() is "RED":
                        print("Parent of " + str(self.__api.read_value()) + " is RED")
                        if self.uncle_color() is "RED":
                                print("UNCLE is RED")
                                self.color_parent("BLACK")
                                self.color_uncle("BLACK")
                                self.color_grand_parent("RED")
                                self.__api.move_grand_parent()
                                self.insert_fix()
                        else: # uncle_color is BLACK
                                print("UNCLE is BLACK")
                                #print(self)
                                case = self.__api.move_grand_parent()
                                self.__api.move(case)
                                print(case)
                                if case[0] == "l" and case[1] == "l":
                                        self.repeat_case("l")
                                elif case[0] == "l" and case[1] == "r":
                                        print("Left Right Case")
                                        self.__api.move_parent()
                                        print("Move to parent:")
                                        print(self)
                                        print("Left Rotate on " + str(self.__api.read_value()))
                                        self.__api.rotate_left()
                                        print(self.__api.verify_tree())
                                        self.__api.move_left()
                                        print("BEFORE REPEAT CASE")
                                        print(self)
                                        self.repeat_case("l")
                                        print("AFTER REPEAT CASE")
                                        print(self)
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
                
                # return self.delete_help(value, True)

                return self.rb_delete(value)
                
        def delete_help(self, value, delete):
                if self.__api.is_null():
                        return False
                elif value < self.__api.read_value():
                        self.__api.move_left()
                elif value > self.__api.read_value():
                        self.__api.move_right()
                elif value == self.__api.read_value():
                        # print(value)
                        return self.delete_cases(delete)
                return self.delete_help(value, delete)
        
        def rb_delete(self, value):                     # RB-DELETE(T, z)
                found = self.__api.std_search(value)    # if left[z] = nil[T] or right[z] = nil[T]

                if not found:
                        return False

                #    then y ← z

                sv = -1
                sc = -1

                if len(self.has_children()) is 2:
                        (sv, sc) = self.successor()
                        self.__api.write_value(sv)
                        self.__api.set_count(sc)
                        print("=========COPY SUCC+++++++++++")
                        print(self)
                        self.move_successor()
                        self.__api.set_count(1)
                        print("=====+++=+Move SUCC--------")
                        print(self)
                color = self.__api.read_closure("color")
                print(self)
                
                suc = self.__api.std_remove(sv)      #    else y ← TREE-SUCCESSOR(z)
                print(suc)
                print(self)

                if self.__api.is_null(): self.__api.write_closure("color", "BLACK")
                print("Deleting: " + str(self.__api.read_value()))
                
                print("Color "+color)
                print(self)
                if color is "BLACK":
                        #self.__api.move(self.has_children())
                        print(self)    # if left[y] ≠ nil[T]
                        self.rb_delete_fixup()          #    then x ← left[y]
                print(self)
                return suc                              #    else x ← right[y]
                                                        # p[x] ← p[y]
                                                        # if p[y] = nil[T]
                                                        #    then root[T] ← x
                                                        #     else if y = left[p[y]]
                                                        #             then left[p[y]] ← x
                                                        #             else right[p[y]] ← x
                                                        #  if y != z
                                                        #     then key[z] ← key[y]
                                                        #          copy y's satellite data into z
                                                        #  if color[y] = BLACK
                                                        #     then RB-DELETE-FIXUP(T, x)
                                                        #  return y
        def rb_delete_fixup(self):
                print("~~~~~~~~~~~~~~RB FIXUP~~~~~~~~~~~~~~~~~~~~~~")
                print("-----BEFORE------")
                print(self)
                print("WHILE LOOP")
                while not self.__api.is_root() and self.__api.read_closure("color") is "BLACK":
                        
                        if self.is_left_child():
                                print(self)
                                print(str(self.__api.read_value())+ " IS A LEFT CHILD")
                                sib = self.sibling_color()
                                print(sib)
                                if sib[0] is "RED":
                                        print("SIBLING IS RED")
                                        self.color_sibling("BLACK")
                                        self.color_parent("RED")
                                        self.__api.move_parent()
                                        self.__api.rotate_left()
                                        self.__api.move_left()
                                        self.__api.move_left()
                                        continue
                                if sib[1] is "BLACK" and sib[2] is "BLACK":
                                        print("BOTH s's CHILDREN ARE BLACK")
                                        self.color_sibling("RED")
                                        self.__api.move_parent()
                                        if(self.__api.read_closure("color") is "RED"):
                                                break
                                        #self.__api.move_parent()
                                        continue
                                elif sib[1] is "RED" and sib[2] is "BLACK":
                                        print("Left CHILD IS RED")
                                        self.__api.move_parent()
                                        self.__api.move_right() # Move to the sibling
                                        self.__api.move_left() # Move to the left child
                                        print("==> Move to s's left")
                                        self.__api.write_closure("color", "BLACK") 
                                        print("==> Colored BLACK")
                                        print(self)
                                        self.__api.move_parent() # Move back to sibling
                                        self.__api.write_closure("color", "RED")
                                        print("==> S is red")
                                        print(self)
                                        self.__api.rotate_right() # Right rotate sibling
                                        print("==> Right rotate s")
                                        
                                        #self.__api.reset()
                                        self.__api.move_parent() # Moving back to the node...
                                        print("==> Left Rotate p")
                                        self.__api.rotate_left()

                                        #self.__api.move_left() # Should be back at x
                                        print(self)
                                        self.__api.reset()
                                elif sib[2] is "RED": # Case 4
                                        self.color_sibling(self.parent_color())
                                        self.color_parent("BLACK")
                                        self.__api.move_parent()
                                        self.__api.move_right() # Move to the sibling
                                        self.__api.move_right() # move to the right[sib]
                                        self.__api.write_closure("color", "BLACK")
                                        self.__api.move_parent() # Move to sib
                                        self.__api.move_parent() # Move to parent
                                        self.__api.rotate_left()
                                        self.__api.reset()
                                        continue
                        else:
                                print(self)
                                print(str(self.__api.read_value())+ " IS A right CHILD")
                                sib = self.sibling_color()
                                print(sib)
                                if sib[0] is "RED":
                                        print("SIBLING IS RED")
                                        self.color_sibling("BLACK")
                                        self.color_parent("RED")
                                        self.__api.move_parent()
                                        self.__api.rotate_right()
                                        self.__api.move_right()
                                        self.__api.move_right()
                                        continue
                                if sib[1] is "BLACK" and sib[2] is "BLACK":
                                        print("BOTH s's CHILDREN ARE BLACK")
                                        print(self)
                                        self.color_sibling("RED")
                                        print(self)
                                        self.__api.move_parent()
                                        if(self.__api.read_closure("color") is "RED"):
                                                break
                                        # self.__api.move_parent()
                                        continue
                                elif sib[2] is "RED" and sib[1] is "BLACK":
                                        print("right CHILD IS RED")
                                        print(self)
                                        self.__api.move_parent()
                                        self.__api.move_left() # Move to the sibling
                                        print(" ==> Moved to s")
                                        print(self)
                                        self.__api.move_right() # Move to the right child
                                        self.__api.write_closure("color", "BLACK") 
                                        print(" ==> Moved to s's right")
                                        print(self)
                                        self.__api.move_parent() # Move back to sibling
                                        print(" ==> Moved to parent")
                                        print(self)
                                        self.__api.write_closure("color", "RED")
                                        self.__api.rotate_left() # left rotate sibling
                                        self.__api.move_parent() # Moving back to the node...
                                        self.__api.rotate_right() # Should be back at x
                                        self.__api.reset()
                                        break
                                elif sib[1] is "RED": # Case 4
                                        print("CASE4")
                                        print(self)
                                        self.color_sibling(self.parent_color())

                                        self.color_parent("BLACK")
                                        print("RECOLORED:")
                                        print(self)
                                        self.__api.move_parent()
                                        print(self)
                                        self.__api.move_left() # Move to the sibling
                                        self.__api.move_left() # move to the right[sib]
                                        print(self)
                                        
                                        self.__api.write_closure("color", "BLACK")
                                        print(self)
                                        print("right sibling of 6")
                                        self.__api.move_parent() # Move to sib
                                        self.__api.move_parent() # Move to parent
                                        print(self)
                                        self.__api.rotate_right()
                                        print(self)
                                        print("rotate of 6's parent")
                                        self.__api.reset()
                                        continue
                                        
                self.__api.write_closure("color", "BLACK")

# RB-DELETE-FIXUP(T, x)
# while x ≠ root[T] and color[x] = BLACK
#    do if x = left[p[x]]
#          then w ← right[p[x]]
#               if color[w] = RED
#                  then color[w] ← BLACK                        ▹  Case 1
#                       color[p[x]] ← RED                       ▹  Case 1
#                       LEFT-ROTATE(T, p[x])                    ▹  Case 1
#                       w ← right[p[x]]                         ▹  Case 1
#               if color[left[w]] = BLACK and color[right[w]] = BLACK
#                  then color[w] ← RED                          ▹  Case 2
#                       x p[x]                                  ▹  Case 2
#                  else if color[right[w]] = BLACK
#                          then color[left[w]] ← BLACK          ▹  Case 3
#                               color[w] ← RED                  ▹  Case 3
#                               RIGHT-ROTATE(T, w)              ▹  Case 3
#                               w ← right[p[x]]                 ▹  Case 3
#                        color[w] ← color[p[x]]                 ▹  Case 4
#                        color[p[x]] ← BLACK                    ▹  Case 4
#                        color[right[w]] ← BLACK                ▹  Case 4
#                        LEFT-ROTATE(T, p[x])                   ▹  Case 4
#                        x ← root[T]                            ▹  Case 4
#       else (same as then clause with "right" and "left" exchanged)
# color[x] ← BLACK

        def delete_cases(self, delete):
                # print("In delete cases")
                if delete and self.__api.get_count() >= 2:
                        self.__api.dec_count()
                        return
                if len(self.has_children()) is 2:
                        # Case 1
                        print("Case 1")
                        (v, count) = self.successor()
                        # print(self.__api.read_value())
                        # print(v)
                        # print(self)
                        self.__api.write_value(v)
                        self.__api.set_count(count)
                        # print(self)
                        self.__api.move_right()
                        return self.delete_help(v, False)
                if self.child_color("l") is "RED" or self.child_color("r") is "RED" or self.__api.read_closure("color") is "RED":
                        # Case 2 -- one child; only of child or self is red
                        print("Case 2 -- Delete: " + str(delete))
                        # print(self)
                        if delete and self.__api.get_count() <= 1:
                                self.__api.std_remove()
                                # print(self)
                                self.__api.write_closure("color", "BLACK")
                        elif delete:
                                self.__api.dec_count()
                                return
                        elif not delete:
                                self.__api.set_count(1)
                                self.__api.std_remove()

                else:
                        # Case 3.3
                        if self.__api.is_root() and self.__api.read_closure("color") is "DBLACK":
                                # print("Case 3.3")
                                self.__api.write_closure("color", "BLACK")
                                return
                        # Case 3 -- one child; both are black
                        print("Case 3")
                        # print(self)
                        if self.__api.get_count() <= 1: 
                                print("Std removed " + str(self.__api.read_value()))
                                self.__api.std_remove()
                        else:
                                print("dec_count")
                                self.__api.dec_count()
                                return
                        # Case 3.1
                        print("Case 3.1")
                        # print(self)
                        self.__api.write_closure("color", "DBLACK")
                        # Case 3.2 reduce DBLACK to BLACK
                        while self.__api.read_closure("color") is "DBLACK" and not self.__api.is_root():
                                print("Case 3.2")
                                if self.parent_color() is "RED":
                                        self.color_parent("BLACK")
                                        self.__api.write_closure("color", "BLACK")
                                # (a) is the sibling is black
                                sib = self.sibling_color()
                                if sib[0] is "BLACK" and (sib[1] is "RED" or sib[2] is "RED"):
                                        print("Case 3.2 a")
                                        print(self)
                                        # Left Left Case
                                        # Left Right Case
                                        # Right Right Case
                                        # Right Left Case
                                        case1 = self.__api.move_parent()
                                        self.__api.move(case1)
                                        self.__api.write_closure("color", "BLACK") # Color u
                                        if case1 is "r": # implies s is left child
                                                print(end="Left ")
                                                # Left left Case
                                                if sib[1] is "RED":
                                                        print("Left Case")
                                                        self.__api.move_grand_parent() # move to p

                                                        self.__api.rotate_right() # right rotate it

                                                        self.__api.move_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                # Left Right Case
                                                elif sib[2] is "RED":
                                                        print("Right Case")
                                                        print("------LEFT RIGHT CASE --------")
                                                        print(self)
                                                        print(" ===> Move Parent")
                                                        self.__api.move_parent()
                                                        print(self)
                                                        print(" ===> rot right")
                                                        self.__api.move_right()
                                                        print(self)
                                                        self.__api.rotate_left()
                                                        self.__api.write_closure("color", "BLACK")
                                                        self.__api.move_parent()
                                                        self.__api.rotate_left()
                                                        # print(self)
                                        else:
                                                # print(self)
                                                print(end="Right ")
                                                # Right Right Case
                                                if sib[2] is "RED":
                                                        print("Right Case")
                                                        print(self)
                                                        self.__api.move_parent()
                                                        
                                                        self.__api.rotate_left()

                                                        self.__api.move_right()
                                                        self.__api.write_closure("color", "BLACK")
                                                        print(self)
                                                #print("========== Moved Parent then LEFT =======")
                                                #print(self)
                                                #print("========== =======")
                                                # Right Left Case
                                                elif sib[1] is "RED":
                                                        print("Left Case")
                                                        print("------RIGHT LEFT CASE --------")
                                                        print(self)
                                                        print(" ===> Move Parent")
                                                        self.__api.move_parent()
                                                        print(self)
                                                        print(" ===> rot left")
                                                        self.__api.rotate_left()
                                                        print(self)
                                                        print(" ===> move left")
                                                        self.__api.move_left()
                                                        print(self)
                                                        print(" ===> write closure")
                                                        self.__api.write_closure("color", "RED")
                                                        print(self)
                                                        print(" ===> move parent")
                                                        self.__api.move_parent()
                                                        print(self)
                                                        print(" ===> rotate right")
                                                        self.__api.rotate_right()
                                                        print(self)

                                # (b) sibling and both children are black
                                elif sib[0] is "BLACK":
                                        print("3.2 (b)")
                                        self.__api.write_closure("color", "BLACK")
                                        m = self.__api.move_parent()
                                        c = self.__api.read_closure("color")
                                        self.__api.write_closure("color", "DBLACK" if c is "BLACK" else "BLACK")
                                        self.__api.move("l" if m is "r" else "r")
                                        self.__api.write_closure("color", "RED")
                                        self.__api.move_parent()
                                        continue
                                # (c) if sibling is red
                                else:
                                        print("3.2 c")
                                        if delete and self.__api.get_count() <= 1: 
                                                self.__api.std_remove()
                                        elif delete:
                                                self.__api.dec_count()
                                                return
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

        def verify_tree(self):
                return self.__api.verify_tree(True)
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
