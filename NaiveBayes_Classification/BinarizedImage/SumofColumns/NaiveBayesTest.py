import math

'''Class for handling NaiveBayes Test'''
class NaiveBayesTest():

    def __init__(self, yestest,notest, trained):
        self.yestestfile = yestest
        self.notestfile  = notest
        #Key is test sample id and value is posterior calculation for yes and no
        self.yesposterior = {}
        self.noposterior = {}
        #Key is test sample id and value is true label
        self.truelabel = {}
        #Key is test sample id and value is test label
        self.testlabel = {}
        #Original training in 1,0 format
        self.originalyes = []
        self.originalno = []
        #Training class is instantiated to get access to priors and likelihood
        self.trained = trained
        #True counts
        self.yestrue = 0
        self.notrue = 0
        




    ''' Function to parse test set with true label : yes'''
    def parseyes(self):
        yesfp = open(self.yestestfile, "r")
        yeslines = yesfp.readlines()
        x = 0 
        yessum = math.log(self.trained.yesprior)
        nosum = math.log(self.trained.noprior)
        yesfp.close()
        for yesline in yeslines:                      
            elementlist = []
            #After 3 empty lines, new test pattern begins
            #Initialize the running sum to log(prior)
            if (x == 28):
                x = 0
                yessum = math.log(self.trained.yesprior)
                nosum = math.log(self.trained.noprior)
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
                 #Calculate sum of log of each row for both yes and no
                temp.append(highcnt)
                yessum = yessum + math.log(self.trained.yes[tuple(temp)])
                nosum = nosum + math.log(self.trained.no[tuple(temp)])
                self.originalyes.append(elementlist)
            else:
                self.originalyes.append("End")
            x = x + 1
            #End of a pattern
            #MAP decision calculation and record the true and test labels
            if (x == 25):
                self.yesposterior[self.yestrue] = yessum
                self.noposterior[self.yestrue]  = nosum
                self.truelabel[self.yestrue] = 'Yes'                
                if yessum >= nosum:
                    self.testlabel[self.yestrue] = 'Yes'
                elif yessum < nosum:
                    self.testlabel[self.yestrue] = 'No'              

                self.yestrue = self.yestrue + 1 
                 

    ''' Function to parse test set with true label : no'''
    def parseno(self):
        nofp = open(self.notestfile, "r")
        nolines = nofp.readlines()
        x = 0 
        yessum = math.log(self.trained.yesprior)
        nosum = math.log(self.trained.noprior)
        nofp.close()
        for noline in nolines:                      
            elementlist = []
            #After 3 empty lines, new test pattern begins
            #Initialize the running sum to log(prior)
            if (x == 28):
                x = 0
                yessum = math.log(self.trained.yesprior)
                nosum = math.log(self.trained.noprior)
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
                 #Calculate sum of log of each row for both yes and no
                temp.append(highcnt)
                yessum = yessum + math.log(self.trained.yes[tuple(temp)])
                nosum = nosum + math.log(self.trained.no[tuple(temp)])
                self.originalno.append(elementlist)
            else:
                self.originalno.append("End")
            x = x + 1
            #End of a pattern
            #MAP decision calculation and record the true and test labels
            if (x == 25):
                self.yesposterior[self.yestrue + self.notrue] = yessum
                self.noposterior[self.yestrue + self.notrue]  = nosum
                self.truelabel[self.yestrue + self.notrue] = 'No'                
                if yessum >= nosum:
                    self.testlabel[self.yestrue + self.notrue] = 'Yes'
                elif yessum < nosum:
                    self.testlabel[self.yestrue + self.notrue] = 'No'              

                self.notrue = self.notrue + 1 

                 
     
    def printtestresults(self):

        print(len(self.yesposterior), len(self.noposterior), len(self.testlabel), len(self.truelabel))
        for data in self.yesposterior.keys():
            print(data,self.yesposterior[data],self.noposterior[data],self.truelabel[data],self.testlabel[data])

    

    def confusionmatrix(self):
        yesyes = 0
        yesno = 0
        nono = 0
        noyes = 0
        confusionmatrix = []

        for data in self.truelabel.keys():
            if self.truelabel[data] == 'Yes' and self.testlabel[data] == 'Yes':
                yesyes = yesyes + 1
            elif self.truelabel[data] == 'Yes' and self.testlabel[data] == 'No':
                yesno = yesno + 1
            elif self.truelabel[data] == 'No' and self.testlabel[data] == 'No':
                nono = nono + 1
            else:
                noyes = noyes + 1
        
        yeslst = []
        yeslst.append(yesyes/self.yestrue)
        yeslst.append(yesno/self.yestrue)  

        nolst = []
        nolst.append(noyes/self.notrue)
        nolst.append(nono/self.notrue)

        confusionmatrix.append(yeslst)
        confusionmatrix.append(nolst)
        #yesrate = yesyes/self.yestrue
        #norate =  nono/self.notrue
        accuracy = (yesyes + nono)/ (self.notrue + self.yestrue)

        print("Accuracy Rate =  ",accuracy)
        print("ConfusionMatrix")
        for element in confusionmatrix:
            print(*element)

        return accuracy 
         
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
















