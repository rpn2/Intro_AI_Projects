# Classifies digits based on pixel values, using Naive Bayes classification

import math
import csv


# Open the training data and put into a 2D array.
fname="trainingimages"
with open(fname) as f:
    trainingimages=f.readlines()

fname="traininglabels"
with open(fname) as f:
    traininglabels=f.readlines()

for i in range(len(traininglabels)):
    traininglabels[i] = int(traininglabels[i].rstrip())

#print (traininglabels)

# valueFrequency[i][j][c][f] Records how many times pixel i,j in the class c has a value of f



valueFrequency = [[[[0 for f in range(2)] for c in range(10)] for j in range(28)] for i in range(28)]
classFrequency = [0 for n in range(500)]


for row in range(len(trainingimages)):
    for col in range(len(trainingimages[row])):
        i = row%28
        j = col%28
        c = traininglabels[int(row/28)]
        f = 0
        if trainingimages[row][col] == '#' or trainingimages[row][col] == '+':
            f = 1
            
        valueFrequency[i][j][c][f] += 1
        classFrequency[c] += 1


# L is the laplacian smoothing factor.
L = 1;

# Given the class c, this object stores the probability that the pixel i,j has the value f
likelihood = [[[[0 for f in range(2)] for c in range(10)] for j in range(28)] for i in range(28)]
for i in range(28):
    for j in range(28):
        for c in range(10):
            for f in range(2):
                likelihood[i][j][c][f] = (valueFrequency[i][j][c][f] + L) / (classFrequency[c] + 2*L)
                if(j==0):
                    likelihood[i][j][c][f] = (valueFrequency[i][1][c][f] + L) / (classFrequency[c] + 2*L)
                if(j == 0 or j == 1):
                    print (i,j,c,f,likelihood[i][j][c][f])


prior = [classFrequency[c]/sum(classFrequency) for c in range(10)]
print (prior)

#------------------------------TESTING
fname="testimages"
with open(fname) as f:
    testimages=f.readlines()

fname="testlabels"
with open(fname) as f:
    testlabels=f.readlines()

# For each test image, store the class that is most likely to be.
predictedClasses = []
probability = [math.log(n) for n in prior]

maxMaxPosteriorProbability = [-99999 for c in range(10)]
#Used to find the most prototypical test image in each class
maxMaxPosteriorProbabilityRow = [0 for c in range(10)]

minMaxPosteriorProbability = [10000 for c in range(10)]
#Used to find the least prototypical test image in each class
minMaxPosteriorProbabilityRow = [0 for c in range(10)]

for row in range(len(testimages)):
    for col in range(len(testimages[0])):
        i = row%28
        j = col%28
        f = 0
        if not testimages[row][col] == ' ':
            f = 1
        for c in range(10):
            probability[c] += math.log(likelihood[i][j][c][f])
        #At the end of each image, store the calculated posterior probablities. Reset probability
        #Predict the class using the maximum probability (MAP)
        if(i == 27 and j==27):
            maxPosteriorProbability = max(probability)
            predictedClass = probability.index(maxPosteriorProbability)
            if(maxPosteriorProbability > maxMaxPosteriorProbability[predictedClass]):
                maxMaxPosteriorProbability[predictedClass] = maxPosteriorProbability
                maxMaxPosteriorProbabilityRow[predictedClass] = row
            if(maxPosteriorProbability < minMaxPosteriorProbability[predictedClass]):
                minMaxPosteriorProbability[predictedClass] = maxPosteriorProbability
                minMaxPosteriorProbabilityRow[predictedClass] = row
                
            predictedClasses.append(predictedClass)
            probability = [math.log(n) for n in prior]

print (predictedClasses)

print ("Most confident for each class:")
for n in range(len(maxMaxPosteriorProbabilityRow)):
    print (n,maxMaxPosteriorProbabilityRow[n])

print ("Least confident for each class:")
for n in range(len(minMaxPosteriorProbabilityRow)):
    print (n,minMaxPosteriorProbabilityRow[n])

# PRINT OUT CONFOIDENT AND LEAST CONFIDENT

for c in range(10):
    startingRow = maxMaxPosteriorProbabilityRow[c] - 27
    endingRow = maxMaxPosteriorProbabilityRow[c]
    for r in range(startingRow, endingRow+1):
        print (testimages[r], end='')
        
for c in range(10):
    startingRow = minMaxPosteriorProbabilityRow[c] - 27
    endingRow = minMaxPosteriorProbabilityRow[c]
    for r in range(startingRow, endingRow+1):
        print (testimages[r], end='')
            

## CALCULATE CLASSIFICATION RATES
classificationCorrect = [0 for c in range(10)]
classificationTotal = [0 for c in range(10)]

classificationRate = [0 for c in range(10)]

confusionMatrix = [[0 for c in range(10)] for r in range(10)]
for n in range(len(testlabels)):
    classificationTotal[int(testlabels[n])] += 1
    if(predictedClasses[n] == int(testlabels[n])):
        classificationCorrect[int(testlabels[n])] += 1
    confusionMatrix[int(testlabels[n])][predictedClasses[n]] += 1

# Turn confusion matrix into percentages (based on row)
for r in range(len(confusionMatrix)):
    totalInClass = sum(confusionMatrix[r])
    for c in range(len(confusionMatrix[0])):
        confusionMatrix[r][c] /= totalInClass
        confusionMatrix[r][c] = round(confusionMatrix[r][c], 3)


classificationRate = [100 * classificationCorrect[c]/classificationTotal[c] for c in range(10)]
overallAccuracy = 100 * (sum(classificationCorrect)/sum(classificationTotal))

print (classificationRate)
print (overallAccuracy)

for r in range(len(confusionMatrix)):
    for c in range(len(confusionMatrix[0])):
        print ("%.3f" % confusionMatrix[r][c], end='    ')
    print('')

# Calculate log likelihoods (2 for each pair) and log odds ratio
pairs = [[8,3],[5,3],[7,9],[4,9]]
logLikelihoodMap = [[[0 for col in range(28)] for  row in range(28)] for num in range(10)]
logOddsRatio = [[[0 for col in range(28)] for  row in range(28)] for pairs in range(4)]

for pair in pairs:
    actual = pair[0]
    predicted = pair[1]
    for i in range(28):
        for j in range(28):
            logLikelihoodMap[actual][i][j] = math.log(likelihood[i][j][actual][1])
            logLikelihoodMap[predicted][i][j] = math.log(likelihood[i][j][predicted][1])
            logOddsRatio[pairs.index(pair)][i][j] = math.log(likelihood[i][j][actual][1] / likelihood[i][j][predicted][1])

index = 0
for pair in pairs:
    index += 1
    with open(str("output" + str(index) + ".csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(logLikelihoodMap[pair[0]])
    index += 1
    with open(str("output" + str(index) + ".csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(logLikelihoodMap[pair[1]])
    index += 1
    with open(str("output" + str(index) + ".csv"), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(logOddsRatio[pairs.index(pair)])






            
