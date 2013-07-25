from tasks import *
from taskinit import *
import casac
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as mpl
import pylab as pl
global deg2rad
deg2rad = pl.pi/180.;
import blib
reload(blib)
import sys
from optparse import OptionParser

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# O1 for Option 
parser.add_option("-p", type='string', dest='p', default=None, 
	help='Name of PSF Image [None]')
parser.add_option('-f', type='string', dest='f', default=None, 
	help = 'Name of Fit to PSF [None]');
parser.add_option("-x", type='float', dest='x', default=0., 
	help = 'X - Central position of slice [0]');
parser.add_option('-y', type='float', dest='y', default=0., 
	help = 'Y - Central position of slice [0]');
parser.add_option("-t", type='float', dest='t', default=90., 
	help = 'Angle of Major Axis [90deg]')
parser.add_option('-o', type='string', dest='o', default=None, 
	help = 'Name of plotfile [None]');
parser.add_option('-d', type='float', dest='d', default=60., 
	help = 'Length of slice in pixels [60]')
(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);


#psf_file = 'ska1-mid.UN.11km.psf';
psf_file = options.p;
#fit_file = 'ska1-mid.UN.11km.psf.mod'
fit_file = options.f;
x0 = options.x;
y0 = options.y;
pa = options.t;
D = options.d;
x_psf_major, y_psf_major = blib.imslice(psf_file, v='major', theta=pa, x0=x0, y0=y0, D=D);
hm_psf_major, fwhm_psf_major = blib.fwhm(x_psf_major, y_psf_major);
x_psf_minor, y_psf_minor = blib.imslice(psf_file, v='minor', theta=pa, x0=x0, y0=y0, D=D);
hm_psf_minor, fwhm_psf_minor = blib.fwhm(x_psf_minor, y_psf_minor);
print "PSF FWHM {0:.3f}arcsec by {1:.3f}arcsec" .format(fwhm_psf_major[0], fwhm_psf_minor[0])

pl.subplot(121);
pl.plot(x_psf_major, y_psf_major, 'k-');
pl.subplot(122);
pl.plot(x_psf_minor, y_psf_minor, 'k-');

x_fit_major, y_fit_major = blib.imslice(fit_file, v='major', theta=pa, x0=x0, y0=y0, D=D);
hm_fit_major, fwhm_fit_major = blib.fwhm(x_fit_major, y_fit_major);
x_fit_minor, y_fit_minor = blib.imslice(fit_file, v='minor', theta=pa, x0=x0, y0=y0, D=D);
hm_fit_minor, fwhm_fit_minor = blib.fwhm(x_fit_minor, y_fit_minor);
print "FIT FWHM {0:.3f}arcsec by {1:.3f}arcsec" .format(fwhm_fit_major[0], fwhm_fit_minor[0])

pl.subplot(121);
pl.plot(x_fit_major, y_fit_major, ls='-', color='gray');
pl.subplot(122);
pl.plot(x_fit_minor, y_fit_minor, ls='-', color='gray');
pl.savefig(options.o, dpi=300);
pl.close();
