
'''Class to represent statespace for Part1 : Basic Pathfinding'''
class StateSpace():
	''' Get mazefile to parse, store it as inplist, get the start location, goal locations, total goals'''   
    
	def __init__(self,filename):
		self.mazefile = filename
		self.inplist = []
		self.goal =[]
		self.start =[]
		self.original = []
		self.numgoals = 0
		self.rows = 0
		self.cols = 0
		''' Parse the input Maze text file and store it as 2D list in python. The topmost left corner is (0,0) and bottom right corner is (maxrow,maxcol)
		The indices of list are maze (x,y) locations and values are 1 for Wall, 0 for path, 2 for start node, 3 for goals'''
	def parseFile(self):
		fp = open(self.mazefile, "r")
		lines = fp.readlines()
		x = 0 
		for line in lines:
			temp = []
			temp1 = []
			y = 0
			for element in range(0,len(line) - 1):
				temp1.append(line[element])
				if line[element] is '%':
					temp.append(1)
				elif line[element] is ' ':
					temp.append(0)
				elif line[element] is 'P':
					temp.append(2)
					self.start.append(x)
					self.start.append(y)
				elif line[element] is '.':
					temp.append(3)
					tempgoal = []
					tempgoal.append(x)
					tempgoal.append(y)
					self.goal.append(tempgoal)
					self.numgoals = self.numgoals + 1;
				y = y + 1
			self.inplist.append(temp)
			self.original.append(temp1)
			x = x + 1
		self.rows = x
		self.cols = y


	'''Functions to return the start location, all goal locations and number of goals'''
	def getStart(self):
		return self.start
	def getGoals(self):
		return (self.numgoals, self.goal)

	''' Function to get valid successors of a given node'''
	def getNeighbors(self,x,y):
		nbrs = []
		if((x-1) >=0):
			if(self.inplist[x-1][y] != 1):
				nbrs.append(x-1)
				nbrs.append(y)
		if((x+1) < self.rows):
			if(self.inplist[x+1][y] != 1):
				nbrs.append(x+1)
				nbrs.append(y)
		if((y-1) >=0):
			if(self.inplist[x][y-1] != 1):
				nbrs.append(x)
				nbrs.append(y-1)
		if((y+1) < self.cols):
			if(self.inplist[x][y+1] != 1):
				nbrs.append(x)
				nbrs.append(y+1)
		return(nbrs)

	'''Helper function for debug'''
	def printMaze(self):

		for item in self.inplist:
			print(*item)

		print("\nStart is ", self.start)
		print("\nGoals = " , self.numgoals)
		for item in self.goal:
			print(*item)

		print("\n Rows = ", self.rows)
		print("\n Cols = ", self.cols)


	'''Helper function to plot results'''
	def printSolution(self):
		for item in self.original:
			print(*item)








		

		











