from utils import *
import copy
from collections import deque


class Dinic:
    def __init__(self, graph):
        self.graph = copy.deepcopy(graph)
        self._graph = copy.deepcopy(graph)
        self.length = len(graph)
        self.level = [-1] * self.length
        self.__init_graph()

    def __init_graph(self):
        _graph = []
        for i in range(self.length):
            _graph.append([])
            for j in range(self.length):
                _graph[i].append(-1)
        for i in range(self.length):
            for j in range(len(self.graph[i])):
                u, v, w = i, self.graph[i][j][0], self.graph[i][j][1]
                _graph[u][v] = w
        self.graph = _graph

    def bfs(self, s, t):
        visited = [False] * self.length
        queue = deque()
        queue.append(s)
        visited[s] = True
        self.level[s] = 0
        while queue:
            u = queue.popleft()
            for v in range(self.length):
                if visited[v] == False and self.graph[u][v] > 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
                    visited[v] = True
        return visited[t]

    def dfs(self, u, t, flow):
        if u == t:
            return flow
        for v, cap in enumerate(self.graph[u]):
            if self.level[v] == self.level[u] + 1 and cap > 0:
                d = self.dfs(v, t, min(flow, cap))
                if d > 0:
                    self.graph[u][v] -= d
                    self.graph[v][u] += d
                    return d
        return 0

    def max_flow(self, s, t):
        _max_flow = 0
        while self.bfs(s, t):
            while True:
                flow = self.dfs(s, t, float('inf'))
                if flow == 0:
                    break
                _max_flow += flow
        return _max_flow

    def find_paths(self):
        s = 0
        g = [[] for _ in range(self.length)]
        for u in range(self.length):
            for v, w in self._graph[u]:
                if self.graph[u][v] == 0 or w != 1 or u in [0, 1] or v in [0, 1]:
                    g[u].append((v, 0))
        # show_graph(g, model=self._graph)
        # exit()
        paths = []
        father = [-1] * self.length
        queue = deque()
        queue.append(s)
        final = []
        while queue:
            u = queue.popleft()
            for v, _ in g[u]:
                if v == 1:
                    if u not in final:
                        final.append(u)
                    continue
                father[v] = u
                queue.append(v)
        for u in final:
            cur = u
            path = []
            while cur != 0:
                path.append(cur)
                cur = father[cur]
            if len(path) > 1:
                path.reverse()
                paths.append(path)
        return paths

if __name__ == '__main__':
    import random

    random.seed(0)
    from data_generator import *
    from graph import *
    resources = generate_data()
    node_info, index, graph = graph_init(resources)
    dinic = Dinic(graph)
    max_flow = dinic.max_flow(0, 1)
    paths = dinic.find_paths()
    for i in range(10):
        print(paths[i])
    print(len(paths), max_flow)

    # show_graph(graph, paths=paths)

