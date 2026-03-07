class Node:
    def __init__(self, key, color="RED"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    def __init__(self):
        self.NIL = Node(None, "BLACK")
        self.root = self.NIL

    def search(self, key):
        current = self.root
        while current != self.NIL and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def minimum(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return None
        while node.left != self.NIL:
            node = node.left
        return node

    def maximum(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return None
        while node.right != self.NIL:
            node = node.right
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def insert(self, key):
        new_node = Node(key, "RED")
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        if new_node.parent is None:
            new_node.color = "BLACK"
            return

        if new_node.parent.parent is None:
            return

        self.fix_insert(new_node)

    def fix_insert(self, node):
        while node.parent and node.parent.color == "RED":
            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left
                if uncle.color == "RED":
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.left_rotate(node.parent.parent)
            else:
                uncle = node.parent.parent.right
                if uncle.color == "RED":
                    uncle.color = "BLACK"
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.color = "BLACK"
                    node.parent.parent.color = "RED"
                    self.right_rotate(node.parent.parent)

            if node == self.root:
                break

        self.root.color = "BLACK"

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.search(key)
        if z == self.NIL:
            return False  # key not found

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)

        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)

        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == "BLACK":
            self.fix_delete(x)

        return True

    def fix_delete(self, x):
        while x != self.root and x.color == "BLACK":
            if x == x.parent.left:
                s = x.parent.right

                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == "BLACK" and s.right.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.right.color == "BLACK":
                        s.left.color = "BLACK"
                        s.color = "RED"
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.right.color = "BLACK"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left

                if s.color == "RED":
                    s.color = "BLACK"
                    x.parent.color = "RED"
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == "BLACK" and s.left.color == "BLACK":
                    s.color = "RED"
                    x = x.parent
                else:
                    if s.left.color == "BLACK":
                        s.right.color = "BLACK"
                        s.color = "RED"
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = "BLACK"
                    s.left.color = "BLACK"
                    self.right_rotate(x.parent)
                    x = self.root

        x.color = "BLACK"

    def inorder(self, node=None):
        if node is None:
            node = self.root
        if node == self.NIL:
            return []
        return self.inorder(node.left) + [f"{node.key}({node.color})"] + self.inorder(node.right)

# In order to run this program, first create a Red-Black Tree object:

# tree = RBTree()

# tree.insert(data)
# Inserts a new node with the given value into the Red-Black Tree.

# print(tree.search(data))
# Searches for a value in the tree and returns the node if it exists.

# print("Min:", tree.minimum().key)
# Prints the smallest value in the tree.

# print("Max:", tree.maximum().key)
# Prints the largest value in the tree.

# tree.delete(data)
# Deletes the node with the given value from the tree.