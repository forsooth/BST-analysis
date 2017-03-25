import AbstractBST


class ExampleBST(AbstractBST.AbstractBST):
        # ExampleBST — example of a concrete implementation of AbstractBST
        def __init__(self):
                super(ExampleBST, self).__init__()

        def insert(self, value):
                print("Inserted " + str(value))

        def delete(self, value):
                print("Deleted " + str(value))

        def search(self, value):
                print("Found " + str(value))

x = ExampleBST()
