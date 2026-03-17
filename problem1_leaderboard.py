from RBT import RBTree


class Leaderboard:
    def __init__(self):
        self.tree = RBTree()
        self.players = {}

    def add(self, player, score):
        self.players[player] = score
        self.tree.insert((score, player))

    def update(self, player, delta):
        scor_vec = self.players[player]
        self.tree.delete((scor_vec, player))
        scor_nou = scor_vec + delta
        self.players[player] = scor_nou
        self.tree.insert((scor_nou, player))

    def remove(self, player):
        score = self.players.pop(player)
        self.tree.delete((score, player))

    def top(self, k):
        result = []
        self._reverse_inorder(self.tree.root, result, k)
        return result

    def _reverse_inorder(self, node, result, k):
        if node == self.tree.NIL or len(result) >= k:
            return
        self._reverse_inorder(node.right, result, k)
        if len(result) < k:
            result.append((node.key[1], node.key[0]))
            self._reverse_inorder(node.left, result, k)


def process(operations):
    board = Leaderboard()
    for op in operations:
        parts = op.split()
        if parts[0] == "ADD":
            board.add(parts[1], int(parts[2]))
        elif parts[0] == "UPDATE":
            board.update(parts[1], int(parts[2]))
        elif parts[0] == "REMOVE":
            board.remove(parts[1])
        elif parts[0] == "TOP":
            for player, score in board.top(int(parts[1])):
                print(player, score)


# In order to run this program, first create a Leaderboard object:

# board = Leaderboard()

# board.add("Alex", 120)
# Adds a new player "Alex" with score 120.

# board.update("Bob", 50)
# Increases (or decreases if negative) Bob's score by 50.

# board.remove("Carol")
# Removes Carol from the leaderboard.

# board.top(2)
# Returns a list of the top 2 players as (player, score) tuples, highest first.

# process([])
# Processes a list of string operations ("ADD", "UPDATE", "REMOVE", "TOP k")
# and prints TOP results.

# Example (matches expected output):
# process([
#     "ADD Alice 120",
#     "ADD Bob 90",
#     "ADD Carol 150",
#     "UPDATE Bob 50",
#     "TOP 2",
#     "REMOVE Carol",
#     "TOP 2",
# ])
