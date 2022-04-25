#!/usr/bin/python3

import numpy as np


class Particle:
    def __init__(self,path,matrix):
        self.path = path
        self.matrix = matrix
        self.computeCost()

    def computeCost(self):
        cost = 0
        for i in range(len(self.path)-1):
            cost += self.matrix[self.path[i]][self.path[i+1]]
        cost += self.matrix[self.path[-1]][self.path[0]]
        self.cost = cost

    def moveTo(self, particle):
        # for i in range(len(self.path)):
        #     if(self.path[i] != particle.path[i]):
        #         j = self.path.index(particle.path[i])
        #         self.swap(i,j)
        #         break

        i = np.random.randint(len(self.path))
        j = self.path.index(particle.path[i])
        self.swap(i,j)

        self.computeCost()
        

    def swap(self, i, j):
        temp = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = temp

    def __str__(self) -> str:
        return str(self.path) + " " +str(self.cost)
    def __gt__(self, __o: object) -> bool:
        return self.cost < __o.cost
    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost
    def __eq__(self, __o: object) -> bool:
        return self.path == __o.path