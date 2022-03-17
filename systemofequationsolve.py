import numpy as np

#watch at 21:30 seconds
#https://www.youtube.com/watch?v=8f09fSCWhMM 
#https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html

#modeling a 3x3 set of linear equations, 3 unknowns
#solving for fx, fy, and Moment about xy axis 

a = np.array([[.9396,1,-0.906], [0.342,0,0.4226], [-8.457,0,9.2976]])
b = np.array([0,50,700])

x = np.linalg.solve(a,b)
print(x)

#checking to see that the solution is full ranked matrix 
np.allclose(np.dot(a, x), b)
