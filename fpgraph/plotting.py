#!/usr/bin/env python

import sys, math
import os, shutil

xmin = xmax = -1.0

try:
	dirname = sys.argv[1]; del sys.argv[1]
except IndexError:
	print 'Directory name is not specified!'
	print 'Usage:', sys.argv[0], ' fulldirname [xmin xmax]'
	sys.exit(1)

while len(sys.argv) > 1:
	xmin = float(sys.argv[1]); del sys.argv[1]
	xmax = float(sys.argv[1]); del sys.argv[1]

infilename1 = "RANGE.txt"
infilename2 = "1D.txt"
infilename3 = "2D.txt"

outfilename1 = "rangedata.txt"
outfilename2 = "1Ddata.txt"
outfilename3 = "2Ddata.txt"

os.chdir(dirname)
try:
	ifile1 = open(infilename1, 'r')  # open file for reading
except:
	print "Cannot find file : ", infilename1, " containing results"; sys.exit(1)

try:
	ifile2 = open(infilename2, 'r')  # open file for reading
except:
	print "Cannot find file : ",infilename2, " containing results"; sys.exit(1)
try:
	ifile3 = open(infilename3, 'r')  # open file for reading
except:
	print "Cannot find file : ",infilename3, " containing results"; sys.exit(1)
	
data1 = ifile1.readlines()[37:]
ifile1.close()
data2 = ifile2.readlines()[2:];
ifile2.close()
data3 = ifile3.readlines()[2:];
ifile3.close()

depth1 = []; ions = []
for line in data1 :
	depthval, ionsval, recoilsval = line.split()
	depth1.append(float(depthval.replace(',','.'))) 
	ions.append(float(ionsval.replace(',','.'))*1e-8)

depth2 = []; ions2 = []
for line in data2 :
	depthval, sumw, ionsval = line.split()
	depth2.append(float(depthval))
	ions2.append(float(ionsval))

depth3 = []; ions3 = []
for line in data3 :
	depthval, sumw, ionsval = line.split()
	depth3.append(float(depthval))
	ions3.append(float(ionsval))
	
ofile1 = open(outfilename1,'w')

for i in range(len(depth1)) :
    ofile1.write('%g  %12.5e\n' % (depth1[i],ions[i]))
ofile1.close()

ofile2 = open(outfilename2,'w')
for i in range(len(depth2)) :
    ofile2.write('%g  %12.5e\n' % (depth2[i],ions2[i]))
ofile2.close()

ofile3 = open(outfilename3,'w')
for i in range(len(depth3)) :
    ofile3.write('%g  %12.5e\n' % (depth3[i],ions3[i]))
ofile3.close()

d = dirname.split('/')
outputgraphname =  d[len(d)-1]

# make file with gnuplot commands
f = open('result.gnuplot', 'w')
f.write("""
set terminal postscript eps enhanced
set output '%s.ps'
""" % outputgraphname)
if(xmin >=0.0 and xmax >= 0.0):
	f.write('set xrange [%g:%g]' % (xmin, xmax))
f.write("""
plot 'rangedata.txt' title 'SRIM' with linespoints lt rgb 'black', \
'1Ddata.txt' title '1D' with lines lt rgb 'green', \
'2Ddata.txt' title '2D' with lines lt rgb 'blue'
""")
f.close()

import commands
cmd = 'gnuplot -persist result.gnuplot'
failure, output = commands.getstatusoutput(cmd)
if failure:
    print 'running gnuplot failed\n%s\n%s' % \
	    (cmd, output);  sys.exit(1)

rmworkfiles = 'rm '+outfilename1+' '+outfilename2+' '+outfilename3+' result.gnuplot'
failure, output = commands.getstatusoutput(rmworkfiles)
if failure:
	print 'Cannot remove files\n%s\n%s' % \
		(cmd, output);  sys.exit(1)

createpdf = 'ps2pdf -dEPSCrop '+outputgraphname+'.ps'
failure, output = commands.getstatusoutput(createpdf)
if failure:
	print 'Cannont create PDF\n%s\n%s' % \
		(cmd, output);  sys.exit(1)
