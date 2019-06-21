import MstHeuristic
import math

'''Class Fore representing Search Graph'''
class Graph():
    
	class GraphNode():
		'''Subclass for representing Node of a Graph'''
		def __init__(self, xloc, yloc,parent):
			'''Each node stores (x,y) location in maze, it's pathcost, heuristic and it's parnet'''
			self.xloc = xloc
			self.yloc=yloc			
			self.parent = parent
			self.heuristic = -1
			self.mstlen = -1
			self.successors = []
			
			if parent is None:
				self.pathcost = 0
			else:
				self.pathcost = parent.pathcost + 1

		def addSuccessor(self,node):
			self.successors.append(node)


        
		def __lt__(self, other):
			'''Helps in priority queue implmentation for a python object'''
			return (self.heuristic < other.heuristic)
			

    
	def __init__(self, sp=False):
		'''Search Graph'''
		self.vertices = []
		self.root = None
		self.TotalNodes = 0
		self.goals =[]
		self.currgoalx = -1
		self.currgoaly = -1
		self.currentweight = -1;
		self.sp = sp
		self.cnt = 0
		
		
    
	def setGoal(self,xloc,yloc):
		'''Goal location is populated from Statespace'''
		self.currgoalx = xloc
		self.currgoaly = yloc


    
	def MSTCalculation(self):
		''' Function to calculate total edge length of minimum spanning Tree of current goals'''


		goalcnt= len(self.goals)		
		mst = MstHeuristic.MstHeuristic(goalcnt)
		for i in range(0,goalcnt):
			for j in range(i+1,goalcnt):
				dist = abs(self.goals[i][0] -self.goals[j][0]) + abs(self.goals[i][1] -self.goals[j][1])
				mst.addEdge(i,j,dist)

		self.currentweight = mst.KruskalMST()
		print(self.cnt, self.currentweight)
		self.cnt = self.cnt + 1
		
		
		
	
	
	def shortestGoal(self,startx,starty):
		'''Function to find the shortest goal'''
		i = 0
		mindist = math.inf
		minindex = 0
		for goal in self.goals:
			goalx = goal[0]
			goaly = goal[1]
			dist = abs(goalx -startx) + abs(goaly - starty)
			if dist < mindist:
				mindist = dist
				minindex = i
			i = i + 1
		#Returns the closest goal
		return(self.goals[minindex][0],self.goals[minindex][1])

    
	def farestGoal(self,startx,starty):
		'''Function to find farest goal: currently unused'''
		i = 0
		maxdist = 0
		maxindex = 0
		for goal in self.goals:
			goalx = goal[0]
			goaly = goal[1]
			dist = abs(goalx -startx) + abs(goaly - starty)
			if dist > maxdist:
				maxdist = dist
				maxindex = i
			i = i + 1
		#Returns the closest goal
		return(self.goals[maxindex][0],self.goals[maxindex][1])

	
	def updateGoalList(self, goallist, precompute = False, realdist = False):
		'''Set of goals updated from Statespace, to aid in minimum spanning tree calculation'''
		self.goals = goallist
		if precompute:
			self.MSTCalculation();

		

	def updateHeuristics(self,currentnode, realdist = False):
		(nearestgoalx,nearestgoaly) = self.shortestGoal(currentnode.xloc,currentnode.yloc)
		currentnode.heuristic =   self.currentweight + abs(currentnode.xloc - nearestgoalx) + abs(currentnode.yloc - nearestgoaly)+ currentnode.pathcost 

	
		
    
	def addVertex(self,xloc,yloc,parent, astar = False, multiplefood = False, realdist = False):
		''' A node is added to search tree, the heuristic of the node is updated based on Greedy or Astar (single and multiple dot)'''
		NewNode = self.GraphNode(xloc,yloc,parent)
		if astar:
			if multiplefood:
				'''Astar: Manhattan Distance to nearest goal plus minimum spanning tree's total edgelength plus pathcost is evaluation function'''
				(nearestgoalx,nearestgoaly) = self.shortestGoal(xloc,yloc)				
				NewNode.heuristic =  NewNode.pathcost + self.currentweight + abs(xloc - nearestgoalx) + abs(yloc - nearestgoaly)
				#print(self.currentweight, NewNode.heuristic)

			else:
				'''Astar : Manhattan Distance to  goal plus pathcost is evaluation function'''
				NewNode.heuristic = abs(xloc - self.currgoalx) + abs(yloc - self.currgoaly) + NewNode.pathcost
		else:
			'''Greedy : Manhattan Distance to goal is evaluation function'''
			NewNode.heuristic = abs(xloc - self.currgoalx) + abs(yloc - self.currgoaly)

		#tup = (self.currgoalx,self.currgoaly)
		#NewNode.statetrack[tup1] = 1

		self.TotalNodes = self.TotalNodes + 1
		self.vertices.append(NewNode)
		if parent is None:
			self.root = NewNode
		else:
			parent.addSuccessor(NewNode)
		return NewNode


	
	def printGraph(self):
		'''Debug friendly function'''
		print("\n Total Nodes is ", self.TotalNodes)
		for vertex in self.vertices:
			print("\nParent :", vertex.xloc,vertex.yloc, vertex.pathcost, vertex.heuristic)
			print("----->")
			for subnode in vertex.successors:
				print("\t", subnode.xloc,subnode.yloc,subnode.pathcost,subnode.heuristic,subnode.parent.xloc,subnode.parent.yloc)


	
