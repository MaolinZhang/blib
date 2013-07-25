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
parser.add_option("--ms", type = 'string', dest = 'ms', default=None, 
	help = 'Name of MS [None]');
parser.add_option("--uvrange", type = 'string', dest = 'uvrange', default=None, 
	help = 'uvrange [None]');
parser.add_option("--weight", type = 'string', dest = 'weight', default=None, 
	help = 'weight [None]');
parser.add_option("--nxy", type = 'int', dest = 'nxy', default=512, 
	help = 'Number of pixels in each direction [512]');
parser.add_option('--cell', type='string', dest='cell', default='1arcsec', 
	help = 'Pixel Size [1arcsec]');
parser.add_option('--robust', type='float', dest='robust', default=0.0, 
	help = 'Robust value If weight=\'briggs\' [0.0]');
parser.add_option("-o", type = 'string', dest = 'o', default=512, 
	help = 'Number of pixels in each direction [512]');


(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);



im.open(options.ms);
im.defineimage(nx = options.nxy, cellx = options.cell, celly = options.cell);
im.selectvis(uvrange=options.uvrange);
im.weight(type=options.weight, robust=options.robust);
im.approximatepsf(options.o);
im.close()
im.done();
