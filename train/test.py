import argparse
import sys

from dgl.data import CoraGraphDataset, CiteseerGraphDataset, CoauthorCSDataset
from dgl.data.utils import split_dataset

sys.path.append('../')
import csv
import ast
import itertools
import matplotlib.pyplot as plt
from sklearn.manifold import Isomap
from dgl import DGLGraph
import numpy as np
import torch as th
import torch.nn.functional as F
import dgl.function as fn
from utils.data_geom import load_data_from_file
from utils.data_mine import print_graph_info, load_data_default
import os
from utils.result_utils import extract_test_accs, get_noisy_edges
import dgl
"""测试按引用赋值"""
# x = th.Tensor([1, 2, 3])
# y = x
# print(x)
# y[0] = 4
# print(x)


"""测试geom中引入的data相关的api"""
"""citation数据集即使加了自循环，也不应该有这么多边啊，可能和作者disconnected那部分有关，但是没看懂"""
"""添加了自循环后，chameleon的边数少了50，不知道是什么原因"""
# g, features, labels, train_mask, val_mask, test_mask, num_feats,\
#                 num_classes = load_data_from_file('chameleon', None, 0.6, 0.2)
# print_graph_info(g)

"""测试命令行"""
# cmds = []
# cmds.append('python hello.py --name A')
# cmds.append('python hello.py --name B')
# for cmd in cmds:
#     os.system(cmd)

"""测试读命令文件"""
# with open('shells/test.txt', 'r') as f:
#     cmds = f.readlines()
#     for cmd in cmds:
#         print(cmd)

"""测试permute等"""
# a = th.Tensor([[[1,2,3],[4,5,6]]])
# print(a.shape)
# b = th.Tensor.permute(a, 2, 0, 1)
# print(b.shape)
# print(b)
# c = th.Tensor.view(a, 3, 1, 2)
# print(c.shape)
# print(c)
# print(a)
# print(a.reshape(3, 1, 2))

# results = extract_test_accs('result/train_result/SGC.txt')
# print(results)

# a = np.array([[0.778, 0.8, 0.797, 0.805, 0.808, 0.807, 0.805, 0.799, 0.802, 0.804, 0.802, 0.796, 0.796, 0.793, 0.792, 0.793, 0.789, 0.787, 0.787, 0.784, 0.777, 0.775, 0.772, 0.771, 0.769, 0.766, 0.762, 0.759, 0.756, 0.753, 0.75, 0.745, 0.742, 0.732, 0.728, 0.714, 0.705, 0.696, 0.685, 0.673, 0.659, 0.643, 0.632, 0.618, 0.599, 0.585, 0.566, 0.547, 0.527],
# [0.781, 0.801, 0.798, 0.805, 0.808, 0.807, 0.805, 0.799, 0.802, 0.804, 0.802, 0.795, 0.797, 0.793, 0.791, 0.793, 0.789, 0.787, 0.786, 0.785, 0.777, 0.775, 0.773, 0.771, 0.769, 0.766, 0.762, 0.759, 0.756, 0.753, 0.749, 0.745, 0.742, 0.733, 0.728, 0.714, 0.707, 0.696, 0.686, 0.673, 0.658, 0.643, 0.632, 0.622, 0.6, 0.585, 0.565, 0.547, 0.529]])
# b = np.array([[0.746, 0.774, 0.777, 0.784, 0.784, 0.785, 0.788, 0.792, 0.792, 0.794, 0.799, 0.799, 0.798, 0.799, 0.801, 0.801, 0.806, 0.805, 0.807, 0.809, 0.809, 0.812, 0.811, 0.812, 0.81, 0.812, 0.811, 0.811, 0.812, 0.811, 0.812, 0.812, 0.813, 0.815, 0.813, 0.814, 0.814, 0.813, 0.814, 0.816, 0.815, 0.813, 0.814, 0.815, 0.817, 0.816, 0.815, 0.814, 0.814],
# [0.747, 0.776, 0.775, 0.783, 0.782, 0.787, 0.788, 0.794, 0.792, 0.794, 0.797, 0.799, 0.798, 0.799, 0.8, 0.802, 0.807, 0.806, 0.807, 0.808, 0.809, 0.811, 0.811, 0.812, 0.812, 0.811, 0.811, 0.81, 0.812, 0.812, 0.812, 0.814, 0.813, 0.813, 0.814, 0.815, 0.815, 0.814, 0.814, 0.815, 0.814, 0.813, 0.814, 0.814, 0.814, 0.816, 0.816, 0.815, 0.816]])
# c = np.array([[0.749, 0.78, 0.785, 0.79, 0.79, 0.795, 0.791, 0.795, 0.799, 0.801, 0.797, 0.799, 0.803, 0.807, 0.805, 0.81, 0.809, 0.811, 0.813, 0.816, 0.815, 0.814, 0.817, 0.816, 0.817, 0.816, 0.814, 0.813, 0.815, 0.813, 0.814, 0.815, 0.815, 0.814, 0.816, 0.815, 0.815, 0.814, 0.817, 0.815, 0.815, 0.816, 0.817, 0.817, 0.816, 0.815, 0.818, 0.815, 0.822],
# [0.746, 0.783, 0.787, 0.79, 0.789, 0.796, 0.791, 0.799, 0.8, 0.8, 0.799, 0.799, 0.803, 0.807, 0.809, 0.81, 0.808, 0.811, 0.813, 0.813, 0.817, 0.816, 0.815, 0.818, 0.819, 0.816, 0.813, 0.815, 0.815, 0.814, 0.813, 0.813, 0.814, 0.814, 0.812, 0.815, 0.816, 0.817, 0.815, 0.814, 0.814, 0.816, 0.814, 0.816, 0.816, 0.816, 0.816, 0.818, 0.818]])
# r = np.median(c, 0)
# print(repr(r))
# r = np.array([0.631, 0.631, 0.641, 0.636, 0.644, 0.653, 0.656, 0.655, 0.649, 0.652, 0.65, 0.653, 0.654, 0.657, 0.66, 0.667, 0.665, 0.671, 0.671, 0.671, 0.674, 0.679, 0.679, 0.682, 0.68, 0.689, 0.688, 0.688, 0.695, 0.691, 0.694, 0.692, 0.699, 0.698, 0.695, 0.694, 0.698, 0.698, 0.696, 0.693, 0.693, 0.693, 0.697, 0.693, 0.697, 0.691, 0.693, 0.687, 0.694])
# best = max(r)
# index = np.where(r == best)
# print(best)
# print(index)

# dgl_dataset = DglNodePropPredDataset(name="ogbn-arxiv")
# print(dgl_dataset.num_classes)
# split_index = dgl_dataset.get_idx_split()
# print(dgl_dataset[0])
#
# print(split_index)
# if 'cora' in ['cora', 'pubmed', 'citeseer']:
#     print('sb')

# dataset = dgl.data.CiteseerGraphDataset()
# graph = dataset[0]
# print(type(graph))
# node_features = graph.ndata['feat']
# print(type(node_features))

# data = DglNodePropPredDataset(name='ogbn-arxiv')
# graph, labels = data[0]
# print(type(labels))

# a = th.Tensor([1, 2, 3, 4])
# print(a.shape)
# print(2 * a)
# print(a + 1)

# g, features, labels, train_mask, val_mask, test_mask, num_feats, num_classes = load_data_default('cora')
# degs0 = g.in_degrees().float().clamp(min=1)
# print(degs0[0:9])
# g = g.remove_self_loop()
# degs1 = g.in_degrees().float().clamp(min=1)
# print(degs1[0:9])

# with open('../shells/tmp.txt', 'r') as f:
#     s = f.readlines()
#     print(len(s))

# with open('../shells/fuck.txt', 'w') as f:
#     for _ in range(3):
#         for _ in range(2):
#             f.write('fuck\n')

# a = {'a':1, 'b':2, 'c':3}

# with open('../shells/test.csv', 'a') as f:
#     fdn = list(a.keys())
#     writer = csv.DictWriter(f, fieldnames=fdn)
#     writer.writerow(a)

# with open('../shells/test.csv', 'r') as f:
#     reader = csv.DictReader(f)
#     print(reader.line_num)
#     for i in reader:
#         print(i)


# a = np.array([1, 2, 3, 4, 5, 6])
# print(a)
# b = a.reshape([2, 3])
# print(a)
# print(b)
# c = a.reshape([3, 2])
# print(c)

# dataset = CoauthorCSDataset()
# print(dataset[0])


# dataset = ['cora', 'citeseer', 'pubmed', 'chameleon', 'cornell', 'texas', 'wisconsin']
#
# with open('../shells/MLP_result_{}.txt'.format('_'.join(dataset)), 'w') as f:
#     for d in dataset:
#         for i in range(10):
#             split = '../data/splits/{}_split_0.6_0.2_{}.npz'.format(d, i)
#             command = 'python train_mlp.py --dataset {} --split {}\n'.format(d, split)
#             f.write(command)

# a = th.Tensor([[1, 0], [0, 0]])
# print(th.inverse(a))

# with open("../shells/VBlockGCN_nsl_search_cora.sh", "r") as f:
#     l = f.readlines()
#     print(len(l))

# a = th.Tensor([0.2393, 0.1668, 0.1246, 0.3383, 0.2066, 0.1483, 0.3383, 0.5780, 0.2766,
#         0.2274])
# print(th.pow(a, -1))

# a = th.Tensor([1, 2, 3])
# print(a**2)


# graph, features, labels, train_mask, val_mask, test_mask, num_feats, num_classes = load_data_default("cora")
# # edges = graph.edges()
# # print(edges)
# graph = graph.remove_self_loop()
# print(graph.number_of_edges())
# es = get_noisy_edges(graph, labels)
# print(len(es))

# a = th.Tensor([1, 2, 3, 4, 5])
# b = th.Tensor([3, 4, 5, 6, 7])
# count = 0
# for t in a:
#     if t in b:
#         count += 1
# print(count)

def remove_reverse_edges(graph):
    edges = graph.edges()
    m = graph.num_edges()
    edges_set = set()
    remove_eids = []
    for i in range(m):
        u, v = edges[0][i].item(), edges[1][i].item()
        if u > v:
            e = (v, u)
        else:
            e = (u, v)
        if e in edges_set:
            remove_eids.append(i)
        else:
            edges_set.add(e)

    graph.remove_edges(th.LongTensor(remove_eids))


graph, features, labels, train_mask, val_mask, test_mask, num_feats, num_classes = load_data_default("citeseer")
graph = graph.remove_self_loop()
print(graph.num_edges())
remove_reverse_edges(graph)
print(graph.num_edges())

