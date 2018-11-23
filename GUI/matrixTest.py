import numpy as np
import matrices as m

X = m.rotX(0.5)

X2 = m.rotX(0.1)

X3 = X*X2

x = np.array([1,0,0])
x2 = np.array([0,1,0])

A = m.affine(X, x)
#A2 = m.affine(X2,x2)

R = np.array([1,0,0,1])

R_ = A*R
print(A)
print(R_)
