#!/usr/bin/env python3

import numpy as np
import vector, lineseg

'''
A class for defining an arbitrary shape of a geometry
'''
class geometry:
	
	def getseg(self, ind):
		ps = self.pts[ind]
		pe = self.pts[ind+1]

		return lineseg.lineseg(ps, pe)
	
	def getsegs(self):
		ls = []
		for i in range(0, self.size()):
			ls.append(self.getseg(i))
		return ls

	def __init__(self, *arg):
		self.pts = []
		if isinstance(arg[0], str):
			f = open(arg[0], 'r')
			lines = f.readlines()

			for line in lines:
				vl = line.split()
				for i in range(0, len(vl)):
					vl[i] = float(vl[i])
				self.pts.append(vector.vector(vl))
		elif isinstance(arg[0], list):
			self.pts = arg[0]
		else:
			for p in arg[0]:
				self.pts.append(p)

		self.size_ = len(self.pts)

		self.pts.append(self.pts[0])

		self.ls = self.getsegs()
	
	def __str__(self):
		s = str(len(self.pts)) + '\n(\n'
		for p in self.pts:
			s += str(p) + '\n'
		s += ')'

		return s
	
	def size(self):
		return self.size_
	
	def totalSize(self):
		return self.size_ + 1
	
	def segments(self):
		return self.ls
	
	def inside(self, p):
		ldet = lineseg.lineseg(p, vector.vector(p.x()+1e5, p.y()))
		nsects = 0
		psects = []

		for l in self.ls:
			isectd, psect = lineseg.intersect(ldet, l)

			if isectd:
				append = False
				if len(psects)>0:
					for pchk in psects:
						chk = vector.mag(pchk - psect)
						if chk > 1e-10:
							append = True
				else:
					append = True
				
				if append:
					nsects += 1
					psects.append(psect)

		if nsects % 2 == 0:
			return False
		else:
			return True
	
	def intersect(self, lseg):
		isectd = False
		psect = None
		indsect = -1

		iseg = 0
		for l in self.segments():
			isectd, psect = lineseg.intersect(lseg, l)

			if isectd:
				indsect = iseg
				break

			iseg += 1

		return isectd, psect, indsect

'''
A class for defining a cell
'''
class cell:
	
	def __init__(self, *pts):
		self.pts = []
		self.fl = []
		
		if isinstance(pts[0], list):
			self.pts = pts
		else:
			for p in pts:
				self.pts.append(p)

		self.size_ = len(self.pts)

		self.pts.append(self.pts[0])

		for i in range(0, self.size_):
			self.fl.append(lineseg.lineseg(self.pts[i], self.pts[i+1]))

	#--- Access
	def points(self, closed = True):
		if closed:
			return self.pts
		else:
			return self.pts[:-1]
	
	def faces(self):
		return self.fl

	def size(self):
		return self.size_
	
	def totalSize(self):
		return self.size_ + 1

	def __str__(self):
		s = str(self.size()) + '\n(\n'
		for p in self.points():
			s += str(p) + '\n'
		s + ')'
		return s
	
	#--- Helper function
	def intersect(self, g):
		ninside = 0
		for p in self.points():
			if g.inside(p):
				ninside += 1

		if ninside == 0 or ninside == self.totalSize():
			return False
		else:
			return True
	
	def inside(self, g):
		ninside = 0
		for p in self.points():
			if g.inside(p):
				ninside += 1

		if ninside == self.totalSize():
			return True
		else:
			return False

	def getarea(self):
		sumA = 0.0
		for i in range(0, self.totalSize()-2):
			v1 = self.pts[i+1] - self.pts[0]
			v2 = self.pts[i+2] - self.pts[0]
			sumA += 0.5*vector.mag(vector.cross(v1, v2))

		return sumA

	def intersectedArea(self, g):
		if not self.intersect(g):
			return -1

		# search the pivot point
		ist = 0
		poly = []
		for i in range(0, self.size()):
			if g.inside(self.pts[i]):
				ist = i
				poly.append(self.pts[ist])
				break

			lseg = lineseg.lineseg(self.pts[i], self.pts[i+1])
			isectd, psect, iseg = g.intersect(lseg)
			if isectd:
				poly.append(psect)
				ist = i
				break

		# Walk along boundary of intersected area
		cag = geometry(self.points(False))
		for i in range(ist+1, self.size()+1):
			p = self.pts[i]

			f = lineseg.lineseg(self.pts[i-1], self.pts[i])
			isectd, psect, iseg = g.intersect(f)
			if isectd:
				piden = vector.mag(poly[-1]-psect)
				if piden>1e-10:
					poly.append(psect)

				for i in range(iseg+1, g.size()):
					pchk = g.pts[i]
					piden = vector.mag(poly[-1]-pchk)
					if cag.inside(pchk) and piden>1e-10:
						poly.append(pchk)

			piden = vector.mag(poly[-1]-p)
			if g.inside(p) and piden>1e-10:
				poly.append(p)

		# Estimate the area
		if len(poly) == 3:
			v1 = poly[1] - poly[0]
			v2 = poly[2] - poly[1]
			return 0.5*vector.mag(vector.cross(v1, v2))
		else:
			sumA = 0.0
			for i in range(0, len(poly)-2):
				v1 = poly[i+1] - poly[0]
				v2 = poly[i+2] - poly[0]
				sumA += 0.5*vector.mag(vector.cross(v1, v2))

			return sumA

'''
A class for defining a cartesian domain
'''
class cartesianDomain:
	
	def __init__(self, x, y, nx, ny):
		self.xl = np.linspace(-0.5*x, 0.5*x, nx+1)
		self.yl = np.linspace(-0.5*y, 0.5*y, ny+1)

	#--- Access
	def pt(self, i, j):
		return vector.vector(self.xl[i], self.yl[j])
	
	def ptlist(self):
		pts = [None]*self.size1D()

		ind = 0
		size = self.size()
		for i in range(0, size[0]):
			for j in range(0, size[1]):
				pts[ind] = self.pt(i,j)
				ind += 1

		return pts

	def size(self):
		return (len(self.xl), len(self.yl))
	
	def size1D(self):
		s = self.size()
		return s[0]*s[1]

	def flist(self):
		nx, ny = self.size()
		fl = []

		for i in range(0, nx):
			for j in range(0, ny):
				p1 = vector.vector(self.xl[i], self.yl[j])

				if i+1<nx:
					p2 = vector.vector(self.xl[i+1], self.yl[j])
					fl.append(lineseg.lineseg(p1, p2))

				if j+1<ny:
					p3 = vector.vector(self.xl[i], self.yl[j+1])
					fl.append(lineseg.lineseg(p1, p3))

		return fl
	
	def cell(self, i, j):
		p1 = vector.vector(self.xl[i], self.yl[j])
		p2 = vector.vector(self.xl[i+1], self.yl[j])
		p3 = vector.vector(self.xl[i+1], self.yl[j+1])
		p4 = vector.vector(self.xl[i], self.yl[j+1])

		return cell(p1, p2, p3, p4)

def geometryGenerator(fname, gtype, *arg):
	f = open(fname, 'w')

	if gtype == 'circle':
		r = arg[0]

		tht = 0.0
		dtht = 2*np.pi/180.0

		while True:
			x = r*np.cos(tht)
			y = r*np.sin(tht)
			f.write(str(x) + '\t' + str(y) + '\n')

			tht += dtht

			if tht >= 2*np.pi:
				break

	f.close()
