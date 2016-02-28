#-*- coding: utf-8 -*-
#示例维数灾难
import matplotlib.pyplot as plt
import numpy as np

max_demension = 10
ax = plt.axes(xlim=(0, max_demension), ylim=(0, 1/(0.01**max_demension)))
x = np.linspace(0, max_demension, 1000)
y = 1/(0.01**x)
plt.plot(x, y, lw=2)
plt.show()