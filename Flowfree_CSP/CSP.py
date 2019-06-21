class CSP():

    #CSP object tracks assigned and unassigned grids

    def __init__(self,filename,domain):
        self.puzzlefile = filename      
        self.assignedNode = {}
        self.unassignedNode = {}
        self.rows = 0
        self.cols = 0
        self.original = []
        self.domain= domain
        self.allNodes = {}
        self.final = []

    #Parse the input file to populate unassigned grids, assigned grids

    def parseFile(self):
        fp = open(self.puzzlefile, "r")
        lines = fp.readlines()
        x = 0 
        for line in lines:
            line1 = line.rstrip();
            y = 0
            elementlist = []
            for element in range(0,len(line1)):
                temp = []
                temp.append(x)
                temp.append(y)
                if line[element] is '_':
                    
                    N1 = self.Node(x,y,self.domain)
                    self.unassignedNode[tuple(temp)] = N1               
                else:
                    N1 = self.Node(x,y,line[element],line[element],True)                    
                    self.assignedNode[tuple(temp)] = N1
                self.allNodes[tuple(temp)] = N1
                elementlist.append(line[element])
                y = y + 1
            self.original.append(elementlist)
            self.final.append(elementlist)
            x = x + 1
        self.rows = x
        self.cols = y
        self.updateCnt()
        self.updateType()
        
    
    #Updates the initial empty and assigned neighbors of every grid
    def updateCnt(self):
        for location,node in self.allNodes.items():
            nbrs = self.getNeighbors(node.x,node.y)         
            for neighbor in nbrs:
                if self.allNodes[tuple(neighbor)].color == None:                    
                    node.emptyneighborlst.append(self.allNodes[tuple(neighbor)])
                else:
                    node.assignedneighborlst.append(self.allNodes[tuple(neighbor)])

    def updateType(self):
        for location,node in self.allNodes.items():
            if ((location[0] == 0 and location[1] == 0) or (location[0] == 0 and location[1] == self.cols -1 ) or (location[0] == self.rows-1 and location[1] == 0) or (location[0] == self.rows-1 and location[1] == self.cols-1)):
                node.type = 'corner'
            elif ( location[0] == 0 or location[0] == self.rows-1 or location[1] == 0 or location[1] == self.cols-1):
                node.type = 'edge'
            else:
                node.type = 'normal'




    #Node represents a grid in a given cell. Each node has the following attributes: the grid location, grid color once assigned, 
    #information about source/non-source, domainlist, list of empty and assigned neighbor nodes

    class Node():
        def __init__(self,xloc,yloc,domain,color=None,endpoint = False):
            self.x = xloc           
            self.y = yloc
            self.color = color
            self.dir = None
            self.endpoint = endpoint
            self.domainlist = domain            
            self.emptyneighborlst = []          
            self.assignedneighborlst = []
            self.type = None

        def __lt__(self,other):
            return (len(self.domainlist) < len(other.domainlist))

    #Returns the neighbors of a node
    def getNeighbors(self,x,y):
        nbrs = []
        if((y+1) < self.cols):
            l1 = []                  
            l1.append(x)
            l1.append(y+1)
            nbrs.append(l1)
        if((x+1) < self.rows):
            l1 = []
            l1.append(x+1)
            l1.append(y)
            nbrs.append(l1)
        if((x-1) >=0):
            l1 = []
            l1.append(x-1)
            l1.append(y)
            nbrs.append(l1)
        if((y-1) >=0):
            l1 = []
            l1.append(x)
            l1.append(y-1)
            nbrs.append(l1)

        return(nbrs)
    
    #Debug routines
    def printAllNodes(self):
        print("All Nodes")
        for key,node in self.allNodes.items():
            print(key)
            print(node.x, node.y, node.color, node.endpoint, node.domainlist, node.type)
            print("Assigned =" , len(node.assignedneighborlst))         
            #Assigned neighbors
            for node in node.assignedneighborlst:
                print(node.x,node.y)
            print("Empty = ", len(node.emptyneighborlst))
            for node in node.emptyneighborlst:
                print(node.x,node.y)

    def printAssignedNode(self):
        print("Assigned Nodes")
        for key,value in self.assignedNode.items():
            print(key, value)

    def printUnAssignedNode(self):
        print("UnAssigned Nodes")
        for key,value in self.unassignedNode.items():
            print(key, value)

    

    def printoriginal(self):
        print("Original Puzzle")
        print(self.rows,self.cols)
        for element in self.original:
            print(*element)


