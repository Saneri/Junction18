import pandas as pd
import numpy as np

def gencsv():
    X = range(100)
    Y = range(100)
    Z = range(100)

    R = list(zip(X,Y,Z))

    X0 = Y0 = Z0 = np.zeros(100, dtype = 'int')
    R0 = list(zip(X0,X0,X0))

    df = pd.DataFrame({'S0' : R0, 'S1' : R})
    
    print(df)
    df.to_csv('testi.csv')

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
