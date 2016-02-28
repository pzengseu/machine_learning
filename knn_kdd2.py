#-*- coding: utf-8 -*-
#author: zp
#简单模拟KNN算法中KD树的生成与KD树搜索

T = [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]

class node:
    def __init__(self, point):
        self.left = None
        self.right = None
        self.point = point
        self.parent = None

    def set_left(self, left):
        if not left: pass
        left.parent = self
        self.left = left

    def set_right(self, right):
        if not right: pass
        right.parent = self
        self.right = right

def median(lst):
    m = len(lst) / 2
    return lst[m], m

def build_kdtree(data, d):
    data = sorted(data, key=lambda x: x[d])
    p, m = median(data)
    tree = node(p)

    del data[m]
    # print data, p

    if m > 0: tree.set_left(build_kdtree(data[:m], not d))
    if len(data) > 1:   #只剩两个数的情形
        # print len(data)
        tree.set_right(build_kdtree(data[m:], not d))
    return tree

def distance(a, b):
    print a, b
    return ((a[0] - b[0])**2 + (a[1] - b[1])**2)**0.5

def update_best(t, best, target):
    if not t: return
    d = distance(t.point, target)
    if d < best[1]:
        best[1] = d
        best[0] = t.point

def search_kdtree(tree, d, target):
    # print target[d], tree.point[d]
    if target[d] < tree.point[d]:
        if tree.left != None:
            return search_kdtree(tree.left, not d, target)
    elif target[d] >= tree.point[d]:
        if tree.right != None:
            return search_kdtree(tree.right, not d, target)

    best = [tree.point, 10000000]
    while(tree.parent):
        update_best(tree.parent.left, best, target)
        update_best(tree.parent.right, best, target)
        tree = tree.parent
    return best[0]

kd_tree = build_kdtree(T, 0)
print search_kdtree(kd_tree, 0, [9, 4])
