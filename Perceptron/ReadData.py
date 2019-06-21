# Classifies digits based on pixel values, using Naive Bayes classification

''' Reads and stores data
 Entire training data is a dictinary with index representing training data ID and value is 2D list of pixels'''
class ReadData:

    def __init__(self, imagefile, labelfile):

        self.data = {}
        self.label = {}
        self.imagefile = imagefile
        self.labelfile = labelfile

    def parsefiles(self):
        # Open the training data and put into a 2D array.
        fname=self.imagefile
        with open(fname) as f:
            trainingimages=f.readlines()
        fname=self.labelfile
        with open(fname) as f:
            traininglabels=f.readlines()

        for i in range(len(traininglabels)):
            self.label[i] = int(traininglabels[i].rstrip())
        
        valuearray = []
        k = 0
        index = 0
        for row in range(len(trainingimages)):  
            valcol = []  
            k = k + 1       
            for col in range(0,28):                
                f = 0
                if trainingimages[row][col] == '#' or trainingimages[row][col] == '+':
                    f = 1
                valcol.append(f)

            valuearray.append(valcol)
            #Reached end of image
            if k == 28:
                self.data[index] = valuearray
                k = 0
                index = index + 1
                valuearray = []


    def debugprint(self):

        print("Labels")
        print(self.traininglabel) 

        print("Data")
                
        for key,val in self.trainingdata.items():
            k = k + 1
            print("length = ", len(val))

            for element in val:
                print(*element)
            
            print("\n")

            
        
                














            
