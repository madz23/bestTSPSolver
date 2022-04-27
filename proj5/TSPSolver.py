#!/usr/bin/python3

from cmath import inf
from queue import PriorityQueue
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
# elif PYQT_VER == 'PYQT4':
# 	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import TSP_BB_functions as bb
import TSP_PSO as PSO



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		# print(results)
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	def greedy( self,time_allowance=60.0 ):
		"""Austin's greedy implementation"""
		start_time = time.time()
		results = {}
		cities = self._scenario.getCities()
		i = 1
		# get start node ( node 0 ):
		start = cities[0]
		isFullPath = False
		# is full path is never modified, but we shouldn't ever hit an infinite loop
		while not isFullPath:
			# print(i)
			# initialize a visited nodes list
			visited = [start]
			# while we haven't put every node:
			while len(visited) != len(cities):
				current = visited[-1]
				currentBest = None
				# add the next closest node:
				for city in cities:
					if city not in visited:
						if currentBest == None or current.costTo(city) <= current.costTo(currentBest):
							currentBest = city
				visited.append(currentBest)
			# check for a path back to node 1, otherwise repeat. If we have hit every node, return infinity.
			cost = 0
			for j in range(len(visited) - 1):
				cost += visited[j].costTo(visited[j+1])
				# print(j,visited[j]._index,cost)
				print(j, visited[j].costTo(visited[j+1]))
			cost += visited[-1].costTo(visited[0])
			# print(len(visited) -1, visited[-1]._index, cost)
			# print(visited[-1].costTo[visited[0]], cost)
			print(cost)


			print(i)
			if cost != np.inf or i == len(cities) - 1:
				print(i)
				end_time = time.time()
				bssf = TSPSolution(visited)
				print([city._index for city in visited])
				results['cost'] = cost
				results['time'] = end_time - start_time
				results['count'] = i
				results['soln'] = bssf
				results['max'] = None
				results['total'] = None
				results['pruned'] = None
				return results
			else:
				start = cities[i]
				i += 1

	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	def branchAndBound( self, time_allowance=60.0 ):
		"""
		Initialization - subsection
		initialize all the variable tracked turing the algorithm and returned, while the start variable 
		could technically take O(n!) time, however in practice with out problems it is very fast. and for 
		our problems, I believe its actually impossible, as there will always be a certain number of 
		solutions. For realisms sake, I'll consider it on average time O(n), which gives us O(n) time and
		space for this section
		"""
		#--------------------------------------------------
		cities = self._scenario.getCities()
		ncities = len(cities)
		start = TSPSolver.defaultRandomTour(self)
		bssf = None
		bssf_cost = start["cost"]
		print(bssf_cost)
		count = 0
		pruned = 0
		total = 0
		pqmax = 0
		matrix = []
		#---------------------------------------------------
		"""
		Initial Cost Matrix
		creating the cost matric takes O(n^2) time and space
		"""
		#---------------------------------------------------
		start_time = time.time()
		for i in range(ncities):
			matrix.append([])
			for j in range(ncities):
				matrix[i].append(cities[i].costTo(cities[j]))
		state0 = bb.State(matrix)
		total += 1
		#---------------------------------------------------
		"""
		Search
		Searching could potentially take O(n!), or max 60 seconds if n is large enough, 
		however the pruning aspect of the algorithm improves this significantly, for 
		most problem instance. As far as I am aware there is not a way to prove a garaunteed 
		time reduction for all problems, giving us a worst case O(n^2n!) time and space,
		where the n^2 is from the time it takes to compute each cost matrix.
		"""
		#---------------------------------------------------
		PQ = PriorityQueue()
		PQ.put((state0.lb/len(state0.path),state0))
		while not PQ.empty() and time.time()-start_time < time_allowance:
			if(len(PQ.queue) > pqmax):
				pqmax = len(PQ.queue)
			# print(pqmax)
			parent = PQ.get()
			if (parent[1].lb > bssf_cost):
				pruned += 1
				continue
			for i in range(ncities):
				if i not in parent[1].path:
					child = parent[1].makeChild(i)
					total += 1
					if(len(child.path) == ncities):
						solution = child.makeChild(child.path[0])
						if solution.lb < bssf_cost:
							bssf = solution.path
							bssf_cost = solution.lb
							count += 1
					if child.lb < bssf_cost:
						PQ.put((child.lb/len(child.path),child))
					else: pruned += 1
		#---------------------------------------------------
		"""
		Return
		If a new route is found it takes O(n) to turn it into a TSPSolution object,
		other than that these are all constant time, giving us O(n) time and space
		"""
		#---------------------------------------------------
		end_time = time.time()
		route = []
		if (bssf == None):
			bssf = start["soln"]
		else:
			for i in bssf[:-1]:
				route.append(cities[i])
			bssf = TSPSolution(route)
		results = {}

		results['cost'] = bssf.cost
		results['time'] = (end_time - start_time)
		results['count'] = count
		results['soln'] = bssf
		results['max'] = pqmax
		results['total'] = total
		results['pruned'] = pruned 
		print(results)
		return results
		#---------------------------------------------------

	

		



	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''
		
	def fancy( self,time_allowance=60.0 ):
		"""This is our particle swarm optimization algorithm.
		It creates particles that move towards the single best solution in their search space
		It is not guaranteed to find the optimal solutions, but it is guaranteed to be better than Greed"""
		cities = self._scenario.getCities()
		ncities = len(cities)
		basePath = [i for i in range(1,ncities)]
		count = 1
		pruned = 0
		total = 0
		pqmax = 0
		matrix = []
		route = []

		start_time = time.time()
		for i in range(ncities):
			matrix.append([])
			for j in range(ncities):
				matrix[i].append(cities[i].costTo(cities[j]))

		"""
		Creation of the particle swarm
		"""
		particleSwarm = []

		routeAsCities = self.greedy()['soln'].route
		path = [city._index for city in routeAsCities]
		print(path[0])
		while path[0] != 0:
			path = path[1:] + path[:1]
		bestParticle = PSO.Particle(path,matrix)
		i = 0
		swarmSize = ncities*3
		while i <= swarmSize or (bestParticle.cost == np.inf and i < swarmSize * 2):
			print(i)                           #size of swarm
			path = np.random.permutation(basePath).tolist()
			path.insert(0,0)
			particleSwarm.append(PSO.Particle(path,matrix))
			if(particleSwarm[i] > bestParticle):
				bestParticle = particleSwarm[i]
			i += 1
		"""
		The actual swarming part
		"""
		
		iterations = 0
		while len(particleSwarm) > 1:
			print(iterations,len(particleSwarm))
			for particle in particleSwarm:
				particle.moveTo(bestParticle)
				if(particle > bestParticle):
					bestParticle = particle
					bestParticle.fullLocalSearch()
					print("new best")
					count += 1

			place = 0
			while place <= len(particleSwarm)-1 :
				for i in range(len(particleSwarm)-1,place,-1):
					if particleSwarm[place] == particleSwarm[i]:
						del particleSwarm[i]
				place += 1

			iterations += 1
			
		end_time = time.time()
		print("_____________________________")
		print(bestParticle)
		print("______________________________")

		"""
		Results calculation
		"""
		for i in bestParticle.path:
			route.append(cities[i])
		# print(route)
		bssf = TSPSolution(route)
		results = {}

		results['cost'] = bssf.cost
		results['time'] = (end_time - start_time)
		results['count'] = count
		results['soln'] = bssf
		results['max'] = pqmax
		results['total'] = total
		results['pruned'] = pruned 
		print(results)
		return results

		pass
		



