from abc import ABC, abstractmethod

class AbstractBST(ABC):
        """
        AbstactBST defines the required methods for a particular BST
        """
        @abstractmethod 
        def insert(self, value):
                pass
        @abstractmethod 
        def delete(self, value):
                pass
        @abstractmethod 
        def search(self, value):
                pass