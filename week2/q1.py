import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import scipy.interpolate
import random




#Analytic Fit
x = np.arange(0,4.000001,.001)
alpha, a, k = -.75, 2, .1
y = a* sp.exp(alpha*x)+k
noise = np.empty((len(x)))
for i in range(len(noise)):
  noise[i] =random.gauss(0,.1)
generate  = y + noise

def peval(x,par):
  return par[1]*sp.exp(par[0]*x) + par[2] 

def analytic_residuals(par, x,y):
  alpha, a, k = par
  err = a*sp.exp(alpha*x)+k - y
  return err

"""
res = leastsq(analytic_residuals,[0,0,y.mean()], args=(x,generate), maxfev=10000)
print res[0]
#[-0.74517277  2.01169371  0.0940487 ]
#compare with
# [-.75, 2, .1]
plt.plot( x, generate,'g,',x,peval(x,res[0]),'r',x, y,'b')
plt.title('Least Squares Fit-Analytic')
plt.legend(['Noisy','Fit','True'])
plt.show()
"""

"""
#Cubic Spline Fit
tck = scipy.interpolate.splrep(x,generate,s=0)
x_new = np.arange(0,4.000001,.5)
spline_y = scipy.interpolate.splev(x_new, tck, der=0)
plt.plot( x, generate,'g,',x_new,spline_y,'r',x, y,'b')
plt.title('Cubic Spline on %d knots'%len(x_new-2))
plt.legend(['Noisy','Fit','True'])
plt.show()
"""

#Polynomial Fit
order0 = np.polyfit(x,y,deg=0)
order1 = np.polyfit(x,y,deg=1)
order2 = np.polyfit(x,y,deg=2)
zero = 0*x+order0[0]
first = order1[0]*x + order1[1]
second = order2[0]*x*x + order2[1]*x + order2[2]
plt.plot( x,second,x, first, x, zero,x, y)
plt.title('Polynomial Fits')
plt.legend(['Second Degree','First Degree','0 Degree','True'])
plt.show()


