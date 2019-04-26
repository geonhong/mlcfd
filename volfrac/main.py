#!/usr/bin/env python

import vector, lineseg, geometry

if __name__ == '__main__':
	dom = geometry.cartesianDomain(1,1,4,4)
	pts = dom.ptlist()

	print(dom.size())

	for i in range(0, dom.size()[0]):
		print(dom.pt(i,i))

	for pt in pts:
		print(pt)
