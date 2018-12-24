import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np


initial = 0.001
run_times = 10
step = 100
gama = 0.08
beta = 0.15

result = dict()
result[0] = initial
for i in range(1, step):
    result[i] = []

fp = open('e:/paper_data/hash_without_time/Foxconn worker falls to death')
edge = []
for line in fp:
    (a, b) = line.split()
    edge.append((int(a), int(b)))
fp.close()
g = nx.Graph()
g.add_edges_from(edge)
node_num = g.number_of_nodes()

for times in range(run_times):
    I_set = []
    state = [0] * (node_num + 1)

    for i in range(int(initial * node_num)):
        temp = random.randint(1, node_num)
        while state[temp] == 1:
            temp = random.randint(1, node_num)
        state[temp] = 1
        I_set.append(temp)

    for i in range(1, step):
        I_new = []
        S_new = []
        for j in I_set:
            for k in nx.neighbors(g, j):
                if state[k] == 0:
                    if random.random() < beta:
                        if k not in I_new:
                            I_new.append(k)
            if random.random() < gama:
                S_new.append(j)
        for j in S_new:
            state[j] = 0
            I_set.remove(j)
        for j in I_new:
            state[j] = 1
            I_set.append(j)
        result[i].append(len(I_set) / node_num)
    print(times)

present = []
for i in sorted(result.keys()):
    present.append(np.mean(result[i]))
plt.axis([0, step, 0, 1])
plt.plot(sorted(result.keys()), present)
plt.show()

