#!/usr/bin/env python

import numpy as np

class vector:
	# Constructor
	def __init__(self, *cmpt):
		if isinstance(cmpt[0], (list,)):
			self.v_ = cmpt[0]
		else:
			self.v_ = []
			for c in cmpt:
				self.v_.append(c)
		self.rank = 1
		self.dimension = len(self.v_)

	# Access methods
	def x(self):
		return self.v_[0]

	def y(self):
		return self.v_[1]

	def z(self):
		return self.v_[2]

	def size(self):
		return len(self.v_)
	
	def __str__(self):
		s = '( '
		for c in self.v_:
			s += str(c) + ' '
		s += ')'
		return s

	# Helper function
	def mag(self):
		s = 0.0
		for c in self.v_:
			s += c*c
		return np.sqrt(s)

	# Operator overloading
	def __add__(self, v2):
		vo = vector([None]*self.size())
		for i in range(0, self.size()):
			vo.v_[i] = self.v_[i] + v2.v_[i]
		return vo

	def __mul__(self, v2):
		vo = vector([None]*self.size())
		for i in range(0, self.size()):
			if isinstance(v2, vector):
				vo.v_[i] = self.v_[i] * v2.v_[i]
			else:
				vo.v_[i] = self.v_[i] * v2
		return vo

	def __sub__(self, v2):
		vo = vector([None]*self.size())
		for i in range(0, self.size()):
			vo.v_[i] = self.v_[i] - v2.v_[i]
		return vo

	def __truediv__(self, v2):
		vo = vector([None]*self.size())
		for i in range(0, self.size()):
			vo.v_[i] = self.v_[i] / v2.v_[i]
		return vo

def dot(v1, v2):
	return np.dot(v1.v_, v2.v_)

def cross(v1, v2):
	return np.cross(v1.v_, v2.v_)

def mag(v):
	if isinstance(v, (vector,)):
		return v.mag()
	elif isinstance(v, (list,)):
		s = 0.0
		for c in v:
			s += c*c
		return np.sqrt(s)
	else:
		return np.sqrt(v*v)
