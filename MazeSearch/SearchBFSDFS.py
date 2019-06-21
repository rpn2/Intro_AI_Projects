from collections import deque
import Graph
'''Top-level search for BFS and DFS'''
class SearchBFSDFS():
	'''Statepace and Graph class are instantiated'''
	def __init__(self, statespace):
		self.sp = statespace
		self.sp.parseFile()
		self.sg = Graph.Graph()
		#Start and Goal location, total goals obtained from Statespace
		self.start = self.sp.getStart()
		(self.numgoals, self.goals) = self.sp.getGoals()
		#Frontier and priority queue defined
		self.frontier = deque()
		self.explored = []
		#List to keep track of goals reached
		self.foundgoals =[]
		self.numNodes = 0

	def BFS_DFS(self, DFS = False):
		# start node added as root of search tree
		root = self.sg.addVertex(self.start[0],self.start[1],None)
		self.frontier.append(root)
		if (self.numgoals > 0):
			
			
			while(self.frontier):

				#Get a node from frontier for respective search
				if DFS:
					currnode = self.frontier.pop()
				else:
					currnode = self.frontier.popleft()
				self.numNodes = self.numNodes + 1
				goalchecktemp =[]
				#Add currrent node to explored
				goalchecktemp.append(currnode.xloc)
				goalchecktemp.append(currnode.yloc)
				self.explored.append(goalchecktemp)

				#Check if current node is goal

				if goalchecktemp in self.goals:
					self.foundgoals.append(currnode)
					self.numgoals = self.numgoals - 1;
					#Break if all goals have been reached
					if (self.numgoals ==0):
						break	
			    ##Get neighbors of current node		
				nbrs = self.sp.getNeighbors(currnode.xloc,currnode.yloc)

				#For each neighbor do the following
				for m in range(0,len(nbrs),2):
					xloc = nbrs[m]
					yloc = nbrs[m+1]
					explorecheck = []
					explorecheck.append(xloc)
					explorecheck.append(yloc)

					
					'''Repeated state detection
					Create a new node if neighbor is not in explored set &&
					if the frontier does not same node with lower cost'''
					delnode = None
					addnode = False
					if explorecheck not in self.explored:
						
						#Check the path cost of newnode with existing items in frontier
						if self.frontier:
							for eachitem in self.frontier:
								if(eachitem.xloc == xloc and eachitem.yloc == yloc and eachitem.pathcost > currnode.pathcost + 1):							
									delnode = eachitem
									addnode = True
									break
								elif(eachitem.xloc == xloc and eachitem.yloc == yloc and eachitem.pathcost <= currnode.pathcost + 1):
									addnode = False
									break
								else:
									addnode = True
						else:
							addnode = True
					#Add node
					if addnode:
						#Remove higher path cost node from frontier
						if delnode:
							self.frontier.remove(delnode)

						#add node with(x,y,0,parent)
						subnode = self.sg.addVertex(xloc,yloc,currnode)
						self.frontier.append(subnode)

	



    #Helper function to print results
	def results(self):
		if self.foundgoals:
			for goal in self.foundgoals:
				self.backTrackPath(goal)
		else:
			print("No goals found")

	#Helper function to print results and debug if needed
	def backTrackPath(self,goal):
		#print("Results")
		print("Total nodes expanded = ",self.numNodes)
		print("Path cost =", goal.pathcost)
		k = 1
		while(goal):
			#print("\n", goal.xloc, goal.yloc)
			if (k != 1 and goal.parent is not None):
				self.sp.original[goal.xloc][goal.yloc] = '.'
			k = 2
			goal = goal.parent
		self.sp.printSolution()	

	
    #Helper function for debug
	def printDebug(self):



		for item in self.explored:
			print (item)

		print("Frontier")

		while(self.frontier):
			item = self.frontier.pop()
			print(item.xloc, item.yloc)





		


                    
	











