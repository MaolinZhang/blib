import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
import pylab as pl 
# Let's create a function to model and create data
def func(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

# Generating clean data
x = np.linspace(0, 20, 200)
y1 = func(x[np.where(x <= 10)], 1, 3, 1)
y2 = func(x[np.where(x > 10)], -2, 15, 0.5)

y = np.hstack([y1, y2])

# Adding noise to the data
yn = y + 0.2 * np.random.normal(size=len(x))
pl.savetxt('testdata.txt', zip(x,yn), fmt='%10.5f');


# Plot out the current state of the data and model
#fig = mpl.figure()
#ax = fig.add_subplot(111)
#ax.plot(x, y, c='k', label='Function')
#ax.scatter(x, yn)
#fig.savefig('model_and_noise_multiple.png')

## Executing curve_fit on noisy data
#popt, pcov = curve_fit(func, x, yn, p0=[-1, 15, 1])
#
##popt returns the best fit values for parameters of the given model (func)
#print popt
#
#ym = func(x, popt[0], popt[1], popt[2])
##ax.plot(x, ym, c='r', label='Best fit')
#
#popt, pcov = curve_fit(func, x, yn, p0=[1, 2, 1])
#ym2 = func(x, popt[0], popt[1], popt[2])
##ax.plot(x, ym2, c='b', label='Best fit')
#
#yt = ym+ym2;
#ax.plot(x, yt, c='k', ls='--', label='overall');
#ax.legend()
#fig.savefig('model_fit_multiple.png')
