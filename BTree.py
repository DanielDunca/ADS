class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.n = 0


class BTree:
    def __init__(self, t):
        self.t = t
        self.root = BTreeNode(leaf=True)

    def search(self, k, x=None):
        if x is None:
            x = self.root
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1
        if i < x.n and k == x.keys[i]:
            return (x, i)
        elif x.leaf:
            return None
        else:
            return self.search(k, x.children[i])

    def _split_child(self, x, i, y):
        t = self.t
        z = BTreeNode(leaf=y.leaf)
        z.n = t - 1

        for j in range(t - 1):
            z.keys.append(y.keys[j + t])

        if not y.leaf:
            for j in range(t):
                z.children.append(y.children[j + t])

        median = y.keys[t - 1]
        y.keys = y.keys[:t - 1]
        y.n = t - 1
        if not y.leaf:
            y.children = y.children[:t]

        x.children.insert(i + 1, z)
        x.keys.insert(i, median)
        x.n += 1

    def insert(self, k):
        r = self.root
        if r.n == 2 * self.t - 1:
            s = BTreeNode(leaf=False)
            self.root = s
            s.children.append(r)
            self._split_child(s, 0, r)
            self._insert_nonfull(s, k)
        else:
            self._insert_nonfull(r, k)

    def _insert_nonfull(self, x, k):
        i = x.n - 1
        if x.leaf:
            x.keys.append(None)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
            x.n += 1
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if x.children[i].n == 2 * self.t - 1:
                self._split_child(x, i, x.children[i])
                if k > x.keys[i]:
                    i += 1
            self._insert_nonfull(x.children[i], k)

    def delete(self, k, x=None):
        if x is None:
            x = self.root
        t = self.t
        i = 0
        while i < x.n and k > x.keys[i]:
            i += 1

        if i < x.n and x.keys[i] == k:
            if x.leaf:
                x.keys.pop(i)
                x.n -= 1
            else:
                y = x.children[i]
                z = x.children[i + 1]
                if y.n >= t:
                    k_prime = self._get_predecessor(y)
                    x.keys[i] = k_prime
                    self.delete(k_prime, y)
                elif z.n >= t:
                    k_prime = self._get_successor(z)
                    x.keys[i] = k_prime
                    self.delete(k_prime, z)
                else:
                    self._merge(x, i)
                    self.delete(k, x.children[i])
        else:
            if x.leaf:
                return
            child = x.children[i]
            if child.n == t - 1:
                if i > 0 and x.children[i - 1].n >= t:
                    self._borrow_from_left(x, i)
                elif i < x.n and x.children[i + 1].n >= t:
                    self._borrow_from_right(x, i)
                else:
                    if i < x.n:
                        self._merge(x, i)
                    else:
                        self._merge(x, i - 1)
                        i -= 1
                    if x == self.root and x.n == 0:
                        self.root = x.children[0]
                child = x.children[i]
            self.delete(k, child)

    def _get_predecessor(self, x):
        while not x.leaf:
            x = x.children[x.n]
        return x.keys[x.n - 1]

    def _get_successor(self, x):
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]

    def _merge(self, x, i):
        t = self.t
        y = x.children[i]
        z = x.children[i + 1]
        y.keys.append(x.keys[i])
        y.keys.extend(z.keys)
        if not y.leaf:
            y.children.extend(z.children)
        y.n = 2 * t - 1
        x.keys.pop(i)
        x.children.pop(i + 1)
        x.n -= 1

    def _borrow_from_left(self, x, i):
        child = x.children[i]
        sibling = x.children[i - 1]
        child.keys.insert(0, x.keys[i - 1])
        child.n += 1
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        x.keys[i - 1] = sibling.keys.pop()
        sibling.n -= 1

    def _borrow_from_right(self, x, i):
        child = x.children[i]
        sibling = x.children[i + 1]
        child.keys.append(x.keys[i])
        child.n += 1
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        x.keys[i] = sibling.keys.pop(0)
        sibling.n -= 1

    def inorder(self, x=None):
        if x is None:
            x = self.root
        result = []
        for i in range(x.n):
            if not x.leaf:
                result.extend(self.inorder(x.children[i]))
            result.append(x.keys[i])
        if not x.leaf:
            result.extend(self.inorder(x.children[x.n]))
        return result

    def minimum(self):
        if self.root.n == 0:
            return None
        x = self.root
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]

    def maximum(self):
        if self.root.n == 0:
            return None
        x = self.root
        while not x.leaf:
            x = x.children[x.n]
        return x.keys[x.n - 1]


# In order to run this program, first create a B-Tree object with minimum degree t:

# tree = BTree(t)
# Creates a B-Tree with minimum degree t (each non-root node has >= t-1 and <= 2t-1 keys).

# tree.insert(data)
# Inserts a new key into the B-Tree.

# print(tree.search(data))
# Searches for a key in the tree; returns (node, index) if found, None otherwise.

# print("Min:", tree.minimum())
# Prints the smallest key in the tree.

# print("Max:", tree.maximum())
# Prints the largest key in the tree.

# print("Inorder:", tree.inorder())
# Prints all keys in sorted order.

# tree.delete(data)
# Deletes the key from the B-Tree.
