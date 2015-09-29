from scipy.integrate import *
import numpy as np

class Coefficients:
	"""Coefficients of FP equetaion."""
	def __init__(self, E, params):
		self.ll = 0.0; 	self.E = E
		self.uls = np.sqrt(params.delta*params.gamma)*self.E
		self.a = 1.138; self.b = 0.01328
		self.c = 0.21226; self.d = 0.19553
		self.dx = self.uls[0]/200.0
		self.setup(params)
	
	def setup(self, params):
		self.factor = None

	def eval(self):
		self.Value = []

class IntegralCoefficients(Coefficients):
	def B(self, x):
		return (self.b + self.d*x**(0.5-self.c) + x**(1.0-self.c))

	def C(self, x):
		return (self.b*self.c + 0.5*self.d*x**(0.5-self.c) + x**(1.0-self.c))

	def h(self, x):
		return np.log(1+self.a*x)/self.B(x) + self.a*x/(self.B(x)*(1+self.a*x)) - np.log(1+self.a*x)*self.C(x)/(self.B(x))**2

	def I1factor(self):
		numerator = (self.h(0.0) + (1 - self.c)*self.h(self.dx))*self.dx**(1.0 - self.c)
		denominator = (2.0 - self.c)*(1.0 - self.c)
		return numerator/denominator

class AlphaCoeff(IntegralCoefficients):
	def setup(self, params):
		self.factor = params.targetdensity*np.pi*params.AE**2
		self.delta = params.delta; self.gamma = params.gamma
		self.eta = params.m[1]/params.m[0]


	def cosTheta(self, x):
		return (0.5*((1 - x)**(0.5) + (1 - self.eta*x)*(1 - x)**(-0.5)))
		
	def integrand(self, x, e):
		t = x**2/(self.delta*e**2)
		return (1 - self.cosTheta(t))*self.h(x)/(x**(2+self.c))
		
	def eval(self):
		res = []
		for i in range(len(self.uls)):
			I1 = self.a/(2*self.delta*(self.E[i])**2)*self.I1factor()
			res.append(quad(self.integrand, self.dx, self.uls[i], args=(self.E[i]))[0])
		self.Value = self.factor*np.asarray(res)

		
class QCoeff(IntegralCoefficients):
	def setup(self, params):
		self.uls = np.sqrt(params.delta*params.gamma)*self.E
		self.factor = params.targetdensity*np.pi*params.AE**2/(2*params.delta**2)
		
	def integrand(self, x):
		return x**(2.0-self.c)*self.h(x)

	def eval(self):
		res = []
		for e in self.uls:
			res.append(quad(self.integrand, 0, e)[0])
		self.Value =  self.factor*np.asarray(res)/self.E**2

class SnCoeff(IntegralCoefficients):
	def setup(self, params):
		self.dx = self.uls[0]/200.0
		self.factor = params.targetdensity*np.pi*params.AE**2/(2*params.delta)
		
	def integrand(self, x):
		return self.h(x)/x**self.c

	def eval(self):
		res = []
		for e in self.uls:
			dx = e/200.0
			I1 = self.I1factor()
	                res.append(I1 + quad(self.integrand, self.dx, e)[0])
		self.Value = self.factor*np.asarray(res)/self.E

from scipy.interpolate import interp1d

class SeCoeffSRIM(Coefficients):
	def __init__(self, nnodes, params, interp = True):
#		self.Value = []
		self.numnodes = nnodes
		self.ESRIM = params.ESRIM
		self.SESRIM = params.SESRIM
		self.Emin = min(self.ESRIM)
		self.Emax = max(self.ESRIM)
		if interp:
			self.E = np.linspace(self.Emin, self.Emax, self.numnodes)
		else:
			self.E = np.array(self.ESRIM)

	def eval(self):
		f = interp1d(self.ESRIM, self.SESRIM)
		self.Value = f(self.E)

import re

class Parameters:
	"""Physical parameters"""
	
	def __init__(self, filename, targetdensity = 0.05):
		self.targetdensity = targetdensity
		self.filename = filename
		self.parsefile()
		self.setup()
		
	def setup(self):
		self.AE = 0.4685/(self.z[0]**0.23 + self.z[1]**0.23)
		self.A0 = 0.5292; self.e = 0.02721*self.A0
		self.delta = 0.25*self.m[1]*self.AE**2/(self.m[0]*self.z[0]**2*self.z[1]**2*self.e**2)
		self.gamma = 4*self.m[0]*self.m[1]/(self.m[0] + self.m[1])**2

	def parsefile(self):
		self.m = []; self.z = []
		ifile = open(self.filename, 'r')
		lines = ifile.readlines()
		ifile.close()

		ionpattern = r'Ion = .* \[(.*)\] , Mass = (.*) amu'
		for line in lines:
			matchion = re.search(ionpattern, line)
			if matchion:
				self.z.append(float(matchion.group(1).replace(',','.')))
				self.m.append(float(matchion.group(2).replace(',','.')))
		self.z.append(14.0)
		self.m.append(28.085)

		supattern = r'(.*)\s eV / Angstrom'
		for line in lines:
			matchsu = re.search(supattern,line)
			if matchsu:
				self.sefactor = matchsu.group(1).replace(',','.')

		sepattern = r'(.*)\s{1}(.*)eV\s{3}(.*)\s{2}(.*)\n'

		self.ESRIM = []
		self.SESRIM = []
		for line in lines[23:]:
			matchse = re.search(sepattern,line)
			if matchse:
				if(matchse.group(2) == 'M'):
					evalue = float(matchse.group(1).replace(',','.'))*1000
				elif(matchse.group(2) == 'k'):
					evalue = float(matchse.group(1).replace(',','.'))
				else:
					evalue = float(matchse.group(1).replace(',','.'))/1000

				sevalue = float(matchse.group(3).replace(',','.').split()[0])*float(self.sefactor)*1e-3
				self.ESRIM.append(evalue)
				self.SESRIM.append(sevalue)
