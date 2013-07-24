from tasks import *
from taskinit import *
import casac
import pylab as pl
import sys
from optparse import OptionParser
import blib
reload(blib)

usage = "usage: %prog options \n Script to slice the major and minor axes of psfs, exports them to a plot file. \n"
parser = OptionParser(usage=usage);

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
parser.add_option('--fit', type='string', default='True', 
	help = 'Fit for 2-Gaussian Model? [True]')

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

#if options.fit.upper()=='TRUE':
#	print options.fit
#	print 'yes', 
#	sys.exit(0);


myimage = options.f;
deg2rad = pl.pi/180.;
theta = options.t;
D = options.d
x0 = options.x;
y0 = options.y;

pl.figure(figsize=(10,5));

# Minor axis
pl.subplot(121);
pl.title('Minor Axis');
x_minor, y_minor = blib.imslice(myimage=myimage, v='minor', theta=theta, x0=x0, y0=y0, D=D);
pl.plot(x_minor,y_minor, color='black', ls='-', lw=1, label='Major-Axis');
if options.fit.upper()=='TRUE':
	hm_minor, f_minor, xf_minor, yf_minor = blib.fwhm_2gauss(x_minor, y_minor);
	pl.plot(xf_minor, yf_minor, 'k--', label='Fit')
	pl.hlines(hm_minor, -f_minor/2, f_minor/2, color='gray', label='FWHM-Minor');
else:
	hm_minor, f_minor = blib.fwhm(x_minor, y_minor);
	pl.hlines(hm_minor, -f_minor/2, f_minor/2, color='gray', label='FWHM-Minor');

pl.xlim(pl.amin(x_minor), pl.amax(x_minor));
pl.ylim(pl.amin(y_minor)-0.1, pl.amax(y_minor)+0.1);

# Major Axis
pl.subplot(122);
pl.title('Major Axis')
x_major, y_major =  blib.imslice(myimage=myimage, v='major', theta=theta, x0=x0, y0=y0, D=D);
pl.plot(x_major, y_major, color='black', ls='-', lw=1, label='Major-Axis');
hm_major, f_major, xf_major, yf_major = blib.fwhm_2gauss(x_major, y_major);
if options.fit.upper()=='TRUE':
	pl.plot(xf_major, yf_major, 'k--', label='Fit')
	pl.hlines(hm_major, -f_major/2, f_major/2, color='gray', label='FWHM-Major');
	pl.xlim(pl.amin(x_major), pl.amax(x_major));
else:
	hm_major, f_major = blib.fwhm(x_major, y_major);
	pl.hlines(hm_major, -f_major/2, f_major/2, color='gray', label='FWHM-Minor');
print f_major; 
pl.ylim(pl.amin(y_major)-0.1, pl.amax(y_major)+0.1);
pl.xlabel('Offset [arcsec]');
pl.ylabel('Gain')
pl.savefig(options.o, dpi=300)
pl.close();
#pl.savetxt(options.o.replace('.png','.txt'), zip(minor_slice['distance']*pix-D*pix, minor_slice['pixel']), fmt='%10.5f');


