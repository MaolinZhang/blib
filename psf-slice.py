from tasks import *
from taskinit import *
import casac
import pylab as pl
import sys
from optparse import OptionParser
import blib
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


#myimage = 'SKA1-Mid.NA.11km.psf'
#myimage = 'SKA1-Mid.NA.11km.psf.gaussmodel'
#myimage='SKA1-Mid.NA.image';
#myimage = "Gaussian.im"
myimage = options.f;

deg2rad = pl.pi/180.;
#theta = 90.+71.;
theta = options.t;
#D = 100.;
D = options.d
#x0 = 2048;
x0 = options.x;
#y0 = 2048;
y0 = options.y;
#fwhm_major = 1.15092*60.;
#fwhm_minor = 0.93785*60.;


def rotmax(theta):
	R = pl.array(([pl.cos(theta*deg2rad), -pl.sin(theta*deg2rad)],
		[pl.sin(theta*deg2rad),pl.cos(theta*deg2rad)]))
	return R;

ia.open(myimage);

pix = pl.absolute(pl.round_((ia.summary()['incr']*180./pl.pi)*3600.)[0])

xmaj1 = pl.array(([D,0]))#, [x0-D,y0]));
xmaj1r = pl.dot(rotmax(theta), xmaj1);
xmaj2 = pl.array(([-D,0]))#, [x0-D,y0]));
xmaj2r = pl.dot(rotmax(theta), xmaj2);
x1 = x0+xmaj1r[0]; 
x2 = x0+xmaj2r[0];
y1 = y0+xmaj1r[1]; 
y2 = y0+xmaj2r[1];

major_slice = ia.getslice([x1, x2], [y1, y2])

pl.plot(major_slice['distance']*pix-D*pix, major_slice['pixel'])#, label='Major-Axis');

#fmaj = sd.fitter();
#f.set_data(xdat = major_slice['distance']*pix-D*pix, ydat =major_slice['pixel']);
#f.set_function(gauss=2)
#f.fit()

#x = [x0+xmaj1r[0],x0+xmaj2r[0]]
#y = [y0+xmaj1r[1],y0+xmaj2r[1]]
#pl.plot(x, y);


xmin1 = pl.array(([0., D]))#, [x0-D,y0]));
xmin1r = pl.dot(rotmax(theta), xmin1);
xmin2 = pl.array(([0., -D]))#, [x0-D,y0]));
xmin2r = pl.dot(rotmax(theta), xmin2);
j1 = x0+xmin1r[0]; 
j2 = x0+xmin2r[0];
k1 = y0+xmin1r[1]; 
k2 = y0+xmin2r[1];
minor_slice = ia.getslice([j1, j2], [k1, k2])


#minor_slice = ia.getslice([x0+xmin1r[0], y0+xmin1r[1]],
#	[x0+xmin2r[0], y0+xmin2r[1]])
#minor_slice = ia.getslice([x0+xmin2r[0], y0+xmin2r[1]], [x0+xmin1r[0], y0+xmin1r[1]])

pl.plot(minor_slice['distance']*pix-D*pix, minor_slice['pixel'], ls='--', lw=1)#, label='Minor-Axis');
#pl.hlines(0.5, 0-fwhm_major, 0+fwhm_major);
#x = [x0+xmin1r[0],x0+xmin2r[0]]
#y = [y0+xmin1r[1],y0+xmin2r[1]]
#pl.plot(x, y);
#pl.plot(2048, 2048, 'ko');
pl.xlim(-D, D);
#pl.legend();
pl.title("Cross-sections for "+options.f)
pl.xlabel('Offset [arcsec]');
pl.ylabel('Gain')
pl.savefig(options.o, dpi=300)
pl.close();
#pl.close();
ia.close();
pl.savetxt(options.o.replace('.png','.txt'), zip(minor_slice['distance']*pix-D*pix, minor_slice['pixel']), fmt='%10.5f');


