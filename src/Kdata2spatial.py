import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class state():

    def __init__(self,pos,vel):
        self.pos = pos
        self.vel = vel

    def getPos(self):
        return self.pos

    def getVel(self):
        return self.vel

    def getF(self):
        return np.array([-1,0,2])

    def takeStep(self, integrator, step):
        if integrator == 'euler':
           eulerStep(self,step) 



def eulerStep(state, step):
    R = state.getPos()
    V = state.getVel()
    F = state.getF()

    R_ = R + V.dot(step)
    V_ = V + F.dot(step)

    state.pos = R_
    state.vel = V_
    return True


if __name__=='__main__':

    df = pd.read_csv('acceleration.csv')
    r = np.array([1,0,0])
    v = np.array([0,1,0])

    S = state(r,v)

    R = []

    for i in range(0,100):
        R.append(S.pos)
        S.takeStep("euler", 0.01) 

    XX = R[:][0]
    YY = R[:][1]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(R)
    plt.show()
