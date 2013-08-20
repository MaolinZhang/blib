import pylab as pl
from tasks import *
from taskinit import *
import casac
import sys
from optparse import OptionParser
import os
global options

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# O1 for Option 
parser.add_option("--tag", type = 'string', dest = 'tag', default=None, 
	help = 'Name of filetag [None]');

parser.add_option('--calls', '-c', type='string', dest='c', default=None, 
	help= "Routines to be called [None]")

parser.add_option("--kw", type='string', dest='kw', default=None, 
	help = "For imstatr, the statistic to be saved [None]");

parser.add_option("-o", type='string', dest='o', default = None, 
	help="Name of output file [None]");

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

def Fn(na=0.78, nc=1., D=13.5, Trx=20, L=1):
    A = pl.pi*pl.square(D/2.);
    numer = pl.sqrt(2)*k*Trx;
    denom = na*nc*A*pl.sqrt(L)
    dI = numer/denom;
    return dI;

def iv_ratio():
	tag = options.tag;
	vis = tag+'.ms';
	im = tag+'.im.image';
	vs = visstat(vis);
	ims = imstat(im);
	iv_r = vs['DATA']['stddev']/ims['sigma'];
	print "vs['stddev'] = " , vs['DATA']['stddev']
	print "ims['sigma'] = " , ims['sigma'];
	print iv_r;
	return iv_r;

def vis_sens():
	tag = options.tag;
	vis = tag+'.ms';
	im.open(vis);
	print im.sensitivity();
	im.close()

def jyscale():
	imagename = options.tag+'.im.image'; 
	bmaj = imhead(imagename=imagename,mode='get',hdkey='beammajor')
	bmin = imhead(imagename=imagename,mode='get',hdkey='beamminor')
	bmaj = qa.convert(bmaj, 'rad')['value']
	bmin = qa.convert(bmin, 'rad')['value']
	toJy =  (1.1331 * bmaj * bmin);
	ims = imstat(imagename);
	#scale = ims['max'][0]*toJy;
	scale = toJy;
	print "Jy/beam to Jy scale = %f" % scale;
	print scale;

def imstatr():
	tag = options.tag;
	c = 'ls -d '+tag;
	fnames = os.popen(c).read().split('\n');
	fnames = fnames[0:len(fnames)-1]
	q = [];
	Z = [];
	for f in fnames:
		s = imstat(f);
		q.append(s[options.kw]);
		Z.append(f+'\t'+str(s[options.kw]).replace(']','').replace('[','')+'\n');
	q = pl.array(q);
	#Z = zip(fnames, q);
	#print Z 
	f = open(options.o, 'w');
	for z in Z:
		f.write(z);
	f.close();
	return Z


if len(options.c)>0.:
	for sr in options.c.split(','):
		exec(sr+'()');

