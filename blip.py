import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
import pylab as pl

def fwhm(x, y, dx=0.001):
	'''
	Finds the FWHM for the profile y(x), with accuracy dx=0.001
	'''
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

def gauss2(x, a, x0, s, a2, x02, s2):
	'''
	Returns two Gaussians with amp,mean,std.dev given by (a, x0, s) and (a2, x02, s2).
	'''
	return a*np.exp(-(x-x0)**2/(2*s**2)) + a2*np.exp(-(x-x02)**2/(2*s2**2))


