import ReadData 
import Perceptron 
from random import shuffle

class Classifier:

    def __init__(self, epoch = 1000, initwt =0, bias = 0, biasen = 0):

        self.epoch = epoch
        self.initwt = initwt
        self.bias = bias
        

        #required for confusion matrix calculation, key is (truelabel, predicted label) and value is number of occurences in test
        self.labeldict = {}

        #Read and store training data
        self.Tr = ReadData.ReadData("trainingimages.txt","traininglabels.txt")
        self.Tr.parsefiles()

        #Dictionary of perceptrons,
        self.dictpt = {}
        #Initialize 10 perceptrons
        for i in range(0,10):
            #id,bias,random wt or not
                p1 = Perceptron.Perceptron(i,self.initwt,self.bias,biasen)
                self.dictpt[i] = p1


    
    def runtraining(self):

        accuracy = []
        trlist = list(self.Tr.data.keys())

        for eachrun in range(0,self.epoch):
            #Shuffle the order of training data, randomizing input order
            shuffle(trlist)
            trlabeldict = {}

            alpha = 100 / (100 + eachrun + 1)
            
            for datakey in trlist:
                image = self.Tr.data[datakey]
                truelabel = self.Tr.label[datakey]

                res = []
                for i in range(0,10):
                    p1 = self.dictpt[i]
                    res.append(p1.classifyres(image))

                maxres = res[0]
                maxindex = 0
                #Find the maximum 
                for index in range(1,10):
                    if res[index] > maxres:
                        maxindex = index
                        maxres = res[index]
                
                prlabel = maxindex

                if (prlabel != truelabel):
                    self.dictpt[prlabel].weightdec(alpha,image)
                    self.dictpt[truelabel].weightinc(alpha,image)
            
            #Overall accuracy of training data
            tracc = 0
            #Run classifier on training data 
            for dkey in self.Tr.data.keys():
               
                image = self.Tr.data[dkey]
                truelabel = self.Tr.label[dkey]

                res = []
                for i in range(0,10):
                    p1 = self.dictpt[i]
                    res.append(p1.classifyres(image))
                
                maxres = res[0]
                maxindex = 0
                #Find the maximum 
                for index in range(1,10):
                    if res[index] > maxres:
                        maxindex = index
                        maxres = res[index]
                
                prlabel = maxindex 
                if (prlabel == truelabel):
                    tracc = tracc + 1

      
            
            #print accuracy of training data 
            print("epoch, accuracy", eachrun+1,tracc/len(trlist))
            '''if tracc/len(trlist) >= 0.998:
                break'''


                 


    

    def runtesting(self):
        #Read and store training data
        test = ReadData.ReadData("testimages.txt","testlabels.txt")
        test.parsefiles()

        #details for confusion matrix



        for datakey in test.data.keys(): 
            temp = []
            image = test.data[datakey]
            truelabel = test.label[datakey]
            temp.append(truelabel)
            res = []
            for i in range(0,10):
                p1 = self.dictpt[i]
                res.append(p1.classifyres(image))
            maxres = res[0]
            maxindex = 0
            #Find the maximum 
            for index in range(1,10):
                if res[index] > maxres:
                    maxindex = index
                    maxres = res[index]
                
            #prlabel = maxindex  
            temp.append(maxindex)  

            temptup = tuple(temp)
            self.labeldict[temptup] = self.labeldict.get(temptup,0) + 1


        #generate confusion matrix
        cm = []
        for i in range(0,10):  
            cmtemp = []         
            for j in range(0,10):
                temp = []
                temp.append(i)
                temp.append(j)
                temptup = tuple(temp)
                cmtemp.append(self.labeldict.get(temptup,0))
            cm.append(cmtemp) 
        
        #Print Confusion matrix
        cmnorm = []
        for row in cm:
            cmtemp = []
            s = sum(row)
            for element in row:
                cmtemp.append(element/s)
            cmnorm.append(cmtemp)
        tcacc = 0
        cmadd = 0
        for r in range(len(cmnorm)):
            for c in range(len(cmnorm[0])):
                cmadd = cmadd + cm[r][c]
                print ("%.3f" % cmnorm[r][c], end='  ')
                if (r == c):
                    tcacc = tcacc + cm[r][c]
            print('')

        print("Testing Overall accuracy = ", tcacc/len(test.data))
        print("total test data, cm sum ", len(test.data),cmadd )

        
        
        for row in cm:
            print(*row)
            

























