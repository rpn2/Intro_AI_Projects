import GamePlay
import time

#Best settings :
#Settings for 12x12 grid totaltrails = 101000, testtrails = 1000, gamma = 0.2, epnum = 1000, lrnum = 10
#Settings for 18x18 grid, 250000,1000,0.2,1000,10 : Ans : 12.23 hits
#Settings for 16x16 grid, 175000,1000,0.2,1000,10 : Ans : 10.02 hits
gammaTest = [0.7]
epnumTest = [1000]
lrnumTest = [10]
for gamma in gammaTest:
    for epnum in epnumTest:
        for lrnum in lrnumTest:
            start_time = time.time()
            QL = GamePlay.GamePlay(101000,1000,gamma,epnum,lrnum)
            QL.QPlay();
            print("gamma: ",gamma," epnum: ",epnum," lrnum: ",lrnum," avg : ",QL.answer)
            print("Time: ",time.time() - start_time, " s")
