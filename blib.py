from tasks import *
from taskinit import *
import casac
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
import pylab as pl
global deg2rad
deg2rad = pl.pi/180.;

def fwhm(x, y, dx=0.001):
	'''
	Finds the FWHM for the profile y(x), with accuracy dx=0.001
	'''
	popt, pcov = curve_fit(gauss2, x, y);
	xx = pl.arange(pl.amin(x), pl.amax(x)+dx, dx);
	ym = gauss2(xx, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
	hm = pl.amax(ym/2.0);
	y_diff = pl.absolute(ym-hm);
	y_diff_sorted = pl.sort(y_diff);
	i1 = pl.where(y_diff==y_diff_sorted[0]);
	i2 = pl.where(y_diff==y_diff_sorted[1]);
	fwhm = pl.absolute(xx[i1]-xx[i2]);
	return hm, fwhm, xx, ym

def gauss2(x, a, x0, s, a2, x02, s2):
	'''
	Returns two Gaussians with amp,mean,std.dev given by (a, x0, s) and (a2, x02, s2).
	'''
	return a*np.exp(-(x-x0)**2/(2*s**2)) + a2*np.exp(-(x-x02)**2/(2*s2**2))

def rotmax(theta):
	R = pl.array(([pl.cos(theta*deg2rad), -pl.sin(theta*deg2rad)],
		[pl.sin(theta*deg2rad),pl.cos(theta*deg2rad)]))
	return R;


def imslice(myimage, v, theta, x0, y0, D):
	ia.open(myimage);
	pix = pl.absolute(pl.round_((ia.summary()['incr']*180./pl.pi)*3600.)[0])
	if v=='major':
		v = [0., D];
		v2 = [0., -D];
	if v=='minor':
		v = [D, 0];
		v2 = [-D, 0];
	x1 = pl.array((v));
	x1r = pl.dot(rotmax(theta), x1);
	x2 = pl.array((v2));
	x2r = pl.dot(rotmax(theta), x2);
	j1 = x0+x1r[0]; 
	j2 = x0+x2r[0];
	k1 = y0+x1r[1]; 
	k2 = y0+x2r[1];
	s = ia.getslice([j1, j2], [k1, k2])
	x = s['distance']*pix-D*pix;
	y = s['pixel'];
	ia.close();
	return x, y
