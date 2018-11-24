import pandas as pd
import numpy as np

def gencsv():
    X = range(100) + np.ones(100, dtype ='int')*50
    Y = range(100) + np.ones(100, dtype ='int')*50

    Z = np.ones(100,dtype='int')

    R = list(zip(X,Y,Z))

    Y0 = np.ones(100, dtype = 'int')*50
    X0 = np.zeros(100, dtype = 'int')
    R0 = list(zip(X0,Y0,X0))

    df = pd.DataFrame({'S0' : R0, 'S1' : R})
    
    print(df)
    df.to_csv('malli.csv')

def loadcsv():
    df = pd.read_csv('testi.csv')
    out = []
    for index, row in df.iterrows():
        out.append(row['S1'])
    print(out)
    return out
if __name__ == "__main__":
    gencsv()
    loadcsv()
