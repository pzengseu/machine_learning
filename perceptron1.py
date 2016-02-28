#-*- coding: utf-8 -*-
#author: zp
'''
PLA perceptron learn algorithm
感知机学习算法的原始形式
统计学习方法中算法2.1及例2.1简单实现
'''

import matplotlib.pyplot as plt
import matplotlib.animation as ani

points  = [(3, 3, 1), (4, 3, 1), (1, 1, -1), (5, 2, -1)]
w = [0, 0]
history = []
b = 0

flag = 1
while True:
    if not flag:
        break
    for p in points:
        flag = 0
        if p[2]*(w[0]*p[0]+w[1]*p[1]+b) <= 0:
            flag = 1
            w0 = w[0]
            w1 = w[1]
            w[0] = w0 + p[2] * p[0]
            w[1] = w1 + p[2] * p[1]
            b = b + p[2]
            history.append([w, b])
            break

fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
line, = ax.plot([], [], 'g', lw=2)
label = ax.text([], [], '')

def init():
    line.set_data([], [])
    x, y, x_, y_ = [], [], [], []
    for p in points:
        if p[2] > 0:
            x.append(p[0])
            y.append(p[1])
        else:
            x_.append(p[0])
            y_.append(p[1])

    plt.plot(x, y, 'bo', x_, y_, 'rx')
    plt.axis([-6, 6, -6, 6])
    plt.grid(True)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Perceptron Algorithm')
    return line, label

def animate(i):
    global history, ax, line, label

    w = history[i][0]
    b = history[i][1]
    if w[1] == 0: return line, label
    x1 = -7
    y1 = -(b + w[0]*x1) / w[1]
    x2 = 7
    y2 = -(b + w[0]*x2)/ w[1]
    line.set_data([x1, x2], [y1, y2])
    x1 = 0
    y1 = -(b + w[0]*x1) / w[1]
    label.set_text(history[i])
    label.set_position([x1, y1])
    return line, label

print history
anim = ani.FuncAnimation(fig, animate, init_func=init, frames=len(history),
                         interval=1000, repeat=True, blit=True)
plt.show()