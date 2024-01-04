def print_arangement(arange):
    ar = arange[2]
    shift = ar['shift']
    week = shift // 100
    day = shift % 100 // 3
    ti = shift // 100 % 3
    week_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ti_name = ['Morning', 'Afternoon', 'Night']
    print('\n================================================')
    print(f'TIME: {week}th WEEK, {week_name[day]}, {ti_name[ti]}')
    for ar in arange:
        if ar['category'] in ['super source', 'super sink']:
            continue
        if ar['duplicate_id'] != -1:
            continue
        print(f'{ar["category"]}: {ar["type"]}, ID: {ar["id"]}')
    print('================================================\n')


def show_graph(graph, model=None, paths=None):
    import networkx as nx
    import matplotlib.pyplot as plt
    from collections import deque

    G = nx.DiGraph()

    for u, edges in enumerate(graph):
        for v, capacity in edges:
            G.add_edge(u, v, capacity=capacity)

    def bfs_levels(graph, source):
        levels = {source: 0}
        queue = deque([source])

        while queue:
            u = queue.popleft()
            for v, capacity in graph[u]:
                if v not in levels:
                    levels[v] = levels[u] + 1
                    queue.append(v)
        return levels

    levels = bfs_levels(model if model is not None else graph, 0)  # Assuming 0 is the source node

    pos = {}
    for node, level in levels.items():
        nodes_in_level = [n for n in levels if levels[n] == level]
        level_width = len(nodes_in_level)
        for i, n in enumerate(sorted(nodes_in_level)):
            pos[n] = (level, (i - level_width / 2) * 1.0)

    # Draw the graph
    selected_edges = []
    if paths:
        for path in paths:
            for i in range(len(path) - 1):
                selected_edges.append((path[i], path[i + 1]))
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=20)
    default_edges = [edge for edge in G.edges() if edge not in selected_edges]
    nx.draw_networkx_edges(G, pos, edgelist=default_edges, edge_color='gray')
    nx.draw_networkx_edges(G, pos, edgelist=selected_edges, edge_color='red')
    nx.draw_networkx_labels(G, pos, font_size=10)
    plt.title('Layered Graph Representation')
    plt.show()


def save_arangement(aranges, path=r'C:\Users\chant\OneDrive\Courses\WOA7001 Advanced Algorithm\final\code\result.csv'):
    week_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ti_name = ['Morning', 'Afternoon', 'Night']
    import csv
    with open(path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        title = ['Week', 'Day', 'Time'] + ['ID', 'Type'] * 5
        writer.writerow(title)
        for arange in aranges:
            ar = arange[2]
            shift = ar['shift']
            week = shift // 100
            day = shift % 100 // 3
            ti = shift // 100 % 3
            row = [week + 1, week_name[day], ti_name[ti]]
            for ar in arange:
                if ar['category'] in ['super source', 'super sink']:
                    continue
                if ar['duplicate_id'] != -1:
                    continue
                row += [ar['id'], ar['type']]
            writer.writerow(row)
