#-*- coding: utf-8 -*-
'''
模拟多元混合高斯分布的EM算法:
每个高斯分布的选择概率相同,标准差相同
这里指定二元混合高斯分布
'''

import math
import copy
import numpy as np
import matplotlib.pyplot as plt

def init_data(Sigma, Mu1, Mu2, K, N):
    '''
    :param Sigma: 标准差
    :param Mu1: 用于产生高斯分布1的随机数
    :param Mu2: 用于产生高斯分布1的随机数
    :param K: 高斯分布个数
    :param N: 输出数据个数
    :return:
    '''
    global X
    global Mu
    global Expectations
    X = np.zeros((1, N))
    Mu = np.random.random(K)
    Expectations = np.zeros((N, K))
    for i in xrange(0, N):   #生产N个随机数
        if np.random.random(1)[0] > 0.5:
            X[0, i] = np.random.normal(Mu1, Sigma)
        else:
            X[0, i] = np.random.normal(Mu2, Sigma)
    # print X

def e_step(Sigma, k, N):
    '''
    E步,计算E[Zij]
    :param Sigma:
    :param k:
    :param N:
    :return:
    '''
    global X
    global Mu
    global Expectations
    for i in xrange(N):
        sum = 0.0
        singles = np.zeros((1, k))
        for j in xrange(k):
            sum += math.exp(-((X[0, i] - Mu[j]) ** 2) / (2 * (float(Sigma) ** 2)))
            singles[0, j] = math.exp(-((X[0, i] - Mu[j]) ** 2) / (2 * (float(Sigma) ** 2)))
        Expectations[i] = singles / sum

def m_step(k, N):
    '''
    M步,计算Mu
    :param k:
    :param N:
    :return:
    '''
    global X
    global Mu
    global Expectations
    for j in xrange(k):
        singles = 0.0
        sum = 0.0
        for i in xrange(N):
            singles += Expectations[i, j] * X[0, i]
            sum += Expectations[i, j]
        Mu[j] = singles / sum

def run(Sigma, Mu1, Mu2, k, N, iter_num, Epsilon):
    '''
    迭代iter_num次,或精度达到Epsilon停止迭代
    '''
    init_data(Sigma, Mu1, Mu2, k, N)
    print "init Mu: ", Mu
    for i in xrange(iter_num):
        Old_mu = copy.deepcopy(Mu)
        e_step(Sigma, k, N)
        m_step(k, N)
        print i, Mu
        if sum(abs(Mu - Old_mu)) < Epsilon:
            break

if __name__ == '__main__':
    run(6, 40, 100, 2, 1000, 1000, 0.0001)
    # plt.hist(X[0, :], 50)
    # plt.show()