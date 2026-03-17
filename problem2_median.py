from RBT import RBTree


class MedianFinder:
    def __init__(self):
        self.tree = RBTree()
        self.count = 0

    def add(self, x):
        self.tree.insert(x)
        self.count += 1

    def remove(self, x):
        self.tree.delete(x)
        self.count -= 1

    def median(self):
        if self.count == 0:
            return None
        target = (self.count - 1) // 2
        result = []
        self._inorder_until(self.tree.root, result, target)
        return result[target]

    def _inorder_until(self, node, result, target):
        if node == self.tree.NIL or len(result) > target:
            return
        self._inorder_until(node.left, result, target)
        if len(result) <= target:
            result.append(node.key)
            self._inorder_until(node.right, result, target)


def process(operations):
    finder = MedianFinder()
    for op in operations:
        parts = op.split()
        if parts[0] == "ADD":
            finder.add(int(parts[1]))
        elif parts[0] == "REMOVE":
            finder.remove(int(parts[1]))
        elif parts[0] == "MEDIAN":
            print(finder.median())


# In order to run this program, first create a MedianFinder object:

# finder = MedianFinder()

# finder.add(5)
# Inserts the number 5 into the data stream.

# finder.remove(5)
# Removes one occurrence of 5 from the data stream.

# finder.median()
# Returns the current median. If the count is odd, returns the middle element.
# If the count is even, returns the lower of the two middle elements.

# process([])
# Processes a list of string operations ("ADD x", "REMOVE x", "MEDIAN")
# and prints MEDIAN results.

# Example (matches expected output):
# process([
#     "ADD 5",
#     "ADD 2",
#     "ADD 10",
#     "MEDIAN",
#     "ADD 7",
#     "MEDIAN",
#     "REMOVE 5",
#     "MEDIAN",
# ])