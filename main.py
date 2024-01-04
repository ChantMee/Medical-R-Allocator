from data_generator import *
from graph import *
from utils import *
from max_flow import *


resources = generate_data()
node_info, index, graph = graph_init(resources)
print_graph_abstract(graph, node_info)

dinic = Dinic(graph)
max_flow = dinic.max_flow(0, 1)
arrs = dinic.find_paths()

for i in range(len(arrs)):
    for j in range(len(arrs[i])):
        arrs[i][j] = node_info[arrs[i][j]]
    if len(arrs[i]) % 2 == 1:
        nid = arrs[i][-1]['duplicate_id']
        arrs[i].append(node_info[nid - 1])

assert len(arrs) == max_flow
print(f'In the following {TOT_WEEKS} week(s), we can arrange {len(arrs)} patient(s) to have surgery. ({len(resources["illness"])} patients in total)')
print(len(arrs))
save_arangement(arrs)
# show_graph(graph, arrs)
