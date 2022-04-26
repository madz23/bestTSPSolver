#!/usr/bin/python3
import random

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
        for x in range(int(len(self.path)/10)+1):
            i = np.random.randint(len(self.path))
            j = self.path.index(particle.path[i])
            self.swap(i,j)
        if(random.randint(0,len(self.path)*5) == 1):
            self.fullLocalSearch()

        self.computeCost()


    def swap(self, i, j):
        temp = self.path[i]
        self.path[i] = self.path[j]
        self.path[j] = temp
    
    def fullLocalSearch(self):
        possible = True
        while possible:
            swapped = False
            for i in range(1,len(self.path)):
                for j in range(i,len(self.path)):
                    newPath = self.path.copy()
                    tempP = Particle(newPath,self.matrix)
                    tempP.swap(i,j)
                    tempP.computeCost()
                    if tempP.cost < self.cost:
                        self.swap(i,j)
                        self.computeCost()
                        swapped = True
                        break
            if not swapped:
                possible = False


    def localSearchStep(self):
        newPath = self.path[:]
        i = np.random.randint(2,len(newPath)-1)
        j = np.random.randint(2,len(newPath)-1)
        temp = newPath[i]
        newPath[i] = newPath[j]
        newPath[j] = temp
        newcost = 0
        for i in range(len(self.path)-1):
            newcost += self.matrix[newPath[i]][newPath[i+1]]
        newcost += self.matrix[newPath[-1]][newPath[0]]
        # print(newcost)
        if(newcost < self.cost):
            self.path = newPath
            self.computeCost()
            # self.localSearch()

    def __str__(self) -> str:
        return str(self.path) + " " +str(self.cost)
    def __gt__(self, __o: object) -> bool:
        return self.cost < __o.cost
    def __lt__(self, __o: object) -> bool:
        return self.cost < __o.cost
    def __eq__(self, __o: object) -> bool:
        return self.path == __o.path
