# Pong Graphics Display
# Constructs a window and displays the current state of the game
# Also displays the trial number and number of hits so far

from graphics import *
import time

DISPLAY_SPEED = 50 #Hz (refresh rate in cycles per second (approx.)

class Display:

    def __init__(self):
        
        self.win = GraphWin("PONG", 600,600)
        self.win.setCoords(0,1,1,0)

        self.rect = Rectangle(Point(0, 0),Point(1, 0))
        self.cir = Circle(Point(0,0), .01)
        self.trial = Text(Point(.6,.05), "Trial: ")
        self.trial.draw(self.win)
        self.bounces = Text(Point(.2,.05), "Bounces: ")
        self.bounces.draw(self.win)

        self.leftWall = Rectangle(Point(0,0), Point(0.01,1))
        self.leftWall.setFill("black")
        self.leftWall.draw(self.win)

        


        self.paddley = 0
        self.ballx = 0
        self.bally = 0
        

    def initialize(self, markovState, trial):
        self.rect.undraw()
        self.rect = Rectangle(Point(.99, markovState.paddley),Point(1, markovState.paddley + markovState.paddleht))
        self.rect.setOutline('red')
        self.rect.setFill('red')
        self.rect.draw(self.win)

        self.cir.undraw()
        self.cir = Circle(Point(markovState.ballx,markovState.bally), .01)
        self.cir.setOutline('blue')
        self.cir.setFill('blue')
        self.cir.draw(self.win)

        self.paddley = markovState.paddley
        self.ballx = markovState.ballx
        self.bally = markovState.bally

        self.trial.setText(str("Trial "+str(trial)))
    def draw(self, markovState, bounces):
        
        self.rect.move(0, markovState.paddley - self.paddley)
        self.paddley = markovState.paddley
        """
        self.rect.undraw()
        self.rect = Rectangle(Point(.99, markovState.paddley),Point(1, markovState.paddley + markovState.paddleht))
        self.rect.setOutline('red')
        self.rect.setFill('red')
        self.rect.draw(self.win)
        """

        self.cir.move(markovState.ballx - self.ballx, markovState.bally - self.bally)
        self.ballx = markovState.ballx
        self.bally = markovState.bally

        self.bounces.setText(str("Bounces "+str(bounces)))

        time.sleep(1/DISPLAY_SPEED)
        
                           

        
        
