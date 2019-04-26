#!/usr/bin/env python3

import numpy as np
import vector, lineseg

class cartesianDomain:
	
	def __init__(self, x, y, nx, ny):
		self.xl = np.linspace(-0.5*x, 0.5*x, nx+1)
		self.yl = np.linspace(-0.5*y, 0.5*y, ny+1)

	# Access
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
