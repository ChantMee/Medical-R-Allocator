import time
import random

# config
range_patient = (75, 100)
range_operator = (12, 16)
range_anesthesiologist = (6, 10)
range_room = (6, 10)
range_nurse = (10, 13)

available_rate_patient = 1
available_rate_operator = 0.3
available_rate_anesthesiologist = 0.3
available_rate_room = 0.4
available_rate_nurse = 0.3

max_flow = {
    'illness': 1,
    'operator': 1,
    'room': 1,
    'anesthesiologist': 1,
    'nurse': 5,
}

# resource category
illness_name = [
    'Coronary Artery Bypass Graft',
    'Valve Replacement',
    'Brain Tumor Removal',
    'Spinal Fusion',
    'Joint Replacement',
    'Fracture Repair',
    'Heart Defect Repair',
    'Inguinal Hernia Repair',
    'Gallbladder Removal',
    'Appendectomy',
]
illness_name2id = {name: id for id, name in enumerate(illness_name)}

operator_category = [
    'Cardiology', 
    'Neurology', 
    'Orthopedics', 
    'Pediatrics', 
    'Surgery', 
]
operator_category2id = {name: id for id, name in enumerate(operator_category)}

room_category = [
    'Surgical Room',
    'Pediatrics',
]
room_category2id = {name: id for id, name in enumerate(room_category)}

anesthesiologist_category = [
    'Anesthesiologist', 
]
anesthesiologist_category2id = {name: id for id, name in enumerate(anesthesiologist_category)}

nurse_category = [
    'Nurse',
]
nurse_category2id = {name: id for id, name in enumerate(nurse_category)}

## merge category
id2name = {
    'illness': illness_name,
    'operator': operator_category,
    'room': room_category,
    'anesthesiologist': anesthesiologist_category,
    'nurse': nurse_category,
}
name2id = {
    'illness': illness_name2id,
    'operator': operator_category2id,
    'room': room_category2id,
    'anesthesiologist': anesthesiologist_category2id,
    'nurse': nurse_category2id,
}































# dependency
resource_category_dependency = {
    'illness': 'operator',
    'operator': 'room',
    'room': 'anesthesiologist',
    'anesthesiologist': 'nurse',
    'nurse': 'END',
}

dependency_illness = {
    'Coronary Artery Bypass Graft': ['Cardiology'],
    'Valve Replacement': ['Cardiology'],
    'Brain Tumor Removal': ['Neurology'],
    'Spinal Fusion': ['Neurology', 'Orthopedics'],
    'Joint Replacement': ['Orthopedics'],
    'Fracture Repair': ['Orthopedics'],
    'Heart Defect Repair': ['Pediatrics'],
    'Inguinal Hernia Repair': ['Pediatrics'],
    'Gallbladder Removal': ['Surgery'],
    'Appendectomy': ['Surgery'],
}

dependency_operator = {
    'Cardiology': ['Surgical Room'],
    'Neurology': ['Surgical Room'],
    'Orthopedics': ['Surgical Room'],
    'Pediatrics': ['Pediatrics'],
    'Surgery': ['Surgical Room'],
}

dependency_room = {
    'Surgical Room': ['Anesthesiologist'],
    'Pediatrics': ['Anesthesiologist'],
}

dependency_anesthesiologist = {
    'Anesthesiologist': ['Nurse'],
}

dependency_nurse = {
    'Nurse': ['END'],
}

def transform_to_id(dependency, name):
    dependency_id = dict()
    for key, deps in dependency.items():
        key_id = name2id[name][key]
        deps_id = [name2id[resource_category_dependency[name]][dep] if dep != 'END' else -1 for dep in deps]
        dependency_id[key_id] = deps_id
    return dependency_id

# transform to id
dependency_illness_id = transform_to_id(dependency_illness, 'illness')
dependency_operator_id = transform_to_id(dependency_operator, 'operator')
dependency_room_id = transform_to_id(dependency_room, 'room')
dependency_anesthesiologist_id = transform_to_id(dependency_anesthesiologist, 'anesthesiologist')
dependency_nurse_id = transform_to_id(dependency_nurse, 'nurse')

# merge dependency
dependency = {
    'category': resource_category_dependency,
    'illness': dependency_illness,
    'operator': dependency_operator,
    'room': dependency_room,
    'anesthesiologist': dependency_anesthesiologist,
    'nurse': dependency_nurse,
}





























#generate data

def generate_info(id, type_range, flow, available_rate):
    info = {
        'id': id,
        'type': random.randint(type_range[0], type_range[1]),
        'flow': flow,
        'available_shift': [],
    }
    for j in range(21):
        if random.random() < available_rate:
            info['available_shift'].append(j)
    return info

patients = []
for i in range(random.randint(range_patient[0], range_patient[1])):
    patients.append(generate_info(i, (0, len(illness_name) - 1), max_flow['illness'], available_rate_patient))

operators = []
for i in range(random.randint(range_operator[0], range_operator[1])):
    operators.append(generate_info(i, (0, len(operator_category) - 1), max_flow['operator'], available_rate_operator))

rooms = []
for i in range(random.randint(range_room[0], range_room[1])):
    rooms.append(generate_info(i, (0, len(room_category) - 1), max_flow['room'], available_rate_room))

anesthetists = []
for i in range(random.randint(range_anesthesiologist[0], range_anesthesiologist[1])):
    anesthetists.append(generate_info(i, (0, len(anesthesiologist_category) - 1), max_flow['anesthesiologist'], available_rate_anesthesiologist))

nurses = []
for i in range(random.randint(range_nurse[0], range_nurse[1])):
    nurses.append(generate_info(i, (0, len(nurse_category) - 1), max_flow['nurse'], available_rate_nurse))

# merge data
resource = {
    'illness': patients,
    'operator': operators,
    'room': rooms,
    'anesthesiologist': anesthetists,
    'nurse': nurses,
}

# calculate n_patient:n_operator:n_room:n_anesthetist:n_nurse
def calculate_max_serving_flow(resource):
    max_serving_flow = 0
    for i in range(len(resource)):
        max_serving_flow += resource[i]['available_shift'].count(0) * resource[i]['flow']
    return max_serving_flow

for category, resources in resource.items():
    if category == 'illness':
        print(f'patient: \t{len(patients)}')
        continue
    print(f'{category}: \t{len(resources)}')






































# generate graph
node_info = []
CUR_NODE_ID = 2
TOT_WEEKS = 5
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

index = {}

for category, resources in resource.items():
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
print(f'number of nodes: {len(node_info)}')

graph = [[] for _ in range(len(node_info))]
for node in node_info:
    if node['category'] == 'illness' and node['duplicate_id'] != -1:
        u, v = node['node_id'], node['duplicate_id']
        graph[SOURCE_ID].append((u, float('inf')))
        graph[u].append((v, node['flow']))

def build_graph(cur):
    if node_info[cur]['dependency_category'] == 'END':
        graph[cur].append((node_info[cur]['duplicate_id'], node_info[cur]['flow']))
        graph[node_info[cur]['duplicate_id']].append((SINK_ID, node_info[cur]['flow']))
        return
    if len(graph[cur]) > 0:
        # is the super sink
        if node_info[cur]['category'] == 'super source':
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
            graph[v].append((node_info[v]['duplicate_id'], node_info[v]['flow']))
            build_graph(v)

build_graph(SOURCE_ID)

NUM_EDGE = 0
for i in range(len(graph)):
    NUM_EDGE += len(graph[i])
print(f'number of edges: {NUM_EDGE}')


def print_arangement(arange):
    ar = arange[1]
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



queue = []
def dfs(cur):
    if node_info[cur]['category'] == 'super sink':
        print_arangement(queue)
        exit()
    for v in graph[cur]:
        queue.append(node_info[v[0]])
        dfs(v[0])
        queue.pop()















































# find how many patients in total
n_patient = 0
for i in range(len(node_info)):
    if node_info[i]['category'] == 'illness':
        n_patient += 1
print(n_patient)



# from collections import deque

# class Dinic:
#     def __init__(self, graph):
#         self.graph = graph
#         self.N = len(graph)
#         self.level = [0] * self.N
#         self.it = [0] * self.N

#     def bfs(self, s, t):
#         for i in range(self.N):
#             self.level[i] = -1
#         queue = deque()
#         queue.append(s)
#         self.level[s] = 0

#         while queue:
#             u = queue.popleft()
#             for v, cap in self.graph[u]:
#                 if cap > 0 and self.level[v] < 0:
#                     self.level[v] = self.level[u] + 1
#                     queue.append(v)
#         return self.level[t] != -1

#     def dfs(self, u, t, flow):
#         if u == t:
#             return flow
#         for i in range(self.it[u], len(self.graph[u])):
#             self.it[u] = i
#             v, cap = self.graph[u][i]
#             if cap > 0 and self.level[u] < self.level[v]:
#                 d = self.dfs(v, t, min(flow, cap))
#                 if d > 0:
#                     self.graph[u][i] = (v, cap - d)
#                     for j in range(len(self.graph[v])):
#                         if self.graph[v][j][0] == u:
#                             vc, vcap = self.graph[v][j]
#                             self.graph[v][j] = (vc, vcap + d)
#                             break
#                     else:
#                         self.graph[v].append((u, d))
#                     return d
#         return 0

#     def max_flow(self, s, t):
#         flow = 0
#         while self.bfs(s, t):
#             for i in range(self.N):
#                 self.it[i] = 0
#             f = self.dfs(s, t, float('inf'))
#             while f:
#                 flow += f
#                 f = self.dfs(s, t, float('inf'))
#         return flow

#     def find_paths(self, s, t):
#         paths = []
#         path = []

#         def dfs_path(u):
#             path.append(u)
#             if u == t:
#                 paths.append(list(path))
#             else:
#                 for v, cap in self.graph[u]:
#                     if cap > 0:
#                         dfs_path(v)
#             path.pop()

#         dfs_path(s)
#         return paths


# dinic = Dinic(graph)
# max_flow = dinic.max_flow(0, 1)
# print("Max Flow:", max_flow)
# # paths = dinic.find_paths(0, 1)
# # print("Paths:", paths)

