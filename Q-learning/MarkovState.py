'''Class that keeps track of Markov state
Assumptions : top of the screen is y =0, bottom of the scren is y = 1,
Top of the paddle can take 0 to 0.8'''

import random
import math
import Display
class MarkovState:
    #Initialize the statepsace variables
    def __init__(self, reward = 1, gridx = 12, gridy = 12):
        self.ballx = 0.5
        self.bally = 0.5
        self.velocityx = 0.03
        self.velocityy = 0.01
        self.paddleht = 0.2
        self.paddley = 0.5 - (self.paddleht/2.0)
        self.reward = reward
        self.ycolli = 0
        self.gx = gridx
        self.gy = gridy
        self.genreward = 0

        #discrete values
        self.dbx = 0
        self.dby = 0
        self.dvx = 0
        self.dvy = 0        
        self.dpy = 0

        
        
        


    #Code single unit time step. AI input is three actions for paddle : NOTHING (0), MOVE_UP (1), MOVE_DOWN(-1)
    def singlestep(self,AIinput):

        # Update the ball location
        self.ballx = self.ballx + self.velocityx
        self.bally = self.bally + self.velocityy

        #Update the paddle location

        #Move paddle up, if it goes out of top-screen, hold it at top-screen
        if AIinput == 1:
            self.paddley = self.paddley -0.04
            if self.paddley < 0:
                self.paddley = 0
        #Move paddle down, if it goes out of bottom-sceen, hold it at bottom-screen
        elif AIinput == -1:
            self.paddley = self.paddley +0.04
            if self.paddley > 0.8:
                self.paddley = 0.8
        #Do nothing
        else:
            self.paddley = self.paddley
        
        #Detect collision in Y axis
        self.ycolli = 0
        if self.bally >= self.paddley and self.bally <= self.paddley + self.paddleht:
            self.ycolli = 1
        
        #Check for bounce on other walls 
        if  self.bally < 0:
            self.bally = -self.bally
            self.velocityy = -self.velocityy
            self.genreward = 0
        elif self.bally > 1:
            self.bally = 2-self.bally
            self.velocityy = -self.velocityy
            self.genreward = 0
        elif self.ballx < 0:
            self.ballx = -self.ballx
            self.velocityx = -self.velocityx
            self.genreward = 0
        #Ball hit the paddle, reward is 1
        elif self.ballx >= 1  and self.ycolli ==1 :
            #bounce adjustments
            self.ballx = 2-self.ballx
            U = random.uniform(-0.015, 0.015)            
            self.velocityx = -self.velocityx + U
            #Check for limits of velocity x
            if self.velocityx >= 0 and self.velocityx < 0.03:
                self.velocityx = 0.03
            elif self.velocityx < 0 and self.velocityx > -0.03:
                self.velocityx = -0.03
            elif self.velocityx > 1.0:
                self.velocityx = 1
            elif self.velocityx < -1.0:
                self.velocityx = -1

            V = random.uniform(-0.03, 0.03)
            self.velocityy =  self.velocityy+ V
            if self.velocityy > 1.0:
                self.velocityy = 1.0
            elif self.velocityy < -1:
                self.velocityy = -1.0
            self.genreward = self.reward            
        #Ball did not hit paddle, reward is -1
        elif self.ballx > 1  and self.ycolli ==0 :
            self.genreward = -self.reward
        else:
            self.genreward = 0
           

    #Generate discrete values of continuous statepace
    def currentstate(self):
        self.dbx = min(self.gx-1, int(math.floor(self.ballx*self.gx)))
        self.dby = min(self.gy-1, int(math.floor(self.bally*self.gy)))
        
        if self.velocityx >=0:
            self.dvx = 1
        else:
            self.dvx = -1
        if abs(self.velocityy) < 0.0015:
            self.dvy = 0
        elif self.velocityy >=0:
            self.dvy = 1
        else:
            self.dvy = -1

        self.dpy = min(self.gy-1,int(math.floor(self.gy * self.paddley / (1 - self.paddleht))))
       

        #Terminal state
        if self.genreward < 0:
            self.dbx = self.gx
            self.dby = None
            self.dvx = None
            self.dvy = None        
            self.dpy = None

        return (self.dbx,self.dby,self.dvx,self.dvy,self.dpy),self.genreward
   


        









        













   




