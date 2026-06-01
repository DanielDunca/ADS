class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find_set(self, x):
        if x != self.parent[x]:
            self.parent[x] = self.find_set(self.parent[x])
        return self.parent[x]

    def _link(self, x, y):
        if self.rank[x] > self.rank[y]:
            self.parent[y] = x
        else:
            self.parent[x] = y
            if self.rank[x] == self.rank[y]:
                self.rank[y] += 1

    def union(self, x, y):
        self._link(self.find_set(x), self.find_set(y))


class ConnectedComponents:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        self.ds = DisjointSets(n)

    def count(self):
        for u, v in self.edges:
            if self.ds.find_set(u) != self.ds.find_set(v):
                self.ds.union(u, v)
        roots = {self.ds.find_set(i) for i in range(self.n)}
        return len(roots)


class CycleDetection:
    def __init__(self, n, edges):
        self.n = n
        self.edges = edges
        self.ds = DisjointSets(n)

    def has_cycle(self):
        for u, v in self.edges:
            if self.ds.find_set(u) == self.ds.find_set(v):
                return True
            self.ds.union(u, v)
        return False


class Provinces:
    def __init__(self, is_connected):
        self.is_connected = is_connected
        self.n = len(is_connected)
        self.ds = DisjointSets(self.n)

    def count(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.is_connected[i][j] == 1:
                    if self.ds.find_set(i) != self.ds.find_set(j):
                        self.ds.union(i, j)
        roots = {self.ds.find_set(i) for i in range(self.n)}
        return len(roots)


class SocialNetwork:
    def __init__(self, n, friendships):
        self.n = n
        self.friendships = friendships
        self.ds = DisjointSets(n)

    def process(self):
        for u, v in self.friendships:
            self.ds.union(u, v)

    def get_groups(self):
        self.process()
        groups = {}
        for i in range(self.n):
            root = self.ds.find_set(i)
            if root not in groups:
                groups[root] = []
            groups[root].append(i)
        return list(groups.values())

    def summary(self):
        groups = self.get_groups()
        print(f"{len(groups)} Groups")
        for idx, members in enumerate(groups, 1):
            print(f"Group {idx}: {set(members)} size {len(members)}")


#  Problem 1: Connected Components
# cc = ConnectedComponents(n=5, edges=[(0,1),(1,2),(3,4)])
# print("Connected components:", cc.count())
# Expected: 2  ({0,1,2} and {3,4})

#  Problem 2: Cycle Detection
# cd = CycleDetection(n=4, edges=[(0,1),(1,2),(2,0)])
# print("Has cycle:", cd.has_cycle())
# Expected: True

# cd2 = CycleDetection(n=4, edges=[(0,1),(1,2),(2,3)])
# print("Has cycle:", cd2.has_cycle())
# Expected: False

# Problem 3: Number of Provinces
# matrix = [
#     [1, 1, 0],
#     [1, 1, 0],
#     [0, 0, 1]
# ]
# prov = Provinces(matrix)
# print("Provinces:", prov.count())
# Expected: 2

# Problem 4: Social Network Friend Groups
# net = SocialNetwork(n=7, friendships=[(0,1),(1,2),(3,4),(5,6)])
# net.summary()
# Expected:
# 3 Groups
# Group 1: {0,1,2} size 3
# Group 2: {3,4} size 2
# Group 3: {5,6} size 2
