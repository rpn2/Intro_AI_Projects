import MarkovState 
import random
import Display

class GamePlay:
    def __init__(self, numtrials = 1000, numtest= 25, gamma = 0.3, epnum = 500, lrnum = 100):
        self.numtrials = numtrials
        self.gamma = gamma      
        #key is (state,action) tuple, value is qvalues. initially zero
        self.qtable = {}
        #key is (state,action) tuple, value is frequencies of occurence. initially zero
        self.Nsa ={}
        #Collision tracking
        self.success = {}
        self.epnum = epnum
        self.lrnum = lrnum
        self.numtest = numtest
        self.answer = 0

        #Display for graphics
        self.display = Display.Display()
        

    def QPlay(self):
        totalpositive = 0

        for trial in range(0,self.numtrials):
            if(trial %5000 ==0):
                print(trial)
            #learning rate decay
            C = self.lrnum
            #Initialize a game 
            #Ability to change reward,gridx,gridy
            MS = MarkovState.MarkovState(1,12,12)

            
            
            numpostive = 0
            self.epsilon = self.epnum/(self.epnum+1+trial)
            

            currentstate, currentreward = MS.currentstate()

            testtrial = 0
            if trial >= self.numtrials - self.numtest:
                self.display.initialize(MS, trial)
                testtrial = 1
           

            while(True):                
                action = self.bestaction(currentstate,testtrial)
                #Simulate single time-step
                MS.singlestep(action)

                # If we are running test trials, then display the games.
                if(testtrial == 1):
                    self.display.draw(MS, numpostive)

                
                nextstate, nextreward = MS.currentstate()
                #Update Q value only during trials
                if testtrial == 0:
                    temp = []
                    temp.append(currentstate)
                    temp.append(action)
                    temptuple = tuple(temp)
                    alpha = C/(C + self.Nsa.get(temptuple,0))
                    oldqval = self.qtable.get(temptuple,0)
                    maxqval = self.getmaxqval(nextstate)
                    #Q value update
                    self.qtable[temptuple] = oldqval + alpha*(nextreward + self.gamma* maxqval - oldqval)
                    self.Nsa[temptuple] = self.Nsa.get(temptuple,0) + 1
                currentstate = nextstate
                #determine action
                if (nextreward == -1):
                    break
                if (nextreward == +1):
                    numpostive = numpostive + 1
            
            #self.success[trial] = numpostive
            #Calculate running average of last 1000 trials
            #if numpostive > 0 and trial >= self.numtrials - 1000:
            if testtrial:
                totalpositive =  totalpositive  + numpostive


        print("Average hits= ",totalpositive/self.numtest)
        self.answer = totalpositive/self.numtest



                
            

    
    def getmaxqval(self,state):
        maxaction = 0
        temp = []
        temp.append(state)
        temp.append(maxaction)
        maxqvalue = self.qtable.get(tuple(temp),0)
        for action in [1,-1]:
            temp.pop()
            temp.append(action)
            temptuple = tuple(temp)
            if self.qtable.get(temptuple,0) >= maxqvalue:                
                maxqvalue = self.qtable.get(temptuple,0)

        return maxqvalue




    #Epsilon-greedy 
    def bestaction(self,state,testtrial):
        #For greedy approach, get max action and value       
        
        #Return random action
        #actions = [-1,0,1]
        #Exploration
        if (random.random() < self.epsilon and testtrial == 0):
            bestaction = random.randint(-1,1)
        else:
            #Exploitation
            temp = []
            temp.append(state)
            temp.append(0)
            maxaction = 0
            maxqvalue = self.qtable.get(tuple(temp),0)
            for action in [-1,1]:
                temp.pop()
                temp.append(action)
                temptuple = tuple(temp)
                if self.qtable.get(temptuple,0) >= maxqvalue:
                    maxaction = action
                    maxqvalue = self.qtable.get(temptuple,0)
            bestaction = maxaction

        return bestaction


            







            


                 






