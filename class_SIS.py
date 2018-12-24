import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

# ################
# init
# ################
initial = 0.001                 # the initial rate of I
run_times = 10                  # the times of run
step = 100                      # the number of step ever times
gama = 0.08                     # the rate of I to S
beta = 0.15                     # the rate of S to I

result = dict()                 # the ratio of each step I to the total
result[0] = initial             # the ratio of I to the total at the begin
for i in range(1, step):
    result[i] = []

fp = open('scale_free_network')     # the topology of scale-free network
edge = []
for line in fp:
    (a, b) = line.split()
    edge.append((int(a), int(b)))
fp.close()
g = nx.Graph()
g.add_edges_from(edge)
node_num = g.number_of_nodes()      # the number of node

# #####################################
# main
# ####################################

for times in range(run_times):
    I_set = []                                      # the set of I
    state = [0] * (node_num + 1)                    # the sign of state, 0 means that S, 1 means that I

    for i in range(int(initial * node_num)):        # random select some I at begin
        temp = random.randint(1, node_num)
        while state[temp] == 1:
            temp = random.randint(1, node_num)
        state[temp] = 1
        I_set.append(temp)

    for i in range(1, step):
        I_new = []                                  # the new I is generate at each step
        S_new = []                                  # the recovery of node at each step
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


