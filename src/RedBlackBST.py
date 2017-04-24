import AbstractBST
from api import API

class RedBlackBST(AbstractBST.AbstractBST):
        # RedBlackBST
        # api - an instance of the api class to modify the BST representation
        def __init__(self, api):
                super(RedBlackBST, self).__init__()
                self.__api = api

        # String casts to the printed BST with red black representation
        # TODO: Move the RedBlack part of the tree printing of the BST here
        # (there is no reason for the BST data model to know about the RBTree)
        # Maybe nodes could take a function that becomes their string cast?
        def __str__(self):
                return self.__api.__str__()
        
        # Insert the value into the tree
        def insert(self, value):
                self.__api.reset()
                self.insert_help(value)
                
        def insert_help(self, value):
                # Traverse the tree until we reach a leaf 
                # of we find an identical value
                while not self.__api.is_null():
                        if value < self.__api.read_value():
                                self.__api.move_left()
                        elif value > self.__api.read_value():
                                self.__api.move_right()
                        else:
                                self.__api.inc_count()
                                return

                # Insert the value s.t. the BST property holds
                self.__api.add(value)
                
                # Color it Red
                self.__api.write_closure("color", "RED")
                
                # Color the children "dummy nodes" black
                self.__api.move_left()
                self.__api.write_closure("color", "BLACK")
                self.__api.move_parent()

                self.__api.move_right()
                self.__api.write_closure("color", "BLACK")
                self.__api.move_parent()

                # Fix-up the RedBlack-Tree properties
                self.insert_fix()

        # Determine if a node has left or right children
        # returns a string containing "l" if the current node has a left child
        # and containing "r" if the current node has a right child
        def has_children(self):
                children = ""

                # Left Child
                self.__api.move_left()
                
                if not self.__api.is_null():
                        children += "l"
                
                self.__api.move_parent()

                # Right Child
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

        # Move to the successor
        def move_successor(self):
                self.__api.move_right()

                while not self.__api.is_null():
                        self.__api.move_left()

                self.__api.move_parent()

        # Returns the color of the left child or the right child
        def child_color(self, left_or_right):
                # Move to the child of choice
                if left_or_right is "l":
                        self.__api.move_left()
                else:
                        self.__api.move_right()

                # Grab the color
                color = self.__api.read_closure("color")
                
                # Move Back
                self.__api.move_parent()

                return color

        # Returns an array: 
        # [sibling_color, sibling's_left_child_color, sibling's_right_color_color]
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

        # Color the sibling with c
        def color_sibling(self, c):
                m = self.__api.move_parent()

                if m is "l":
                        self.__api.move_right()
                else:
                        self.__api.move_left()

                self.__api.write_closure("color", c)

                self.__api.move_parent()

                self.__api.move(m)
        
        # Return the color of the parent or None if the root
        def parent_color(self):
                m = self.__api.move_parent()

                if m is "":
                        return None

                parent_color = self.__api.read_closure("color")

                self.__api.move(m)

                return parent_color

        # Color the parent
        def color_parent(self, color):
                m = self.__api.move_parent()
                self.__api.write_closure("color", color)
                self.__api.move(m)
        
        # Get the color of the grandparent    
        def grand_parent_color(self):
                m = self.__api.move_grand_parent()

                if m is "":
                        return None

                grand_parent_color = self.__api.read_closure("color")
                self.__api.move(m)
                
                return grand_parent_color

        # Color the grandparent
        def color_grand_parent(self, color):
                m = self.__api.move_grand_parent()
                self.__api.write_closure("color", color)
                self.__api.move(m)
        
        # Get the color of the uncle
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

        # Returns true if current is a left child
        def is_left_child(self):
                l = self.__api.move_parent()
                self.__api.move(l)
                return l is "l"

        # Color the uncle with color
        def color_uncle(self, color):
                # Move to the grand-parent
                m = self.__api.move_grand_parent()
                # Move to the uncle
                self.__api.move("r" if m[0] == "l" else "l")
                uncle_color = self.__api.write_closure("color", color)
                self.__api.move_parent()
                self.__api.move(m)
        
        # insert-fix helper -
        # c is l or r for each case
        def repeat_case(self, c):

                self.__api.move_parent()
                self.__api.move_parent()

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

        # Fix RB-Tree properties after normal insertion                          
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
                                # Figure out which case we are in (ll, lr, rr, rl)
                                case = self.__api.move_grand_parent()
                                self.__api.move(case)

                                if case[0] == "l" and case[1] == "l":
                                        self.repeat_case("l")

                                elif case[0] == "l" and case[1] == "r":
                                        self.__api.move_parent()
                                        self.__api.rotate_left()
                                        self.__api.move_left()

                                        self.repeat_case("l")

                                elif case[0] == "r" and case[1] == "r":
                                        self.repeat_case("r")

                                elif case[0] == "r" and case[1] == "l":

                                        self.__api.move_parent()
                                        self.__api.rotate_right()
                                        self.__api.move_right()

                                        self.repeat_case("r")
                

        def delete(self, value):
                self.__api.reset()
                
                # return self.delete_help(value, True)

                return self.rb_delete(value)
                
        #def delete_help(self, value, delete):
        #        if self.__api.is_null():
        #                return False
        #        elif value < self.__api.read_value():
        #                self.__api.move_left()
        #        elif value > self.__api.read_value():
        #                self.__api.move_right()
        #        elif value == self.__api.read_value():
        #                # # print(value)
        #                return self.delete_cases(delete)
        #        return self.delete_help(value, delete)
        
        def rb_delete(self, value):
                found = self.__api.std_search(value)

                if not found:
                        return False

                sv = -1
                sc = -1

                if len(self.has_children()) is 2:
                        # Move the successor into place without changing color
                        (sv, sc) = self.successor()
                        self.__api.write_value(sv)
                        self.__api.set_count(sc)
                        # Move to it and...
                        self.move_successor()
                        # Prep for deletion
                        self.__api.set_count(1)
                
                # Grab the color for case analysis
                color = self.__api.read_closure("color")
                
                # Fully remove it from the tree
                suc = self.__api.std_remove(sv)

                # If it had no children then color it BLACK (In case it wasn't? it should be.)
                if self.__api.is_null(): self.__api.write_closure("color", "BLACK")
                
                # if the removed node was Red, Black heights haven't changed and we are done
                # if it was Black then black heights need fixing
                if color is "BLACK":
                        self.rb_delete_fixup()

                return suc

        def rb_delete_fixup(self):
                # Current node is considered to be colored Double Black 
                # (until it reaches a Red Node and loop terminates)
                while not self.__api.is_root() and self.__api.read_closure("color") is "BLACK":
                        # Current Node is left child of parent
                        if self.is_left_child():
                                # Grab sibling and children's color for 
                                # case analysis
                                sib = self.sibling_color()
                                # Sibling is RED
                                if sib[0] is "RED":
                                        self.color_sibling("BLACK")
                                        self.color_parent("RED")
                                        self.__api.move_parent()
                                        self.__api.rotate_left()
                                        self.__api.move_left()
                                        self.__api.move_left()
                                        continue
                                if sib[1] is "BLACK" and sib[2] is "BLACK":
                                        self.color_sibling("RED")

                                        self.__api.move_parent()

                                        if(self.__api.read_closure("color") is "RED"):
                                                # Red + Black = Black
                                                break

                                        continue
                                elif sib[1] is "RED" and sib[2] is "BLACK":
                                        self.__api.move_parent()
                                        self.__api.move_right() # Move to the sibling
                                        self.__api.move_left() # Move to the left child

                                        self.__api.write_closure("color", "BLACK") 
                                        
                                        self.__api.move_parent() # Move back to sibling
                                        self.__api.write_closure("color", "RED")
                                        
                                        self.__api.rotate_right() # Right rotate sibling
                                        
                                        self.__api.move_parent() # Moving back to the node...

                                        self.__api.rotate_left()
                                        # Done -- Reset to the root -- ends loop
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
                                        # Done! 
                                        self.__api.reset()
                                        continue
                        else:
                                # Right child case -- symmetric to Left Child Case
                                sib = self.sibling_color()

                                if sib[0] is "RED":
                                        self.color_sibling("BLACK")
                                        self.color_parent("RED")
                                        self.__api.move_parent()
                                        self.__api.rotate_right()
                                        self.__api.move_right()
                                        self.__api.move_right()
                                        continue
                                if sib[1] is "BLACK" and sib[2] is "BLACK":
                                        self.color_sibling("RED")

                                        self.__api.move_parent()
                                        if(self.__api.read_closure("color") is "RED"):
                                                break

                                        continue
                                elif sib[2] is "RED" and sib[1] is "BLACK":
                                        self.__api.move_parent()
                                        self.__api.move_left() # Move to the sibling

                                        self.__api.move_right() # Move to the right child
                                        self.__api.write_closure("color", "BLACK") 

                                        self.__api.move_parent() # Move back to sibling

                                        self.__api.write_closure("color", "RED")
                                        self.__api.rotate_left() # left rotate sibling
                                        self.__api.move_parent() # Moving back to the node...
                                        self.__api.rotate_right() # Should be back at x
                                        # Done!
                                        self.__api.reset()
                                        break
                                elif sib[1] is "RED": # Case 4
                                        self.color_sibling(self.parent_color())

                                        self.color_parent("BLACK")

                                        self.__api.move_parent()

                                        self.__api.move_left() # Move to the sibling
                                        self.__api.move_left() # move to the right[sib]
                                        
                                        self.__api.write_closure("color", "BLACK")

                                        self.__api.move_parent() # Move to sib
                                        self.__api.move_parent() # Move to parent

                                        self.__api.rotate_right()
                                        # Done!
                                        self.__api.reset()
                                        continue
                                        
                self.__api.write_closure("color", "BLACK")

        def search(self, value):
                self.__api.reset()
                return self.search_help(value)
        
        # Recursive Search of the Tree
        # TODO Make iterative
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

        # Verifies the RedBlack, and BST properties of the Tree through api
        # TODO: Move RedBlack tree Check Here
        def verify_tree(self):
                return self.__api.verify_tree(True)
