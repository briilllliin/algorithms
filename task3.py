import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import norm

M = 101
C = 1
p = 2 ** 32
flag = True

def get_random(U, M, C, p):
    U_new = (U * M + C) % p
    return U_new / p, U_new

def get_random_array(length):
    U = 0
    R = []
    global M, C, p
    for _ in range(length):
        rand, U = get_random(U, M, C, p)
        R.append(rand)
    return R

def get_L():
    numbers = []
    U = [0]
    global M, C, p, flag
    R = []
    rand, num = get_random(U[-1], M, C, p)
    counter = 0
    while num not in numbers:
        U.append(num)
        R.append(rand)
        numbers.append(num)
        rand, num = get_random(U[-1], M, C, p)
        counter += 1
        if len(R) > 10000 and flag:
            print('Более 10000. Продолжить? Y/n')
            user_input = input()
            if user_input != 'Y':
                return len(U)
            else:
                flag = False
        if counter > 100000:
            break
    return len(R)

print('Наибольшая длина неповторяющихся элементов: ', get_L())

b = 0.99
d = 0.01
N = int((norm.ppf((1 - b) / 2) / (2 * d)) ** 2)

random_array = get_random_array(N)

sns_plot = sns.distplot(random_array)
fig = sns_plot.get_figure()
plt.show()

x = random_array[::2]
y = random_array[1::2]

hist, x_edges, y_edges = np.histogram2d(x, y, bins=10)

plt.imshow(hist, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]])
plt.xticks(ticks=x_edges)
plt.xlabel('x')
plt.yticks(ticks=y_edges)
plt.ylabel('y')
plt.show()
