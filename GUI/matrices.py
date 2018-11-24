import numpy as np


class rot():
    def multiply(self,A, B):
        out = A.dot(B)
        return out

    mat = 0
    def __init__(self):
        self.mat = np.matrix([[1,0,0],[0,1,0],[0,0,1]])


    def __str__(self):
        out = ""
        for r in self.mat:
            for e in r:
                out += str(e)
                out += " "
            out += "\n"


        return out
    
    def set(self, M):
        self.mat = M

    def __mul__(self, M):
        return self.multiply(self.mat, M.mat)

    def shape(self):
        return self.mat.shape

class rotX(rot):
    def __init__(self,a):
        rot.__init__(self)
        self.mat = np.matrix([[1,0,0],[0,np.cos(a), -np.sin(a)],[0,np.sin(a),np.cos(a)]])

class rotY(rot): 
    def __init__(self,a):
        rot.__init__(self)
        self.mat = np.matrix([[np.cos(a),0,np.sin(a)],[0,1,0],[-np.sin(a),0,np.cos(a)]])


class rotZ(rot):

    def __init__(self,a):
        rot.__init__(self)
        self.mat = np.matrix([[np.cos(a), -np.sin(a), 0],[np.sin(a),np.cos(a), 0],[0,0,1]])

class affine(rot):
    mat = np.zeros((4,4))
    x = np.array([0,0,0,0])
    def __init__(self, R, x):
        xx,yy = R.shape()
        self.mat = np.zeros((4,4))
        el = 0
        for i in range(0,xx):
            for j in range(0,yy):
                self.mat[i][j] = R.mat.item(el)
                el+=1

        for i in range(0,3):
            self.mat[i][3] = x[i]
            self.mat[3][i] = 0

        self.mat[3][3] = 1
    
    def __mul__(self, x):
        if isinstance(x, np.ndarray):
            print("tick")
            return self.multiply(self.mat, x)
        else:
            return self.multiply(self.mat, x.mat)
    
    def orientation(self):
        out = np.array([])
        for i in range(0,3):
            row = np.array([])
            for j in range(0,3):
                row.append(self.mat[i][j])
            out.append(row)
        return out


