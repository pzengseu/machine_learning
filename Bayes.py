#-*- coding: utf-8 -*-
#基于贝叶斯文本分类器实现的简单情感极性分析器
from math import log, exp

class LaplaceSmoothingEstimate(object):
    '''
    Laplace smooting
    '''

    def __init__(self):
        self.d = {} #词:词频
        self.total = 0.0 #用于计算先验概率
        self.num = 1  #用于计算条件概率
        self.none = 1 #当一个词不存在的时候,它的词频

    def exist(self, key):
        return key in self.d

    def getsum(self):
        return self.total

    def getnum(self):
        return self.num

    def get(self, key):
        if not self.exist(key):
            return False, self.none
        return True, self.d[key]

    def getprob(self, key):
        return float(self.get(key)[1])/self.total

    def sample(self):
        return self.d.keys()

    def add(self, key, value):
        self.num += value
        self.total += value
        if not self.exist(key):
            self.d[key] = 1
            self.total += 1
        self.d[key] += value

class Bayes(object):
    def __init__(self):
        self.d = {} #标签:概率
        self.total = 0

    def train(self, data):
        for d in data:
            c = d[1] #类别
            if c not in self.d:
                self.d[c] = LaplaceSmoothingEstimate()
            for word in d[0]:
                self.d[c].add(word, 1)
        self.total = sum(map(lambda x: self.d[x].getnum(), self.d.keys()))

    def classify(self, x):
        tmp = {}
        for c in self.d:
            tmp[c] = log(self.d[c].getnum()) - log(self.total) #p(Y=ck)
            for word in x:
                tmp[c] += log(self.d[c].getprob(word))
        ret, prob = 0, 0
        for c in self.d:
            now = 0
            try:
                for otherc in self.d:
                    now += exp(tmp[otherc] - tmp[c])
                now = 1/now
            except OverflowError:
                now = 0
            if now > prob:
                ret, prob = c, now
        return (ret, prob)

class Sentiment(object):
    def __init__(self):
        self.classifier = Bayes()

    def segment(self, sent):
        words = sent.split(' ')
        return words

    def train(self, neg_docs, pos_docs):
        data = []
        for sent in neg_docs:
            data.append([self.segment(sent), u'neg'])
        for sent in pos_docs:
            data.append([self.segment(sent), u'pos'])
        self.classifier.train(data)

    def classify(self, sent):
        return self.classifier.classify(self.segment(sent))

s = Sentiment()
s.train([u'糟糕', u'好 差劲'], [u'优秀', u'很 好']) # 空格分词

print s.classify(u"好 优秀 差劲 很 好 好")