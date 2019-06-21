from collections import deque
import Graph
import queue as Q
import string
'''Top-level search for Astar and Greedy'''
class SearchAstarGreedy():
	'''Statepace and Graph class are instantiated'''

	
	def __init__(self,statespace):
		self.sp = statespace
		self.sp.parseFile()
		self.sg = Graph.Graph(self.sp)
        #Start and Goal location, total goals obtained from Statespace
		self.start = self.sp.getStart()
		(self.numgoals, self.goals) = self.sp.getGoals()
        #Frontier and priority queue defined
		self.frontier = Q.PriorityQueue()
		self.explored = {}
		#List to keep track of goals reached
		self.foundgoals =[]
		self.sg.setGoal(self.goals[0][0], self.goals[0][1])
		#Keeps track of total expanded nodes
		self.numNodes = 0
		



	def Greedy_Astar(self,Astar=False,manyfood=False):
			
		#Send goal locations to Search Graph to aid in Heuristic calculation
		self.sg.updateGoalList(self.goals, True)	
		
		# start node added as root of search tree
		root = self.sg.addVertex(self.start[0],self.start[1],None,Astar,manyfood)
		self.frontier.put(root)
		
		if (self.numgoals > 0):
			
			while(~self.frontier.empty()):
				

				#Get a node from frontier with lowest value of heuristic or evaluation function			
				currnode = self.frontier.get()
				self.numNodes = self.numNodes + 1
				goalchecktemp =[]
				#Add currrent node to explored
				goalchecktemp.append(currnode.xloc)
				goalchecktemp.append(currnode.yloc)
				
				self.explored[tuple(goalchecktemp)] = 1

				
				 
                #Check if current node is a gaol
				if goalchecktemp in self.goals:
					self.foundgoals.append(currnode)
					self.numgoals = self.numgoals - 1;
					
					
					#Break if all goals have been reached
					if (self.numgoals ==0):
						break
					## Remove the goal reached					
					##Add current Node as root
					self.goals.remove(goalchecktemp)
					#Updates Goal List and heuristics of current node
					self.sg.updateGoalList(self.goals, True)
					#Reset explored and frontier
					self.explored = {}
					self.frontier = Q.PriorityQueue()				
					
					self.sg.updateHeuristics(currnode)
					self.frontier.put(currnode)
					currnode = self.frontier.get()
					self.numNodes = self.numNodes + 1

			    ##Get neighbors of current node		
				nbrs = self.sp.getNeighbors(currnode.xloc,currnode.yloc)
				
				

				#For each neighbor do the following
				for m in range(0,len(nbrs),2):
					xloc = nbrs[m]
					yloc = nbrs[m+1]
					explorecheck = []
					explorecheck.append(xloc)
					explorecheck.append(yloc)
					addnode = False
					#Repeated state detection logic 

					if tuple(explorecheck) not in self.explored:
						if self.frontier.empty():
							addnode = True
						else:
							for item in self.frontier.queue:
								if(item.xloc == xloc and item.yloc == yloc):
									if(Astar == True and item.pathcost <= currnode.pathcost + 1 ):
										addnode = False
										break
									elif(Astar == True and item.pathcost > currnode.pathcost + 1):
										addnode = True
										break
									else:
										addnode = False
										break
								else:
									addnode = True
					if addnode:						
						subnode = self.sg.addVertex(xloc,yloc,currnode,Astar,manyfood)						
						self.frontier.put(subnode)

		#self.sg.printGraph()
		#print("Debug")
		#self.printDebug()
		if manyfood:
			self.plotGoals()
			print("Final Solution")
			print("Total nodes expanded = ",self.numNodes)
			print("Path cost =", self.foundgoals[len(self.foundgoals) - 1].pathcost)
			self.sp.printFinalSolution()



    #Helper function to print results
	def results(self):
		if self.foundgoals:
			for goal in self.foundgoals:
				self.backTrackPath(goal)
		else:
			print("No goals found")

	
	#Helper function to print results and debug if needed
	def backTrackPath(self,goal):
		print("Results for", goal.xloc, goal.yloc)
		print("Total nodes expanded = ",self.numNodes)		
		print("Path cost =", goal.pathcost)
		#print("Backtracking path")
		k = 1
		while(goal):
			#print("\n", goal.xloc, goal.yloc)
			if (k != 1 and goal.parent is not None):
				self.sp.original[goal.xloc][goal.yloc] = '.'
			k = 2
			#if (goal.parent is not None and goal.heuristic - goal.pathcost + 1 < goal.parent.heuristic - goal.parent.pathcost ):
				#print("Not consistent")
			goal = goal.parent
			
		self.sp.printSolution()	

	#Multiple dot helper function to print results
	def plotGoals(self):

		'''for i in range(0, len(self.foundgoals)):
			if (i >= 0 and i <= 9):
				self.sp.original[self.foundgoals[i].xloc][self.foundgoals[i].yloc] = i
			elif (i >=10 and i <= 35):
				self.sp.original[self.foundgoals[i].xloc][self.foundgoals[i].yloc] = chr(i+55)
			elif(i >=36 and i <= 61):
				self.sp.original[self.foundgoals[i].xloc][self.foundgoals[i].yloc] = chr(i+61)'''
		for i in range(0, len(self.foundgoals)):
			self.sp.original[self.foundgoals[i].xloc][self.foundgoals[i].yloc] = i
			

	#Helper function for debug
	def printDebug(self):
		print("Explored")
		for item in self.explored:
			print (item)

		print("Frontier")

		for item in self.frontier.queue:
			print(item.xloc, item.yloc, item.heuristic, item.pathcost)





		


                    
	











