#!/usr/bin/env python
# -*- coding=utf-8 -*-

import numpy as np
from coeffs import *
import sys, math

try:
	dirname = sys.argv[1]; del sys.argv[1]
except:
	print "Directory with results doesn't specify: "
	print "Usage: computing.py dirname [nolog|logx|logy|loglog]"
	print "Default values: . nolog"
	print "Target is Si [Ion number = 14, Mass = 28.085 amu]"
	dirname = '.'
#	sys.exit(1)

import os, shutil

os.chdir(dirname)
filename = 'SRIMdata.txt'
nn = 1000

params = Parameters(filename)

Se = SeCoeffSRIM(nn,params,False)
Se.eval()

Sn = SnCoeff(Se.E, params)
Sn.eval()

q = QCoeff(Se.E, params)
q.eval()

alpha = AlphaCoeff(Se.E, params)
alpha.eval()

beta = Sn.Value + Se.Value
if(dirname=='.'):
	ofile = open('result.txt','w')
else:
	ofile = open(dirname+'.txt','w')
	
ofile.write('//\t'+dirname+'\t %g -- %g\n' % (min(alpha.E), max(alpha.E)))
ofile.write('Energy\t Alpha\t Beta\t Q\n')
np.savetxt(ofile,np.column_stack((alpha.E,alpha.Value,beta,q.Value)))
ofile.close()
