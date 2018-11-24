import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv2data as cc




class state():

    def __init__(self,pos,vel, F):
        self.pos = pos
        self.vel = vel
        self.F = F
        self.i = 0

    def getPos(self):
        return self.pos

    def getVel(self):
        return self.vel

    def getF(self):
        return (self.F[self.i,:] - self.F[0,:])

    def takeStep(self, integrator, step):
        if integrator == 'euler':
           eulerStep(self,step)
           self.i += 1


def eulerStep(state, step):

    R = state.getPos()
    V = state.getVel()
    F = state.getF()

    R_ = R + V.dot(step)
    V_ = V + F.dot(step)

    state.pos = R_
    state.vel = V_
    return True

def smoothen(vec, win = 9):
    vec2 = np.zeros(len(vec))
    s = 1.0/(win - 1)
    for i in range(int(win/2)):
        vec2[i] = vec[i]
    for i in range(int(win/2), len(vec) - int(win/2)):
        avg = 0
        for j in range(int(-win/2), int(win/2)):
            if j != 0:
                avg += s*vec[i + j]
        vec2[i] = avg
        #vec2[i] = 0.2*vec[i-2] + 0.3*vec[i-1] + 0.3*vec[i + 1] + 0.2*vec[i +2]

    return vec2

#if __name__=='__main__':

def getSpatial(fname = 'src/Mallisuoritus.csv'):

    df = pd.read_csv(fname)
    data = df.values[:, 0:3]
    data -= data[0, :]
    XX = data[:,0]
    YY = data[:,1].dot(-1)
    ZZ = data[:,2]
    #XX = smoothen(XX)
    #YY = smoothen(YY)
    #ZZ = smoothen(ZZ)
    #XX = smoothen(XX)
    #YY = smoothen(YY)
    #ZZ = smoothen(ZZ)

    data_smooth = np.transpose(np.array([XX,YY,ZZ]))
    r = np.array([0,0,0])
    v = np.array([0,0,0])

    S = state(r,v, data_smooth)

    R = []
    V = []

    for i in range(0,data.shape[0]):
        R.append(S.pos)
        V.append(S.vel)
        S.takeStep("euler", 1)

    R = np.asarray(R)
    V = np.asarray(V)


    Z0 = np.zeros(R.shape, dtype='int')

    out = {}
    out['S0'] = Z0
    out['S1'] = R.dot(0.1)

    #return out

    print(data.shape)

    fig = plt.figure()
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)

    ax1.plot(R)
    ax2.plot(V)
    ax3.plot(data - data[0,:])


    plt.show()

    return out

if __name__ == '__main__':
    getSpatial()
