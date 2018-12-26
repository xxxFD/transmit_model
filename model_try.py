import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np


def weight_random(name):
    random_list = []
    fp = open(name)
    for line in fp:
        (a, b) = line.split()[0:2]
        for i in range(int(b)):
            random_list.append(int(a))
    fp.close()
    return random_list


def transmit(node):
    transmit_times[node] -= 1
    # 判断是否为第一次激活
    # 该条件为非第一次传播，且没有传播次数
    if transmit_times[node] == 0 and state[node] == 2:
        state[node] = 1
    # 还有传播次数，生成等待时间
    elif transmit_times[node] != 0:
        wait_time[node] = wait_time_list[random.randint(0, wait_range)]
        state[node] = 2
    # 第一次传播，生成传播次数与等待时间
    elif transmit_times[node] == 0 and state[node] == 0:
        transmit_times[node] = transmit_times_list[random.randint(0, times_range)] - 1
        if transmit_times[node] == 0:
            state[node] = 1
        else:
            wait_time[node] = wait_time_list[random.randint(0, wait_range)]
            state[node] = 2


initial = 1
run_times = 5
step = 300
beta = 0.1

transmit_times_list = weight_random('e:/paper_data/user_transmit_times/Foxconn worker falls to death.txt')
times_range = len(transmit_times_list) - 1
wait_time_list = weight_random('e:/fox_wait.txt')
wait_range = len(wait_time_list) - 1

transmit_num = dict()
transmit_sum = dict()
ratio_I = dict()
transmit_sum[0] = [0]
transmit_num[0] = [0]
for i in range(1, step):
    ratio_I[i] = []
    transmit_num[i] = []
    transmit_sum[i] = []

fp = open('e:/paper_data/hash_without_time/Foxconn worker falls to death')
edge = []
for line in fp:
    (a, b) = line.split()
    edge.append((int(a), int(b)))
fp.close()
g = nx.Graph()
g.add_edges_from(edge)
node_num = g.number_of_nodes()
ratio_I[0] = initial / g.number_of_nodes()


for times in range(run_times):
    state = [0] * (node_num + 1)
    wait_time = [-1] * (node_num + 1)
    transmit_times = [1] * (node_num + 1)

    for i in range(initial):
        temp = random.randint(1, node_num)
        while state[temp] == 1:
            temp = random.randint(1, node_num)
        state[temp] = 1
        transmit_times[temp] = 0

    for i in range(1, step):
        step_transmit_num = 0
        num_I = 0

        for j in range(1, node_num):
            if state[j] == 2:
                wait_time[j] -= 1
                if wait_time[j] == 0:
                    transmit(j)
                    step_transmit_num += 1
            if state[j] == 0:
                for k in nx.neighbors(g, j):
                    if state[k] == 1 or state[k] == 2:
                        if random.random() < beta:
                            transmit(j)
                            step_transmit_num += 1
                        break
        for j in state:
            if j == 1 or j == 2:
                num_I += 1

        ratio_I[i].append(num_I / node_num)
        transmit_num[i].append(step_transmit_num)
        if i == 1:
            transmit_sum[i].append(step_transmit_num)
        else:
            transmit_sum[i].append(transmit_sum[i - 1][times] + step_transmit_num)
    print(times)

result_ratio_I = []
result_transmit_num = []
result_transmit_sum = []
for i in sorted(ratio_I.keys()):
    result_ratio_I.append(np.mean(ratio_I[i]))
    result_transmit_num.append(np.mean(transmit_num[i]))
    result_transmit_sum.append(np.mean(transmit_sum[i]))


plt.subplot(3, 1, 1)
plt.axis([0, step, 0, 1])
plt.plot(sorted(ratio_I.keys()), result_ratio_I)
plt.subplot(3, 1, 2)
plt.plot(sorted(transmit_sum.keys()), result_transmit_sum)
plt.subplot(3, 1, 3)
plt.plot(sorted(transmit_num.keys()), result_transmit_num)
plt.show()


