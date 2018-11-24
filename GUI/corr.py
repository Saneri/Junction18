import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def loadData(df):
    out = []
    
    cols = list(df.columns)
    cols.pop(0)

    for index, row in df.iterrows():
        r = []
        for c in cols:
            vals = row[c][1:-1].split(",")
            vals = [int(x) for x in vals]
            r.append(vals)
        out.append(r)
    return out

def dist(a, b):
    (ax,ay,az) = a
    (bx,by,bz) = b

    dx = (ax-bx)
    dy = (ay-by)
    dz = (az-bz)
    return np.sqrt(dx*dx + dy*dy + dz*dz)

if __name__=="__main__":
    df1 = pd.read_csv("malli.csv")
    df2 = pd.read_csv("testi.csv")
    
    d1 = loadData(df1)
    d2 = loadData(df2)
    #print(d1)

    diff = np.zeros((len(d1),len(d1[0])))

    (X,Y) = diff.shape

    for i in range(X):
        for j in range(Y):
            diff[i][j] = dist(d1[i][j],d2[i][j])


    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(diff)
    plt.show()
    

