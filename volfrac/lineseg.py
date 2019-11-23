#!/usr/bin/env python3
#==================================================================================
#   lineseg.py
#   ~~~~~~~~~~
#   A class for defining a line segment.
#   It consists of two points: the start point and the end point.
#==================================================================================

import numpy as np
import vector

class lineseg:
	
	def __init__(self, vs, ve):
		self.vs = vs
		self.ve = ve
	
	#--- Access
	#- Return the start point
	def start(self):
		return self.vs
	
	#- Return the end point
	def end(self):
		return self.ve

	#- Return the direction vector from the start point to the end point
	def dvec(self):
		return self.ve - self.vs

	#--- Helper functions
	#- Magnitude of the line segment
	def mag(self):
		return vector.mag(self.dvec())

	#- Check if the given point is on the line segment
	def onseg(self, p, Debug=False):
		ltot = self.mag()
		lps = vector.mag(p - self.vs)
		lep = vector.mag(self.ve - p)

		diff = ltot - (lps+lep)

		if Debug:
			print('Total length: ', ltot)
			print('s-p   length: ', lps)
			print('p-t   length: ', lep)
			print('diff        : ', diff)

		if vector.mag(diff)<1e-10:
			return True
		else:
			return False
	
	# I/O
	def __str__(self):
		return (str(self.vs) + ' - ' + str(self.ve))

def intersect(ls1, ls2, Debug=False):
	p = ls1.start()
	q = ls2.start()
	r = ls1.dvec()
	s = ls2.dvec()

	numu = vector.cross((q-p),r)
	den = vector.cross(r,s)

	if Debug:
		print('p:', p)
		print('q:', q)
		print('r:', r)
		print('s:', s)
		print('(q-p)xr = ', numu)
		print('rxs = ', den)

	psect = vector.vector([None]*p.size())
	intersected = False

	if vector.mag(den)<1e-10:
		if vector.mag(numu)<1e-10:
			# Colinear
			pass
		else:
			# Parallel and non-intersecting
			pass
	else:
		numt = vector.cross((q-p),s)

		t = numt/den
		u = numu/den

		if Debug:
			print('t:', t)
			print('u:', u)

		if (u>=0 and u<=1) and (t>=0 and t<=1):
			pintt = p + r*t
			pintu = q + s*u

			if Debug:
				print('p+rxt =', pintt)
				print('q+sxu =', pintu)

			if vector.mag(pintt-pintu)<1e-10:
				psect = pintt
				intersected = True

			else:
				# Two lines are not parallel but do not intersected
				pass
	
	return intersected, psect
