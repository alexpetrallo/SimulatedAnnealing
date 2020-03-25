import time
import itertools
import random
import numpy as np
import matplotlib.pyplot as plt
start_time = time.time()
# from scipy.spatial import distance

def distance(x1, y1, x2, y2):
    d = np.sqrt((x2-x1)**2 + (y2-y1)**2)
    return d


coords = [(round(random.random(), 5), round(random.random(), 5)) for _ in range(10)]
# coords = np.genfromtxt(r'coordsWW.txt', delimiter=' ')


#########This will take a set of coordinates
#######(so you can compare with same coords in sim annealing)
# file = np.loadtxt('coordsWW.txt')
# lat = file[:,0]
# long = file[:,1]
#
# coords = []
# for i in range(len(lat)):
#     coords.append((lat[i], long[i] ))
cLen = len(coords)

# write to file so anealing can use same ones
# f = open("coords.txt", "w")
# for c in coords:
#     print(c)
#     f.write(c)
#     f.write('\n')
# f.close()


np.savetxt('coords.txt', coords)



cLen = len(coords)
distanceList = []

for i in range(cLen):
    # if coords[i] is not coords[-1]:
    x1 = coords[i][0]
    y1 = coords[i][1]

    dist = []


    for c in coords:
        x2 = c[0]
        y2 = c[1]

        dd = distance(x1, y1, x2, y2)
        dist.append(dd)
    distanceList.append(dist)



distances = [[0, 15, 20, 50, 100],
             [10, 0, 100, 25, 2],
             [15, 35, 0, 10, 30],
             [0, 25, 30, 0, 6],
             [8, 9, 10, 20, 0]]


graphs = (list(range(cLen)))

# permutations_object = list(itertools.permutations(graphs))


routes = list(itertools.permutations(range(1,cLen)))

zero = (0,)
walkings = []
for list in routes:
    list = zero + list
    walkings.append(list)


minWeight = 10000
minWalk = None
for walk in walkings:
    weight = 0
    for i in range(len(walk)):
        if walk[i] != walk[-1]:
            add = (distanceList[walk[i]][walk[i + 1]])
            if (walk[i], walk[i+1]) == (1, 5) or (walk[i], walk[i+1]) == (5, 1):
                add = add*200
                # weight += add

            # if walk[i]
            weight += add
        else:
            weight += (distanceList[walk[i]][walk[0]])
    if weight < minWeight:
        minWeight = weight
        minWalk = walk

runTime = time.time() - start_time


for i in range(cLen):

    x1 = coords[minWalk[i]][0]
    y1 = coords[minWalk[i]][1]
    plt.scatter(x1, y1, c='blue')

    if minWalk[i] != minWalk[-1]:
        x2 = coords[minWalk[i+1]][0]
        y2 = coords[minWalk[i+1]][1]

    else:
        x2 = coords[minWalk[0]][0]
        y2 = coords[minWalk[0]][1]

    xPts = [x1, x2]
    yPts = [y1, y2]

    plt.plot(xPts, yPts, c='red')

plt.plot([coords[0][0], coords[minWalk[-1]][0]], [coords[0][1], coords[minWalk[-1]][1]], c='r')
#plot coords from cooords[walk][1 to 5 add the roll here

plt.title("Brute Force Optimized Path distance =" + str(minWeight))
plt.savefig('bruteB.png')
plt.show()






