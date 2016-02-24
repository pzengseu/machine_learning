#-*- coding: utf-8 -*-
#author: zp
'''
感知机学习算法的对偶形式
统计学习方法中算法2.2及例2.2简单实现
'''
import numpy as np

training_set = np.array([[[3, 3], 1], [[4, 3], 1], [[1, 1], -1]])

a = np.zeros(len(training_set), np.float)
b = 0.0
Gram = None
y = np.array(training_set[:, 1])
x = np.empty((len(training_set), 2), np.float)
for i in range(len(training_set)):
    x[i] = training_set[i][0]
history = []

def cal_gram():
    g = np.empty((len(training_set), len(training_set)), np.int)
    for i in range(len(training_set)):
        for j in range(len(training_set)):
            g[i][j] = np.dot(training_set[i][0], training_set[j][0])

    return g

def update(i):
    global a, b
    a[i] += 1
    b = b + y[i]
    history.append([np.dot(a*y, x), b])

def cal(i):
    global a, b, x, y

    res = np.dot(a*y, Gram[i])
    res = (res+b)*y[i]
    return res

def check(i):
    global a,b,x,y
    flag = False
    for i in range(len(training_set)):
        if cal(i) <= 0:
            flag = True
            update(i)
    if not flag:

        w = np.dot(a*y, x)
        print "RESULT: w: " + str(w) + " b: " + str(b)
        return False
    return True

Gram = cal_gram()
for i in xrange(1000):
    if not check(i):
        break

print history