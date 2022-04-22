#!/usr/bin/python3

from cmath import inf

"""
printMatrix takes a 2D array, and prints it as a matrix with alligned rows and collumns
"""
def printMatrix(matrix):
    for row in matrix:
        print("")
        for i in row:
            print(f"{i : ^7}", end="")
        print("")

"""
collumnMin takes a 2D array of integers and a collumn, and returns the value of the 
smallest integer in that collumn
"""
def collumnMin(matrix,collumn):
    cmin = inf
    for i in range(len(matrix)):
        if(matrix[i][collumn] < cmin):
            cmin = matrix[i][collumn]
    return cmin

"""
State is an object that represents a node in a TSP search tree, Its constructor can
be given a 2D arry, a lowerbound, and a path, but at minimum requres a matrix.
"""
class State:
    def __init__(self,matrix,lb = 0,path = [0]):
        self.lb = lb
        self.matrix = matrix
        self.path = path
        self.reduceMatrix(self.matrix)
    """
    reduceMatrix takes a matrix, and returns a reduced matrix, such that each row and
    collumn contains a 0 unless the assosiated node is already in the State path. It searches
    each row and each collum, giving a time complexity of O(n^2), with a space complexity of
    O(n^2) as it creates a new matrix, however it is never used in a way that doesn't replace
    an already created matrix.
    """
    def reduceMatrix(self,matrix):
        for i in range (len(matrix)):
            if i in self.path[:-1]:
                continue
            rmin = min(matrix[i])
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i][j] - rmin
            self.lb += rmin
        for j in range(len(matrix)):
            if j in self.path[1:]:
                continue
            cmin = collumnMin(matrix,j)
            for i in range(len(matrix)):
                matrix[i][j] = matrix[i][j] - cmin
            self.lb += cmin

    """
    makeChild creates a child of a state, and is given only the next node in the path, It copies
    the current states matrix, and must iterate through potentially the entire matrix, to cross
    out rows and collumns assosiated with visited nodes, giving a time and space complexity of O(n^2)
    """
    def makeChild(self, branch):
        childpath = self.path.copy()
        childpath.append(branch)
        childlb = self.lb + self.matrix.copy()[childpath[-2]][childpath[-1]]
        childmatrix = [row.copy() for row in self.matrix]

        for i in range(len(childpath)-1):
            for j in range(len(childmatrix[childpath[i]])):
                childmatrix[childpath[i]][j] = inf

        for i in range(len(childpath)-1):
            for j in range(len(childmatrix[childpath[i+1]])):
                childmatrix[j][childpath[i+1]] = inf

        if len(childpath) < len(childmatrix):
            childmatrix[childpath[-1]][childpath[0]] = inf

        child = State(childmatrix, childlb, childpath)
        
        return child


    def print(self):
        print("________________________________________________________________________")
        printMatrix(self.matrix)
        print(f"lower bound = {self.lb}")
        print(f"path = {self.path}")
        print("________________________________________________________________________")
    
    def prints(self):
        print("________________________________________________________________________")
        print(f"lower bound = {self.lb}")
        print(f"path = {self.path}")
        print("________________________________________________________________________")

    def __str__(self) -> str:
        return str(self.path) 

    def __eq__(self, __o: object) -> bool:
        return self.lb == __o.lb
    def __lt__(self, __o: object) -> bool:
        return self.lb < __o.lb