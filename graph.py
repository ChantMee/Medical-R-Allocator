from config import *
from utils import print_arangement

# generate graph
graph = None
node_info = []
index = {}
CUR_NODE_ID = 2
SOURCE_ID = 0
SINK_ID = 1
node_info.append({
    'node_id': 0,
    'category': 'super source',
    'dependency_category': 'illness',
    'dependency_type': illness_name,
})
node_info.append({
    'node_id': 1,
    'category': 'super sink',
    'dependency_category': 'NO DEPENDENCY'
})


def build_graph(cur):
    if node_info[cur]['dependency_category'] == 'END':
        graph[cur].append((node_info[cur]['duplicate_id'], node_info[cur]['flow']))
        assert cur == node_info[cur]['duplicate_id'] + 1 or cur < node_info[cur]['duplicate_id']
        graph[node_info[cur]['duplicate_id']].append((SINK_ID, node_info[cur]['flow']))
        return
    if len(graph[cur]) > 0:
        # is the super sink
        if node_info[cur]['category'] == 'super source' or node_info[cur]['category'] == first_class:
            for v in graph[cur]:
                build_graph(v[0])
            return
        # is not the duplicated node, just find the duplicated node
        elif node_info[cur]['duplicate_id'] != -1:
            build_graph(graph[cur][0][0])
            return
        else:
            return
    shift = node_info[cur]['shift']
    for v in index[shift]:
        con1 = node_info[v]['category'] == node_info[cur]['dependency_category']
        con2 = node_info[v]['type'] in node_info[cur]['dependency_type']
        con3 = node_info[v]['duplicate_id'] != -1
        if con1 and con2 and con3:
            graph[cur].append((v, node_info[cur]['flow']))
            assert cur == v + 1 or cur < v
            graph[v].append((node_info[v]['duplicate_id'], node_info[v]['flow']))
            assert v == node_info[v]['duplicate_id'] + 1 or v < node_info[v]['duplicate_id']
            build_graph(v)


def graph_init(resource):
    global node_info, CUR_NODE_ID, SOURCE_ID, SINK_ID, index, graph
    for category, resources in resource.items():
        if category == first_class:
            for resource in resources:
                dependency_category = dependency['category'][category]
                type_name = id2name[category][resource['type']]
                dependency_type = dependency[category][type_name]
                node_info.append({
                    'node_id': CUR_NODE_ID,
                    'category': category,
                    'type': type_name,
                    'id': resource['id'],
                    'flow': resource['flow'],
                    'shift': -1,
                    'duplicate_id': -1,
                    'dependency_category': dependency_category,
                    'dependency_type': dependency_type,
                })
                CUR_NODE_ID += 1
                node_info.append(node_info[-1].copy())
                node_info[-1]['node_id'] = CUR_NODE_ID
                CUR_NODE_ID += 1
                node_info[-1]['duplicate_id'] = CUR_NODE_ID - 2
                if -1 not in index:
                    index[-1] = []
                index[-1].append(CUR_NODE_ID - 1)
            continue
        for week in range(TOT_WEEKS):
            for resource in resources:
                for shift in resource['available_shift']:
                    dependency_category = dependency['category'][category]
                    type_name = id2name[category][resource['type']]
                    dependency_type = dependency[category][type_name]
                    node_info.append({
                        'node_id': CUR_NODE_ID,
                        'category': category,
                        'type': type_name,
                        'id': resource['id'],
                        'flow': resource['flow'],
                        'shift': shift + 100 * week,
                        'duplicate_id': -1,
                        'dependency_category': dependency_category,
                        'dependency_type': dependency_type,
                    })
                    CUR_NODE_ID += 1
                    node_info.append(node_info[-1].copy())
                    node_info[-1]['node_id'] = CUR_NODE_ID
                    CUR_NODE_ID += 1
                    node_info[-1]['duplicate_id'] = CUR_NODE_ID - 2
                    if shift + 100 * week not in index:
                        index[shift + 100 * week] = []
                    index[shift + 100 * week].append(CUR_NODE_ID - 1)

    graph = [[] for _ in range(len(node_info))]

    for node in node_info:
        if node['category'] == first_class and node['duplicate_id'] != -1:
            u, v = node['node_id'], node['duplicate_id']
            graph[SOURCE_ID].append((u, float('inf')))
            assert SOURCE_ID == u + 1 or SOURCE_ID < u
            graph[u].append((v, node['flow']))
            assert u == v + 1 or u < v

    for first_class_node in index[-1]:
        u = node_info[first_class_node]['duplicate_id']
        dependency_category = node_info[first_class_node]['dependency_category']
        dependency_type = node_info[first_class_node]['dependency_type']
        for i in range(len(node_info)):
            if node_info[i]['category'] == dependency_category and node_info[i]['type'] in dependency_type and \
                    node_info[i][
                        'duplicate_id'] != -1:
                v, dv = node_info[i]['node_id'], node_info[i]['duplicate_id']
                graph[u].append((v, node_info[u]['flow']))
                assert u == v + 1 or u < v
                graph[v].append((dv, node_info[v]['flow']))
                assert v == dv + 1 or v < dv
    build_graph(SOURCE_ID)
    return node_info, index, graph

# print abstract of graph
def print_graph_abstract(graph, node_info):
    NUM_EDGE = 0
    for i in range(len(graph)):
        NUM_EDGE += len(graph[i])
    print('\n================================================')
    print(f'number of nodes: {len(node_info)}')
    print(f'number of edges: {NUM_EDGE}')
    print('================================================\n')

    # calculate the number of edges of each category
    NUM_EDGE_CATEGORY = {
        'illness': 0,
        'operator': 0,
        'room': 0,
        'anesthesiologist': 0,
        'nurse': 0,
    }
    for i in range(len(graph)):
        if node_info[i]['category'] == 'super source' or node_info[i]['category'] == 'super sink':
            continue
        NUM_EDGE_CATEGORY[node_info[i]['category']] += len(graph[i])
    print('\n================================================')
    for category, num in NUM_EDGE_CATEGORY.items():
        print(f'number of edges of {category}: {num}')
    print('================================================\n')


queue = []
MAX_DEPTH = 0


def check_conn(cur, dep=0, first=True):
    global MAX_DEPTH, queue
    if first:
        queue = []
        first = False
    dep = dep + 1
    if dep > MAX_DEPTH:
        MAX_DEPTH = dep
        print('\n================================================')
        for i in queue:
            print(i)
        print('================================================\n')
    if node_info[cur]['category'] == 'super sink':
        print_arangement(queue)
        exit()
    for v in graph[cur]:
        queue.append(node_info[v[0]])
        check_conn(v[0], dep + 1, first)
        queue.pop()
    dep = dep - 1
