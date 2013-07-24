from tasks import *
from taskinit import *
import casac
import sys
from optparse import OptionParser

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# O1 for Option 
parser.add_option("--ftag", type = 'string', dest = 'ftag', default=None, 
	help = 'Tag for psf files, blah.XX.psf');

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

def run_imfit(fname):
	imfit(imagename = fname, residual = fname+'.res', 
		model =fname+'.mod', estimates='gauss2estimates.txt', 
		logfile = fname+'.logfile')
for w in ['UN', 'NA', 'R0']:
	fname = options.ftag.replace('XX', w);
	#print fname
	run_imfit(fname);
#run_imfit('ska1-mid.NA.11km.psf');
#run_imfit('ska1-mid.R0.11km.psf');
