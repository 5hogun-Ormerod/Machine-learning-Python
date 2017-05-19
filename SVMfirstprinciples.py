import csv
import numpy as np
import scipy as sp
from scipy.optimize import least_squares

def SSE(Normb, X,y):
    Xmat = np.matrix(X)
    (N,d) = Xmat.shape
    M = 100
    b = Normb[-1]
    Norm = np.reshape(np.matrix(Normb[0:d]),(d,1))
    S = M*(sum(abs(Norm))-1)**2
    return S+ sum([max(0,y[k]*(Xmat[k]*Norm-b)) for k in range(N)])
    
X = np.random.random((1000,3))
Normb = np.random.random((4,1))
y = [-1 if X[k,0]+ X[k,1]+ X[(k,2)] > 3/2 else 1 for k in range(1000)]

R = sp.optimize.minimize(SSE,Normb,args=(X,y))


from sklearn import svm
clf = svm.SVC()
clf.fit(X,y)