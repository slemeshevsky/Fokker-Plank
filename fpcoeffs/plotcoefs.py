#!/usr/bin/env python
# -*- coding=utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)

import os, shutil, sys
try:
	dirname = sys.argv[1]; del sys.argv[1]
except:
	print "Directory with results doesn't specify: "
	print "Usage: computing.py dirname [nolog|logx|logy|loglog show|notshow]"
	print "Default values: . nolog notshow"
	print "Target is Si [Ion number = 14, Mass = 28.085 amu]"
	dirname = '.'
#	sys.exit(1)

logplot = 'nolog'
show = 'notshow'
while len(sys.argv) > 1:
	logplot = sys.argv[1]; del sys.argv[1]

os.chdir(dirname)
if(dirname=='.'):
	ifile = open('result.txt','r')
else:
	ifile = open(dirname+'.txt','r')
data = np.loadtxt(ifile, comments='//', skiprows=2)
ifile.close()

[E, alpha, beta, q] = np.hsplit(data,4)

if(logplot=='nolog'):
	plt.plot(E, q, label = '$Q(E)$')
	plt.plot(E, beta, label = "$\\beta(E)$")
	plt.plot(E, alpha, label = '$\\alpha(E)$')
elif(logplot=='loglog'):
	plt.loglog(E, q, label = '$Q(E)$')
	plt.loglog(E, beta, label = "$\\beta(E)$")
	plt.loglog(E, alpha, label = '$\\alpha(E)$')
elif(logplot=='logx'):
	plt.semilogx(E, q, label = '$Q(E)$')
	plt.semilogx(E, beta, label = "$\\beta(E)$")
	plt.semilogx(E, alpha, label = '$\\alpha(E)$')
elif(logplot=='logy'):
	plt.semilogy(E, q, label = '$Q(E)$')
	plt.semilogy(E, beta, label = "$\\beta(E)$")
	plt.semilogy(E, alpha, label = '$\\alpha(E)$')
else:
	print 'Unknown option for plotting'
	sys.exit(1)

plt.xlabel(u'$E$, кэВ')
plt.title(u'Зависимости коэффициентов Фоккера---Планка')
plt.legend(loc='best')
if(dirname=='.'):
	plt.savefig('result_'+logplot+'.pdf')
else:
	plt.savefig(dirname+'_'+logplot+'.pdf')
plt.close()
