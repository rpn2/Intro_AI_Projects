'''Class that defines the perceptron'''
import random
class Perceptron:

    #Contains a 2D array of weights
    def __init__(self, perceptronid,randomwt = 0,bias = 0, biasen = 0):

        #One perceptron for every class
        self.id = perceptronid
        self.biasen = biasen
        if bias == 0:
            self.bias = 0
        else:
            self.bias = random.random()

        if randomwt == 0:
            self.wtarr=[[0]*28 for i in range(28)]
        else:
            self.wtarr=[[random.random() for j in range(28)] for i in range(28)]

    

    def weightinc(self, alpha, trsample):
        if self.biasen:
            self.bias = self.bias + alpha 
        for i in range(0,28):
            for j in range(0,28):
                self.wtarr[i][j] = self.wtarr[i][j] + alpha*trsample[i][j]


    def weightdec(self, alpha, trsample):
        if self.biasen:
            self.bias = self.bias - alpha
        for i in range(0,28):
            for j in range(0,28):
                self.wtarr[i][j] = self.wtarr[i][j] - alpha*trsample[i][j]

    def classifyres(self,trsample):        
        res = self.bias
        for i in range(0,28):
            for j in range(0,28):
                res = res + self.wtarr[i][j] * trsample[i][j]
    
        return res










