from abc import ABC, abstractmethod

# AbstactBST defines the required methods for a particular BST
class AbstractBST(ABC):
        @abstractmethod
        def insert(self, value):
                pass

        @abstractmethod
        def delete(self, value):
                pass

        @abstractmethod
        def search(self, value):
                pass
