




class BinaryTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.left = None
        self.right = None
        self.content = None


def buildTree(arr):
    length = len(arr)
    if length == 0:
        return None

    for i in range(length):
        node = BinaryTree()
        node.root = arr[i]
        node.size = i + 1