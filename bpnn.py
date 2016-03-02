#-*- coding: utf-8 -*-
#The back-propagation algorithm
import math
import random
random.seed(0)

def rand(a, b):
    return (b - a) * random.random() + a

def makeMatrix(I, J, fill=0.0):
    m = []
    for i in xrange(I):
        m.append([fill] * J)
    return m

def randomizeMatrix(matrix, a, b):
    for i in xrange(len(matrix)):
        for j in xrange(len(matrix[0])):
            matrix[i][j] = random.uniform(a, b)

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def dsigmoid(y):
    return y * (1 - y)

class NN:
    def __init__(self, ni, nh, no):
        '''

        :param ni: The number of input layer node
        :param nh: The number of hide layer node
        :param no: The number of output layer node
        :return:
        '''

        self.ni = ni + 1 #bais node
        self.nh = nh
        self.no = no

        #output value
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no
        # print self.ai
        #weight matrix
        self.wi = makeMatrix(self.ni, self.nh) #input layer to hide layer
        self.wo = makeMatrix(self.nh, self.no) #hide layer to output layer

        #randomize weight matrix
        randomizeMatrix(self.wi, -0.2, 0.2)
        randomizeMatrix(self.wo, -2.0, 2.0)

        #权重矩阵的上次梯度
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def runNN(self, inputs):
        '''
        前向传播算法
        :param inputs:
        :return:
        '''
        if len(inputs) != self.ni - 1:
            print "incorrect number of inputs"

        for i in xrange(self.ni - 1):
            self.ai[i] = inputs[i]

        for j in xrange(self.nh):
            sum = 0.0
            for i in xrange(self.ni):
                # print self.ai[i], self.wi[i][j]
                sum += (self.ai[i] * self.wi[i][j])
            self.ah[j] = sigmoid(sum)

        for k in xrange(self.no):
            sum = 0.0
            for j in xrange(self.nh):
                sum += (self.ah[j] * self.wo[j][k])
            self.ao[k] = sigmoid(sum)

        return self.ao

    def backPropagate(self, targets, N, M):
        '''
        后向传播算法
        :param targets: 实例的类别
        :param N: 本次学习效率
        :param M: 上次的学习效率
        :return: 最终的误差平方和的一半
        '''
        output_deltas = [0.0] * self.no
        for k in xrange(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = error * dsigmoid(self.ao[k])

        for j in xrange(self.nh):
            for k in xrange(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += N * change + M * self.co[j][k]
                self.co[j][k] = change

        hidden_deltas = [0.0] * self.nh
        for j in xrange(self.nh):
            error = 0
            for k in xrange(self.no):
                error += output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = error * dsigmoid(self.ah[j])

        for i in xrange(self.ni):
            for j in xrange(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] += N * change + M * self.ci[i][j]
                self.ci[i][j] = change

        error = 0.0
        for k in xrange(len(targets)):
            error += 0.5 * (targets[k] - self.ao[k]) ** 2
        return error

    def weights(self):
        print "Input weights:"
        for i in xrange(self.ni):
            print self.wi[i]
        print
        print "Output weights:"
        for j in xrange(self.nh):
            print self.wo[j]
        print ''

    def test(self, patterns):
        for p in patterns:
            inputs = p[0]
            print "Inputs:", p[0], '-->', self.runNN(inputs), '\tTargets', p[1]

    def train(self, patterns, max_iterations=1000, N=0.5, M=0.1):
        for i in xrange(max_iterations):
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.runNN(inputs)
                error=self.backPropagate(targets, N, M)
            if i%50 == 0:
                print 'Combined error', error
        self.test(patterns)

def main():
    pat = [
        [[0, 0], [1]],
        [[0, 1], [1]],
        [[1, 0], [1]],
        [[1, 1], [0]]
    ]
    myNN = NN(2, 2, 1)
    # myNN.weights()
    myNN.train(pat)


if __name__ == "__main__":
    main()