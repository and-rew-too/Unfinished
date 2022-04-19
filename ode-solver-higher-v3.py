import numpy as np
import pandas as pd
import plotly
import plotly.graph_objects as go


qstar = pd.DataFrame(np.zeros([3,101]))

y0 = pd.DataFrame(np.zeros([3,1]))
y0.iloc[:,0] = [0,-1,0]
print(y0)

A = pd.DataFrame(np.zeros([3,3]))
A.iloc[:,0] = [0,0,-4] #should be construction A from rows makes more sense mathematically
A.iloc[:,1] = [1,0,-6]
A.iloc[:,2] = [0,1,-4]
B = pd.DataFrame(np.zeros([3,1]))
B.iloc[:,0] = [0,0,1]

print(A.dot(B)) # this is how to matrix multiply within pandas

def ode45(x0,y0,xend,n):
    tstar = np.linspace(0, xend, n)
    n = len(tstar)
    h = tstar[4] - tstar[3]
    ystar = pd.DataFrame(np.zeros([3,101]))
    ystar[0] = y0
    h = tstar[2]-tstar[1]
    for i in range(1,n):
        #x = tstar[i-1]
        #k1 = h * f(x, ystar[i-1])
        #k2 = h * f(x + h/2, ystar[i-1] + 0.5 * k1)
        #k3 = h * f(x + h/2, ystar[i-1] + 0.5 * k2)
        #k4 = h * f(x + h, ystar[i-1] + k3)
        #ystar[:,i+1] = ystar[i-1] + (1/6)*(k1+k2+k2+k3+k3+k4)
        #no longer use f(x) now use matrix multiplications...
        k1 = A.dot(ystar.iloc[:,i-1]) + B.dot([1])
        q1 = ystar.iloc[:,i-1] + k1*h/2
        k2 = A.dot(q1) + B.dot([1]
        ystar.iloc[:,i] = ystar.iloc[:,i-1] + k2*h
        #print(k1)
        #print(ystar)
    return tstar, ystar

y0 = [0,-1,0]
tstar,ystar = ode45(0,y0,5,100)
fig = go.Figure()
fig.add_trace(go.Scatter(x=tstar, y=ystar.iloc[0,:],
                    mode='lines',
                    name='lines'))
fig.show()
