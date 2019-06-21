
'''Class that describes the training process of given samples'''
class Training():

    def __init__(self, yestrain,notrain):
        self.yestrainfile = yestrain
        self.notrainfile  = notrain
        #likelihoods numerator is represented as key,value pairs
        #Key is row id, sum of columns; value is number of high pattern in the sequence
        self.yes = {}        
        self.no = {}  
        #priors calculation
        self.totalyes = 0
        self.totalno = 0
        self.yesprior = 0
        self.noprior = 0
        
        #Original training in 1,0 format
        self.originalyes = []
        self.originalno = []
        self.initdict()

    
    ''' Function to initialize all count as zero'''
    def initdict(self):
        for x in range(0,25):
            for y in range(0,11):
                temp = []
                temp.append(x)
                temp.append(y)                
                self.yes[tuple(temp)] = 0 
                self.no[tuple(temp)] = 0

                
               
        

    ''' Function to parse yes training set'''
    def parseyes(self):
        yesfp = open(self.yestrainfile, "r")
        yeslines = yesfp.readlines()
        yesfp.close()
        x = 0 
        for yesline in yeslines:                      
            elementlist = []           
            
            #After 3 empty lines, new training pattern begins
            if (x == 28):
                x = 0
            if x < 25:
                temp = []
                temp.append(x)
                highcnt = 0
                for element in range(0,10):   
                    if yesline[element] is '%':                        
                        elementlist.append(0)
                    else:
                        highcnt = highcnt + 1
                        elementlist.append(1)
                temp.append(highcnt)
                self.yes[tuple(temp)] = self.yes[tuple(temp)] + 1
                self.originalyes.append(elementlist)
            else:
                self.originalyes.append("End")
            x = x + 1
            '''Check end of a pattern'''
            if (x == 25):
                self.totalyes = self.totalyes + 1
            
    
    ''' Function to parse no training set'''
    def parseno(self):
        nofp = open(self.notrainfile, "r")
        nolines = nofp.readlines()
        x = 0 
        nofp.close()
        for noline in nolines:                      
            elementlist = []                       
            #After 3 empty lines, new training pattern begins
            if (x == 28):
                x = 0
            if x < 25:
                temp = []
                temp.append(x)
                highcnt = 0 
                for element in range(0,10):                    
                    if noline[element] is '%':                        
                        elementlist.append(0)
                    else:
                        highcnt = highcnt + 1
                        elementlist.append(1)
                temp.append(highcnt)
                self.no[tuple(temp)] = self.no[tuple(temp)] + 1                
                self.originalno.append(elementlist)
            else:
                self.originalno.append("End")
            x = x + 1
            '''Check end of a pattern'''
            if (x == 25):
                self.totalno = self.totalno + 1        

    

    def printyesoriginal(self):
        x = 0
        for element in self.originalyes:
            if x == 28:
                x = 0
            print(x, *element)
            x = x + 1

    
    def printnooriginal(self):
        x = 0
        for element in self.originalno:
            if x == 28:
                x = 0
            print(x, *element)
            x = x + 1

    
    def priorcalculation(self):
        self.yesprior = self.totalyes/(self.totalyes + self.totalno)
        self.noprior =  self.totalno/(self.totalyes + self.totalno)
        

    
    def likelihoodcalculation(self,k):
        for key,val in  self.yes.items():
            self.yes[key] = (val + k)/(self.totalyes + k*11)
        for key,val in  self.no.items():
            self.no[key] = (val + k)/(self.totalno + k*11)
        

    def debugprint(self):
   
        print("yes")
        for key,val in  self.yes.items():            
            print(key,val)        
        print("no")
        for key,val in  self.no.items():
            print(key,val)        
        print("priors")
        print(self.yesprior,self.noprior)        
        print("Total Yes = ", self.totalyes)
        print("Total No = ", self.totalno)

    

