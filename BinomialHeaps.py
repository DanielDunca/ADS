class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    @staticmethod
    def _link_trees(y, z):
        y.parent = z
        y.sibling = z.child
        z.child = y
        z.degree += 1

    @staticmethod
    def _merge_root_lists(h1, h2):
        if h1 is None:
            return h2
        if h2 is None:
            return h1

        if h1.degree <= h2.degree:
            head = h1
            h1 = h1.sibling
        else:
            head = h2
            h2 = h2.sibling

        tail = head
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling = h1
                h1 = h1.sibling
            else:
                tail.sibling = h2
                h2 = h2.sibling
            tail = tail.sibling

        tail.sibling = h1 if h1 else h2
        return head

    def union(self, other_heap):
        self.head = self._merge_root_lists(self.head, other_heap.head)
        other_heap.head = None

        if self.head is None:
            return

        prev = None
        curr = self.head
        next_node = curr.sibling

        while next_node:
            same_degree = curr.degree == next_node.degree
            next_has_same_degree = (
                next_node.sibling is not None
                and next_node.sibling.degree == curr.degree
            )

            if not same_degree or next_has_same_degree:
                prev = curr
                curr = next_node
            else:
                if curr.key <= next_node.key:
                    curr.sibling = next_node.sibling
                    self._link_trees(next_node, curr)
                else:
                    if prev is None:
                        self.head = next_node
                    else:
                        prev.sibling = next_node
                    self._link_trees(curr, next_node)
                    curr = next_node
            next_node = curr.sibling

    def insert(self, key):
        new_heap = BinomialHeap()
        new_heap.head = BinomialNode(key)
        self.union(new_heap)

    def is_empty(self):
        return self.head is None

    def minimum(self):
        if self.head is None:
            return None

        min_key = self.head.key
        current = self.head.sibling

        while current:
            if current.key < min_key:
                min_key = current.key
            current = current.sibling

        return min_key

    def _find_min_root(self):
        min_prev = None
        min_node = self.head

        prev = self.head
        current = self.head.sibling

        while current:
            if current.key < min_node.key:
                min_node = current
                min_prev = prev
            prev = current
            current = current.sibling

        return min_prev, min_node

    def extract_min(self):
        if self.head is None:
            return None

        min_prev, min_node = self._find_min_root()

        if min_prev is None:
            self.head = min_node.sibling
        else:
            min_prev.sibling = min_node.sibling

        child = min_node.child
        reversed_children = None

        while child:
            next_child = child.sibling
            child.sibling = reversed_children
            child.parent = None
            reversed_children = child
            child = next_child

        new_heap = BinomialHeap()
        new_heap.head = reversed_children
        self.union(new_heap)

        return min_node.key

    def _search_tree(self, node, key):
        current = node

        while current:
            if current.key == key:
                return current

            found = self._search_tree(current.child, key)
            if found:
                return found

            current = current.sibling

        return None

    def search(self, key):
        return self._search_tree(self.head, key)

    def decrease_key(self, key, new_key):
        node = self.search(key)

        if node is None:
            return False

        if new_key > node.key:
            return False

        node.key = new_key
        current = node
        parent = current.parent

        while parent and current.key < parent.key:
            current.key, parent.key = parent.key, current.key
            current = parent
            parent = current.parent

        return True

    def delete(self, key):
        node = self.search(key)
        if node is None:
            return False

        while node.parent:
            node.key, node.parent.key = node.parent.key, node.key
            node = node.parent

        prev = None
        current = self.head

        while current and current != node:
            prev = current
            current = current.sibling

        if current is None:
            return False

        if prev is None:
            self.head = current.sibling
        else:
            prev.sibling = current.sibling

        child = current.child
        reversed_children = None

        while child:
            next_child = child.sibling
            child.sibling = reversed_children
            child.parent = None
            reversed_children = child
            child = next_child

        new_heap = BinomialHeap()
        new_heap.head = reversed_children
        self.union(new_heap)

        return True

    def maximum(self):
        if self.head is None:
            return None

        max_key = None
        stack = [self.head]

        while stack:
            node = stack.pop()

            while node:
                if max_key is None or node.key > max_key:
                    max_key = node.key
                if node.child:
                    stack.append(node.child)
                node = node.sibling

        return max_key


# In order to run this project, first you have to create the object:

# heap = BinomialHeap()

# heap.insert(data) inserts the data into the binomial heap

# print("Search data:", heap.search(data)) heap.search(data) searches for the data in the heap
# print("Min:", heap.minimum()) prints the minimum
# print("Max:", heap.maximum()) prints the maximum

# print("Extract min:", heap.extract_min()) removes and returns the minimum

# heap.decrease_key(old_data, new_data) decreases a key value

# heap.delete(data) deletes the data from the heap
