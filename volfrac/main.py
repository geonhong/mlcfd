#!/usr/bin/env python

import vector, lineseg, geometry

if __name__ == '__main__':
	geometry.geometryGenerator('geo2.dat', 'circle', 6)

	dom = geometry.cartesianDomain(15,15,30,30)

	pts = dom.ptlist()
	g = geometry.geometry('geo2.dat')

	nx, ny = dom.size()
	for i in range(0, nx-1):
		for j in range(0, ny-1):
			c = dom.cell(i,j)

			print(i, j, end='\t')
			if (c.intersect(g)):
				print(c.intersectedArea(g))
			elif c.inside(g):
				print(c.getarea())
			else:
				print(0.0)
	
