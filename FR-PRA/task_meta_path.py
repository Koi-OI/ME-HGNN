from collections import defaultdict
import random
import time


paths = defaultdict(int)
def dfs(graph, start, end, path=[]):
    global paths
    # 将当前节点加入路径
    path = path + [start]
    if len(path) >= 3:
        paths[''.join([d_node_type[node] for node in path])] += 1
    if len(path) >= 5:
        return
    # 如果当前节点就是目标节点，返回路径
    # if start == end:
    #     return
    # 如果当前节点不在图中，返回空路径
    if start not in graph:
        return

    # 对于当前节点的每个邻居节点，进行递归搜索
    for neighbor in graph[start]:
        # 如果邻居节点不在当前路径中，进行递归搜索
        if neighbor not in path:
            dfs(graph, neighbor, end, path)
            # for new_path in new_paths:
            #     paths.append(new_path)

    # return paths


# 读取原始数据文件，构建图
graph = {}
d_node_type = {}
types = [('p', 'a'), ('p', 'v'), ('p', 't')]
d_tj = {'p':0, 'a':0,'v':0,'t':0,'pa':0,'pv':0,'pt':0}
for i, path in enumerate(['data/DBLP/paper_author.txt', 'data/DBLP/paper_conf.txt', 'data/DBLP/paper_term.txt']):
    t_start = time.time()
    type1, type2 = types[i]
    with open(path, 'r') as file:
        all_lines = file.readlines()

        lines = random.sample(all_lines, 500)
        for line in lines:
            n1, n2 = line.strip().split()  # 假设原始数据文件中每行包含两个节点，以空格分隔
            if n1 not in graph:
                graph[n1] = []
            if n2 not in graph:
                graph[n2] = []
            graph[n1].append(n2)
            graph[n2].append(n1)
            d_node_type[n1] = type1
            d_node_type[n2] = type2
        all_1 = []
        all_2 = []
        for line in all_lines:
            n1, n2 = line.strip().split()
            all_1.append(n1)
            all_2.append(n2)
        if i == 0:
            d_tj['p'] += len(set(all_1))
            d_tj['a'] += len(set(all_2))
            d_tj['pa'] += len(all_lines)
        elif i == 1:
            d_tj['p'] += len(set(all_1))
            d_tj['v'] += len(set(all_2))
            d_tj['pv'] += len(all_lines)
        elif i == 2:
            d_tj['p'] += len(set(all_1))
            d_tj['t'] += len(set(all_2))
            d_tj['pt'] += len(all_lines)

# print(graph)
# # 遍历图中的所有节点，以每个节点作为起始点进行深度优先遍历

for start in graph:
     for end in graph:
         dfs(graph, start, end)
for k,v in sorted(paths.items(), key=lambda x: x[1], reverse=True):
#     if k[0] == 'a' and k[-1] == 'a':
#     if k[0] == k[-1]:
    if 'a' in k and len(k) == 3 and k[0] == k[-1]:
        print(k, v)
    if 'a' in k  and len(k) == 5 and k[0] == k[-1] and k[1] == k[-2] and k[0] != k[2]:
         print(k, v)
 
print(d_tj)
t_end = time.time()
print('Total time: ', t_end - t_start,'s')