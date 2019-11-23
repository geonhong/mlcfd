/*--------------------------------*- C++ -*----------------------------------*\
  =========                 |
  \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox
   \\    /   O peration     | Website:  https://openfoam.org
    \\  /    A nd           | Version:  6
     \\/     M anipulation  |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
dnl>
changecom(//)changequote([,]) dnl>
define(calc, [esyscmd(perl -e 'print ($1)')]) dnl>
dnl>
define(pi, 3.141592) dnl>
define(d2r, calc(pi/180)) dnl>
define(sin5, calc(sin(d2r*5))) dnl>
define(cos5, calc(cos(d2r*5))) dnl>
define(tan5, calc(sin5/cos5)) dnl>
dnl>
dnl> ----------------------------------------------------------------------
dnl> <MESH PARAMETERS>
dnl> x-coordinate of forward domain center
define(xc, 0.4)	dnl>
dnl>
dnl> Radius of far-field
define(Rfar, 10) dnl>
dnl>
dnl> Length of the wake region
define(Lwk, 20) dnl>
dnl>
dnl> Number of normally distributed grid points
define(NV, 80) dnl>
dnl>
dnl> Number of grid points on forward section
define(NF, 120) dnl>
dnl>
dnl> Number of grid points on upper surface
define(NU, 80) dnl>
dnl>
dnl> Number of grid points on lower surface
define(NL, 80) dnl>
dnl>
dnl> Number of grid points in the wake region
define(NW, 120) dnl>
dnl>
dnl> Number of grid points on the trailing edge
define(NT, 5) dnl>
dnl>
dnl> Stretching ratio in vertical direction
define(SRV, 5000) dnl>
dnl>
dnl> Stretching ratio in wake region (flow direction)
define(SRW, 100) dnl>
define(SRWi, calc(1/SRW)) dnl>
dnl> </MESH PARAMETERS>
dnl> ----------------------------------------------------------------------
dnl>
dnl> Calculate primitve points
define(x0, calc(xc-Rfar*sin5)) dnl>
define(y0, calc(Rfar*cos5)) dnl>
dnl>
define(x2, 1) dnl>
define(y2, calc((1+(-1*x0))*tan5+y0)) dnl>
dnl>
define(x4, Lwk) dnl>
define(y4, calc(Lwk*tan5+y2)) dnl>
dnl>
define(xf, calc(xc-Rfar)) dnl>
dnl>
define(vertTup,($1 $2 $3)
	($1 -$2 $3)) dnl>
dnl>

convertToMeters 1;

vertices
(
	// Vertices on z=0 plane
	vertTup(x0, y0, 0)
	vertTup(x2, y2, 0)
	vertTup(x4, y4, 0)
	vertTup(x4, 0.01, 0)

	// End points
	include([airfoil.endPoint.z0])

	// Mid points (at maximum thickness)
	include([airfoil.midPoint.z0])

	// Vertices on z=0.1 plane
	vertTup(x0, y0, 0.1)
	vertTup(x2, y2, 0.1)
	vertTup(x4, y4, 0.1)
	vertTup(x4, 0.01, 0.1)

	// End points
	include([airfoil.endPoint.z1])

	// Mid points (at maximum thickness)
	include([airfoil.midPoint.z1])
);

blocks
(
	hex	(10 0 1 11 22 12 13 23) (NV NF 1) 	simpleGrading (SRV 1    1)	// block 1 - Front
	hex	( 8 2 0 10 20 14 12 22) (NV NU 1) 	simpleGrading (SRV 1    1)	// block 2 - upper
	hex	( 6 4 2  8 18 16 14 20) (NV NW 1) 	simpleGrading (SRV SRWi 1)	// block 3 - wake top
	hex	( 7 6 8  9 19 18 20 21) (NT NW 1) 	simpleGrading (1   SRWi 1)	// block 4 - wake mid
	hex	( 9 3 5  7 21 15 17 19) (NV NW 1) 	simpleGrading (SRV SRW  1)	// block 5 - wake bottom
	hex	(11 1 3  9 23 13 15 21) (NV NL 1) 	simpleGrading (SRV 1    1)	// block 6 - lower
);

edges
(
	arc	0  1 	(xf 0 0)
	arc	12 13 	(xf 0 0.1)

	// Airfoil curves on z=0 plane
	// Pressure side - rear
	BSpline	8 10
	(
		include([airfoil.upper.z0])
	)

	// Airfoil front
	BSpline	10 11
	(
		include([airfoil.front.z0])
	)

	// Suction side - rear
	BSpline	11 9
	(
		include([airfoil.lower.z0])
	)

	// Airfoil curves on z=0.1 plane
	// Pressure side - rear
	BSpline	20 22
	(
		include([airfoil.upper.z1])
	)

	// Airfoil front
	BSpline	22 23
	(
		include([airfoil.front.z1])
	)

	// Suction side - rear
	BSpline	23 21
	(
		include([airfoil.lower.z1])
	)
);

defaultPatch
{
	name	emptyPatches;
	type	empty;
}

boundary
(
    inlet
    {
        type patch;
        faces
        (
            (12 0 1 13)
			(14 2 0 12)
			(16 4 2 14)
			(13 1 3 15)
			(15 3 5 17)
        );
    }
    outlet
    {
        type patch;
        faces
        (
            (4 16 18 6)
			(6 18 19 7)
			(7 19 17 5)
        );
    }
    airfoil
    {
        type wall;
        faces
        (
            (22 10 8 20)
			(23 11 10 22)
			(21 9 11 23)
			(20 8 9 21)
        );
    }
);

// ************************************************************************* //
