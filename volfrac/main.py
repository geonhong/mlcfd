#!/usr/bin/env python

import sys
import vector, lineseg, geometry
import numpy as np

def sqr(s):
	return s*s

args = sys.argv[1:]

fname = 'geom.dat'

if len(args)>0:
	fname = args[0]

dom_size = 16
n_cells = 8
vfl = []

cell_area = sqr(dom_size/n_cells)

if __name__ == '__main__':
	# geometry.geometryGenerator('geo2.dat', 'circle', 6)

	dom = geometry.cartesianDomain(dom_size, dom_size, n_cells, n_cells)
	pts = dom.ptlist()

	print("Reading data file ", fname)
	g = geometry.geometry(fname)

	pmin, pmax = g.boundingbox()

	print("> bounding box: ", pmin, pmax)
	a = pmax.x()
	b = pmax.y()
	area_theoret = np.pi*a*b

	nx, ny = dom.size()
	area_total = 0.0
	for i in range(0, nx-1):
		for j in range(0, ny-1):
			c = dom.cell(i,j)

			area = 0.0
			if (c.intersect(g)):
				area = c.intersectedArea(g, Debug=False)
			elif c.inside(g):
				area = c.getarea()
			#else:
			#	print(0.0)

			print(i, j, area)

			vfl.append(area)

			area_total += area
	
	darea = area_theoret - area_total
	err = darea/area_theoret*100.0

	print("Total area   : ", area_total)
	print("Theoret. area: ", area_theoret)
	print("Error        : ", err, " %")

	# Write data into a file
	fout = open('volfrac.dat', 'w')

	for vf in vfl:
		fout.write(str(vf/cell_area) + ' ')
	
	fout.close()
