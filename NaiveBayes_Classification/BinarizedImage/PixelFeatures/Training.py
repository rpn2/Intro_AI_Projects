
'''Class that describes the training process of given samples'''
class Training():

    def __init__(self, yestrain,notrain):
        self.yestrainfile = yestrain
        self.notrainfile  = notrain
        #likelihoods numerator is represented as key,value pairs
        self.yeshigh = {}
        self.yeslow = {}
        self.nohigh = {}
        self.nolow = {}
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
            for y in range(0,10):
                temp = []
                temp.append(x)
                temp.append(y)                
                self.yeshigh[tuple(temp)] = 0
                self.yeslow[tuple(temp)] = 0
                self.nohigh[tuple(temp)] = 0
                self.nolow[tuple(temp)] = 0
                
               
        

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
                for element in range(0,10):
                    temp = []
                    temp.append(x)
                    temp.append(element)
                    if yesline[element] is '%':
                        self.yeslow[tuple(temp)] = self.yeslow[tuple(temp)] + 1
                        elementlist.append(0)
                    else:
                        self.yeshigh[tuple(temp)] = self.yeshigh[tuple(temp)] + 1
                        elementlist.append(1)
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
        nofp.close()
        x = 0 
        for noline in nolines:                      
            elementlist = []
            #After 3 empty lines, new training pattern begins
            if (x == 28):
                x = 0
            if x < 25:
                for element in range(0,10):
                    temp = []
                    temp.append(x)
                    temp.append(element)
                    if noline[element] is '%':
                        self.nolow[tuple(temp)] = self.nolow[tuple(temp)] + 1
                        elementlist.append(0)
                    else:
                        self.nohigh[tuple(temp)] = self.nohigh[tuple(temp)] + 1
                        elementlist.append(1)
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
        for key,val in  self.yeshigh.items():
            self.yeshigh[key] = (val + k)/(self.totalyes + k*2)
        for key,val in  self.yeslow.items():
            self.yeslow[key] = (val + k)/(self.totalyes + k*2)
        for key,val in  self.nohigh.items():
            self.nohigh[key] = (val + k)/(self.totalno + k*2)
        for key,val in  self.nolow.items():
            self.nolow[key] = (val + k)/(self.totalno + k*2)
        

    def debugprintX(self):
   
        print("yeshigh")
        for key,val in  self.yeshigh.items():            
            print(key,val)
        print("yeslow")
        for key,val in  self.yeslow.items():
            print(key,val)
        print("nohigh")
        for key,val in  self.nohigh.items():
            print(key,val)
        print("nolow")
        for key,val in  self.nolow.items():
            print(key,val)
        print("priors")
        print(self.yesprior,self.noprior)        
        print("Total Yes = ", self.totalyes)
        print("Total No = ", self.totalno)

    def debugprint(self):
   
        print("yeshigh vs yeslow")
        for key,val in  self.yeshigh.items():            
            if val + self.yeslow[key] != 1.0:
                print(key,val,self.yeslow[key])
        print("nohigh vs nolow")
        for key,val in  self.nohigh.items():            
            if val + self.nolow[key] != 1.0:
                print(key,val,self.nolow[key])
        
        print("lengths = ", len(self.yeshigh),len(self.yeslow),len(self.nohigh),len(self.nolow) )
        print("priors")
        print(self.yesprior,self.noprior)        
        print("Total Yes = ", self.totalyes)
        print("Total No = ", self.totalno)


