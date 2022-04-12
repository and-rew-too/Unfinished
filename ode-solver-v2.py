
import plotly
import plotly.graph_objects as go
import numpy as np


#https://www.intmath.com/differential-equations/6-rc-circuits.php
# example 1 works
#https://lpsa.swarthmore.edu/NumInt/NumIntSecond.html##section10v
# example 2 has cos, doesn't work
# example 3 works


def ode45(f,x0,y0,xend,n):
    tstar = np.linspace(0, xend, n)
    n = len(tstar)
    #x = np.zeros((n, len(x0)))
    h = tstar[4] - tstar[3]
    ystar = [0]*(n+1)
    ystar[0] = y0
    h = tstar[2]-tstar[1]
    for i in range(1,n+1):
        x = tstar[i-1]
        k1 = h * f(x, ystar[i-1])
        k2 = h * f(x + h/2, ystar[i-1] + 0.5 * k1)
        k3 = h * f(x + h/2, ystar[i-1] + 0.5 * k2)
        k4 = h * f(x + h, ystar[i-1] + k3)
        ystar[i] = ystar[i-1] + (1/6)*(k1+k2+k2+k3+k3+k4)
        ####
        # k1 = f(x,ystar[i-1])
        # y1 = ystar[i-1]+k1*h/2
        # k2 = y1*(1-2*(x+h/2))
        # ystar[i] = ystar[i-1] + k2*h
    return tstar, ystar




def f(x, y):
    #return (100/5)-(y/(5*0.02)) #example 1
    return y*(1-2*x) #example 3
    #return -2*y-np.cos(4*x) #example 2
tstar, ystar = ode45(f, 0, 1, 3, 100) #100 or n is essentially h
print(ystar)
print(tstar)


fig = go.Figure()
fig.add_trace(go.Scatter(x=tstar, y=ystar,
                    mode='lines',
                    name='lines'))
fig.show()
