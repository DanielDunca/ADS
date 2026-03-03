class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        current = self.root
        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left
            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right
            else:
                return

    def search(self, value):
        current = self.root

        while current:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return False


    # -------- MINIMUM --------
    def minimum(self):
        current = self.root
        if current is None:
            return None

        while current.left:
            current = current.left

        return current.value

    def maximum(self):
        current = self.root
        if current is None:
            return None

        while current.right:
            current = current.right

        return current.value

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)

        elif value > node.value:
            node.right = self._delete(node.right, value)

        else:
            if node.left is None and node.right is None:
                return None

            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            temp = node.right
            while temp.left:
                temp = temp.left

            node.value = temp.value
            node.right = self._delete(node.right, temp.value)

        return node


#In order to run this project, first you have to create the object:

#tree = BST()

#tree.insert(data) tree.insert(data) inserts the data into the tree

#print("Search data:", tree.search(data)) tree.search(data) searches for the data in the tree
#print("Min:", tree.minimum()) prints the minimum
#print("Max:", tree.maximum()) prints the maximum

#tree.delete(data) tree.delete(data) deletes the  data from the tree
