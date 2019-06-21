import Classifier 

#epoch = 1000, initwt =0 or 1 (random initial, bias = 0 or 1(random initial), biasen = 0
#Bias, Nobias, initial value as 0 or random value for weights and bias have no signifcant effects
#Alpha is set to 10/(10+t) in Classifier, best setting found

SC = Classifier.Classifier(300, 1, 0, 0)

SC.runtraining()
SC.runtesting()