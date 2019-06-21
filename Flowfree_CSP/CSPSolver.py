import CSP
import random

'''CSP solver uses backtracking to find solution to flow-free'''

class CSPSolver():

    def __init__(self, filename,domain):
        self.csp1 = CSP.CSP(filename, domain)
        self.csp1.parseFile()
        self.finalassignment = {}
        self.cnt = 0


    
    def backtrackSearch(self, heuristic = False):
        assignment = {}
        result,self.finalassignment = self.backtrack(assignment,self.csp1,heuristic)
        if result:
            self.markResults()
        else:
            "No solution found"

    #Helper function to print final results
    def markResults(self):
        for key, val in self.finalassignment.items():            
            self.csp1.final[key[0]][key[1]] = val

        for element in self.csp1.final:
            print(*element)

        print("Number of attempted assignments = ", self.cnt)

    #Recursive backtrack routine
    def backtrack(self,assignment,csp1,heuristic):
        if not csp1.unassignedNode:
            return True,assignment
       
        
        #Variable Selection: Select the unassigned variable and respective node
        var,VarNode = self.selectUnassignedVariable(csp1,heuristic)   
            
        #Value ordering heuristic
        domainlist = self.selectDomainList(var,VarNode,csp1,heuristic)
        
        for element in range(0, len(VarNode.domainlist)):
            val = VarNode.domainlist[element]
            
        
            if(self.consistencyCheck(var,val,csp1)):
                #If the assignment is consistent, add it to assigned and remove the node from unassigned
                VarNode.color = val
                assignment[tuple(var)] = val
                self.cnt = self.cnt + 1
                csp1.assignedNode[tuple(var)] = VarNode
                del csp1.unassignedNode[tuple(var)] 
                #Modify the emptyneighborlst and assignedneighborlst of Var's neighbors since var is assigned
                
                for node in VarNode.assignedneighborlst:
                    node.emptyneighborlst.remove(VarNode)
                    node.assignedneighborlst.append(VarNode)

                for node in VarNode.emptyneighborlst:
                    node.emptyneighborlst.remove(VarNode)
                    node.assignedneighborlst.append(VarNode)

                infresult = self.inferenceCheck(var,val,csp1)
                if infresult:
                    
                    result,dummy = self.backtrack(assignment,csp1,heuristic)
                    if result:
                        return result,dummy

            #Remove variable from assignment
            if(tuple(var) in csp1.assignedNode):
                
                VarNode.color = None
                del csp1.assignedNode[tuple(var)]
                csp1.unassignedNode[tuple(var)] = VarNode
                del assignment[tuple(var)] 
                
                #Modify the emptyneighborlst and assignedneighborlst of Var's neighbors since var is unassigned/Assignment is removed
                for node in VarNode.assignedneighborlst:
                    node.emptyneighborlst.append(VarNode)
                    node.assignedneighborlst.remove(VarNode)

                for node in VarNode.emptyneighborlst:
                    node.emptyneighborlst.append(VarNode)
                    node.assignedneighborlst.remove(VarNode)


        return False,assignment


    
    #Value ordeing heuristic
    def selectDomainList(self,var,VarNode,csp,heuristic = False):
        if not heuristic:
            return VarNode.domainlist

        ordereddomainlst = []

        #Domain list is ordered as per assigned cells in the neighborhood, neighest assigned neigbor is tried first
        #Ordered by 1x1, followed by 2x2, followed by rest of the elements
        #1x1
        for node in VarNode.assignedneighborlst:
            ordereddomainlst.append(node.color)

        #2by2

        for node in VarNode.assignedneighborlst:
            nbrs = csp.getNeighbors(node.x,node.y)
            for neighbor in nbrs:
                if tuple(neighbor) in csp.assignedNode:
                    if csp.assignedNode[tuple(neighbor)].color not in ordereddomainlst:
                        ordereddomainlst.append(csp.assignedNode[tuple(neighbor)].color)

        for node in VarNode.emptyneighborlst:
            nbrs = csp.getNeighbors(node.x,node.y)
            for neighbor in nbrs:
                if tuple(neighbor) in csp.assignedNode:
                    if csp.assignedNode[tuple(neighbor)].color not in ordereddomainlst:
                        ordereddomainlst.append(csp.assignedNode[tuple(neighbor)].color)


        #3by3

        '''for node in VarNode.assignedneighborlst:
            nbrs = csp.getNeighbors(node.x,node.y)
            for neighbor in nbrs:
                nextneighbrs = csp.getNeighbors(neighbor[0],neighbor[1])
                for nxtn in nextneighbrs:                    
                    if tuple(nxtn) in csp.assignedNode:
                        if csp.assignedNode[tuple(nxtn)].color not in ordereddomainlst:
                            ordereddomainlst.append(csp.assignedNode[tuple(nxtn)].color)

        for node in VarNode.emptyneighborlst:
            nbrs = csp.getNeighbors(node.x,node.y)
            for neighbor in nbrs:
                nextneighbrs = csp.getNeighbors(neighbor[0],neighbor[1])
                for nxtn in nextneighbrs:
                    if tuple(nxtn) in csp.assignedNode:
                        if csp.assignedNode[tuple(nxtn)].color not in ordereddomainlst:
                            ordereddomainlst.append(csp.assignedNode[tuple(nxtn)].color)'''

        #Rest of the colors
        for color in VarNode.domainlist:
            if color not in ordereddomainlst:
                ordereddomainlst.append(color)
                
        
        return ordereddomainlst

    
    #Function for choosing the next unassigned variable
    def selectUnassignedVariable(self,csp,heuristic = False):

        #Return a random value or walk through puzzle 
        if not heuristic:
            for key,val in csp.unassignedNode.items():
                return key, val
            #key = random.choice(list(csp.unassignedNode))
            #val = csp.unassignedNode.get(key)            
            return key,val
        else:
            #Find an assigned node that has one empty neighbor and return the empty neighbor as next assignment node, akin to MRV
            assignedNodeOneEmpty = []
            #Find an assigned node with 2 empty neighbors, under the condition that the filled neighbors are of different color
            assignedNodeTwoEmpty = []

            for loc,node in csp.assignedNode.items():
                if (len(node.emptyneighborlst) == 1):                     
                    #Get all nodes that has one empty neighbor
                    assignedNodeOneEmpty.append(node.emptyneighborlst[0])                  
                    #return (tuple(loc),node.emptyneighborlst[0])
                if (len(node.assignedneighborlst) == 2): 
                    if (node.assignedneighborlst[0].color != node.assignedneighborlst[1].color):
                        if (len(node.emptyneighborlst) > 0):
                            assignedNodeTwoEmpty.append(node.emptyneighborlst[0])
                            if (len(node.emptyneighborlst) > 1):
                                assignedNodeTwoEmpty.append(node.emptyneighborlst[1])



            
            

            if assignedNodeOneEmpty:
                
                minsize = len(assignedNodeOneEmpty[0].domainlist)
                minindex = 0               

                #Return the node with at minindex location
                loc = []
                loc.append(assignedNodeOneEmpty[minindex].x)
                loc.append(assignedNodeOneEmpty[minindex].y)
                return (tuple(loc),assignedNodeOneEmpty[minindex])

            if assignedNodeTwoEmpty:
                #return the node with maximum number of assigned neighbors
                index = 0
                maxassigned = 0
                for element in range(1,len(assignedNodeTwoEmpty)):
                    if (len(assignedNodeTwoEmpty[element].assignedneighborlst) > maxassigned):
                        index = element
                        maxassigned = len(assignedNodeTwoEmpty[element].assignedneighborlst)
                loc = []
                loc.append(assignedNodeTwoEmpty[index].x)
                loc.append(assignedNodeTwoEmpty[index].y)
                return (tuple(loc),assignedNodeTwoEmpty[index])



            #If there are no singleton neighbors, find an unassigned node, with most filled neighbors
            #Dictionary with key as number (X) of assigned neighbors and value as list of nodes with X assigned neighbors 
            #Each unassigned cell has 0 to 4 assigned neighbors
            unassignedNodeneighbor = {}
            for x in range(0,5):
                unassignedNodeneighbor[x] = []

            
            
            for loc, node in csp.unassignedNode.items():
                
                if unassignedNodeneighbor[len(node.assignedneighborlst)] is None :
                    lst = []
                    lst.append(node)
                    unassignedNodeneighbor[len(node.assignedneighborlst)] = lst
                    
                else:
                    temp = unassignedNodeneighbor.get(len(node.assignedneighborlst))
                    temp.append(node)
                    unassignedNodeneighbor[len(node.assignedneighborlst)] = temp
            
            


            #Return the node with most assigned value and lowest domain count, this is an extension of MRV
            for x in range(4,-1,-1):
                if unassignedNodeneighbor[x] is not None:
                    currentlist = unassignedNodeneighbor[x]
                    if currentlist:  
                        minindex = 0 
                        #Return the node with at minindex location
                        loc = []
                        loc.append(currentlist[minindex].x)
                        loc.append(currentlist[minindex].y)
                        return (tuple(loc),currentlist[minindex])


    
    #Check if same colored assigned neighbor rule is not violated
    def subChecksame(self, node, csp,neighbor):

        nbrs = csp.getNeighbors(node.x,node.y)
       
        nbrs.remove(list(neighbor))
        sameval = 0

        for neighbor in nbrs:
            if tuple(neighbor) in csp.assignedNode:
                if (csp.assignedNode[tuple(neighbor)].color == node.color):
                    sameval = sameval + 1
            

        if((node.endpoint == True) and (sameval + 1) > 1):
            return False

        if((node.endpoint == False) and (sameval + 1) > 2):
            return False

        return True

    #Check if same colored assigned neighbor rule is not violated
    def subCheckdiff(self, node, csp,neighbor):

        

        nbrs = csp.getNeighbors(node.x,node.y)
        nbrs.remove(list(neighbor))
        sameval = 0
        domaincnt = 0

        for neighbor in nbrs:
            if tuple(neighbor) in csp.assignedNode:
                if (csp.assignedNode[tuple(neighbor)].color == node.color):
                    sameval = sameval + 1
            else:
                if (node.color in csp.unassignedNode[tuple(neighbor)].domainlist):
                    domaincnt = domaincnt + 1

        

        if(node.endpoint == True):
            if((sameval == 0) and (domaincnt >= 1)):
                return True
            elif(sameval == 1):
                return True
            else:
                return False

        if(node.endpoint == False):
            #If there is no assigned node with same color, then the domaincount should be atleast 2 
            if(sameval ==0 and domaincnt >= 2):
                return True
            #If there is one assigned node with same color, then the domaincount should be atleast 1
            elif(sameval == 1 and domaincnt >=1):
                return True
            elif(sameval == 2):
                return True
            else:
                return False

        
    #Tight heuristics with variable and value ordering diminish the need for explicit inference check. Implicitly, it is part of value ordering
    def inferenceCheck(self, var, value, csp, dumb = False):
        return True

            

    #Function that checks if an assignment is consistent
    def consistencyCheck(self,var,val,csp):

        #Generate 4 neighbor's N: (x-1,y),(x+1,y),(x,y-1),(x,y+1)
        nbrs = csp.getNeighbors(var[0],var[1])
       

        #Count the number of occurences of "val" in nbrs[], if the neighbor is assigned
        #If neighbor is not assigned, count the number of occurences of "val" in domain list of unassigned neighbors
        sameval = 0        
        unassigned = 0         
        domaincnt = 0
        assigned = 0
        for neighbor in nbrs:
            #if a neighbor is assigned, get count same colored neighbors
           
            if tuple(neighbor) in csp.assignedNode:
                assigned = assigned + 1
                #For each previously assigned neighbors , check if the new value will violate consistency               
                if csp.assignedNode[tuple(neighbor)].color == val:
                    sameval = sameval + 1
                    subconsistencysame = self.subChecksame(csp.assignedNode[tuple(neighbor)], csp,var)
                    if not subconsistencysame:
                        return False
                else:
                    subconsistencydiff = self.subCheckdiff(csp.assignedNode[tuple(neighbor)], csp,var)
                    if not subconsistencydiff:
                        return False

            #If a neighbor is unassiged, check the number of times "val" occurs in unassigned domainlist
            else:
                unassigned = unassigned + 1                
                if val in csp.unassignedNode[tuple(neighbor)].domainlist:
                    domaincnt = domaincnt + 1

        #If there are 3 neighbors of same value, return false
        if (sameval >=3):
            return False
        #If none of the neighbors are assigned and atleast 2 neighbors have "val" in the domain
        if(unassigned == 4 and domaincnt >=2):
            return True
        
        #If there is no assigned node with same color, then the domaincount should be atleast 2 
        if(sameval ==0 and domaincnt >= 2):
            return True
        #If there is one assigned node with same color, then the domaincount should be atleast 1
        elif(sameval == 1 and domaincnt >=1):
            return True
        elif(sameval == 2):
            return True
        else:
            return False

        



        



        


         


         
        




















        





