import Training 
import NaiveBayesTest



maxaccuracy = 0
accuracylst = {}

#k in range (1,300,10) : higher accuracy

for k in range(1,100,5):

    T1 = Training.Training("yes_train.txt", "no_train.txt")
    T1.parseyes()
    T1.parseno()
    T1.priorcalculation()

    T1.likelihoodcalculation(k/10)
    
    #T1.debugprint()
    NB = NaiveBayesTest.NaiveBayesTest("yes_test.txt", "no_test.txt", T1)
    NB.parseyes()
    NB.parseno()
    #NB.printtestresults()
    print("Smoothing factor = ", k/10)
    a = NB.confusionmatrix()
    accuracylst[k/10] = a


print("Final accuracy")
print(accuracylst)


#NB.printyesoriginal()
#NB.printnooriginal()
