from tasks import *
from taskinit import *
import casac
import pylab as pl
import sys
from optparse import OptionParser
import blib
reload(blib)

def fwhm(x, y, dx=0.001):
	'''
	Finds the FWHM for the profile y(x), with accuracy dx=0.001
	'''
	popt, pcov = curve_fit(blib.gauss2, x, y);
	xx = pl.arange(pl.amin(x), pl.amax(x)+dx, dx);
	ym = blib.gauss2(xx, popt[0], popt[1], popt[2], popt[3], popt[4], popt[5])
	hm = pl.amax(ym/2.0);
	y_diff = pl.absolute(ym-hm);
	y_diff_sorted = pl.sort(y_diff);
	i1 = pl.where(y_diff==y_diff_sorted[0]);
	i2 = pl.where(y_diff==y_diff_sorted[1]);
	fwhm = pl.absolute(xx[i1]-xx[i2]);
	pl.plot(xx, ym, label='xxdflaj,ym');
	return hm, fwhm

def gauss2(x, a, x0, s, a2, x02, s2):
	'''
	Returns two Gaussians with amp,mean,std.dev given by (a, x0, s) and (a2, x02, s2).
	'''
	return a*np.exp(-(x-x0)**2/(2*s**2)) + a2*np.exp(-(x-x02)**2/(2*s2**2))


usage = "usage: %prog options \n Script to slice the major and minor axes of psfs, exports them to a plot file. \n"
parser = OptionParser(usage=usage);

# O1 for Option 
parser.add_option("-f", type = 'string', dest = 'f', default=None, 
	help = 'Name of imagefile to be sliced [None]');
parser.add_option("-t", type='float', dest='t', default=90., 
	help = 'Angle of Major Axis [90deg]')
parser.add_option("-d", type='float', dest='d', default=10., 
	help = 'Half-Width of slice in pixels [10]');
parser.add_option("-x", type='float', dest='x', default=0., 
	help = 'X - Central position of slice [0]');
parser.add_option('-y', type='float', dest='y', default=0., 
	help = 'Y - Central position of slice [0]');
parser.add_option('-o', type='string', dest='o', default=None, 
	help = 'Name of plotfile [None]');

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);


myimage = options.f;
deg2rad = pl.pi/180.;
theta = options.t;
D = options.d
x0 = options.x;
y0 = options.y;

def rotmax(theta):
	R = pl.array(([pl.cos(theta*deg2rad), -pl.sin(theta*deg2rad)],
		[pl.sin(theta*deg2rad),pl.cos(theta*deg2rad)]))
	return R;

ia.open(myimage);

pix = pl.absolute(pl.round_((ia.summary()['incr']*180./pl.pi)*3600.)[0])

pl.figure(figsize=(10,5));

# Minor axis
pl.subplot(121);
xmin1 = pl.array(([D,0]));
xmin1r = pl.dot(rotmax(theta), xmin1);
xmin2 = pl.array(([-D,0]));
xmin2r = pl.dot(rotmax(theta), xmin2);
x1 = x0+xmin1r[0]; 
x2 = x0+xmin2r[0];
y1 = y0+xmin1r[1]; 
y2 = y0+xmin2r[1];
minor_slice = ia.getslice([x1, x2], [y1, y2])
x_minor = (minor_slice['distance']*pix-D*pix);
y_minor = minor_slice['pixel'];
pl.plot(x_minor,y_minor, color='black', ls='-', lw=1, label='Major-Axis');
hm_minor, f_minor, xf_minor, yf_minor = blib.fwhm(x_minor, y_minor);
pl.plot(xf_minor, yf_minor, 'k--', label='Fit')
pl.hlines(hm_minor, -f_minor/2, f_minor/2, color='gray', label='FWHM-Minor');
pl.xlim(pl.amin(x_minor), pl.amax(x_minor));
pl.ylim(pl.amin(y_minor)-0.1, pl.amax(y_minor)+0.1);
print f_minor;

# Major Axis
pl.subplot(122);
xmaj1 = pl.array(([0., D]));
xmaj1r = pl.dot(rotmax(theta), xmaj1);
xmaj2 = pl.array(([0., -D]));
xmaj2r = pl.dot(rotmax(theta), xmaj2);
j1 = x0+xmaj1r[0]; 
j2 = x0+xmaj2r[0];
k1 = y0+xmaj1r[1]; 
k2 = y0+xmaj2r[1];
major_slice = ia.getslice([j1, j2], [k1, k2])
x_major = major_slice['distance']*pix-D*pix;
y_major = major_slice['pixel'];
pl.plot(x_major, y_major, color='black', ls='-', lw=1, label='Major-Axis');
hm_major, f_major, xf_major, yf_major = blib.fwhm(x_major, y_major);
pl.plot(xf_major, yf_major, 'k--', label='Fit')
pl.hlines(hm_major, -f_major/2, f_major/2, color='gray', label='FWHM-Major');
print f_major; 
pl.xlim(pl.amin(x_major), pl.amax(x_major));
pl.ylim(pl.amin(y_major)-0.1, pl.amax(y_major)+0.1);
#pl.title("Cross-sections for "+options.f)
pl.xlabel('Offset [arcsec]');
pl.ylabel('Gain')
pl.legend();
pl.savefig(options.o, dpi=300)
pl.close();
ia.close();
pl.close();
#pl.savetxt(options.o.replace('.png','.txt'), zip(minor_slice['distance']*pix-D*pix, minor_slice['pixel']), fmt='%10.5f');


