'''
Python script to fit multiple Gaussian profiles to a 1D series.
Extracted from:
http://python4esac.github.io/fitting/examples1d.html
'''

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
import pylab as pl

def fwhm(x, y, dx=0.001):
	popt, pcov = curve_fit(func, x, y);
	xx = pl.arange(pl.amin(x), pl.amax(x)+dx, dx);
	ym = func(xx, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
	hm = pl.amax(ym/2.0);
	y_diff = pl.absolute(ym-hm);
	y_diff_sorted = pl.sort(y_diff);
	i1 = pl.where(y_diff==y_diff_sorted[0]);
	i2 = pl.where(y_diff==y_diff_sorted[1]);
	fwhm = pl.absolute(xx[i1]-xx[i2]);
	pl.plot(xx, ym, label='xx,ym');
	return hm, fwhm

def func(x, a, x0, s, a2, x02, s2):
    return a*np.exp(-(x-x0)**2/(2*s**2)) + a2*np.exp(-(x-x02)**2/(2*s2**2))

#TODO: Input file here
data = 'ska1-mid.NA.11km.2048in2asec.psf.gaumod.txt'
X = pl.loadtxt(data);
x = X[:,0];
y = X[:,1];
hm, f = fwhm(x, y);
pl.hlines(hm, -f/2, f/2);

pl.plot(x, y, label='x,y');
#pl.plot(xx, ym, label='xx,ym');
#pl.plot(x, yf, label='x,yf');
#pl.plot(x,r, label='x,r');
#pl.plot(x, resm, label='x,resm');
#pl.plot(x, yf, label='x,yf');
#pl.plot(x, y_diff);
pl.legend();
pl.savefig('gaufit_test.png');
pl.close();
