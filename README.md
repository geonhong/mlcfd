Resources of the machine learning for CFD
=========================================

# volfrac
Estimate the volume fraction of cells in a fixed space

# airfoil
A sample case for predicting the aerodynamic performances of an airfoil. It contains a mesh generator for an airfoil which is written in .m4 macro (Please refer to airfoil/system/blockMeshDict.m4). To generate a mesh, you need a airfoil data with .dat file extension. It is recommended to locate the airfoil data file in constant/airfoilData. Once the airfoil data file is prepared, you can generate the mesh by running meshgen.

## Prepare the mesh generation
### Manipulate the airfoil data file
Suppose that we want to generate a mesh for a Clarky airfoil. The airfoil data is prepared at constant/airfoilData/clarky.dat. To generate a mesh with blockMesh utility, the airfoil should be divided into 3 sections: upper, front, lower sections. Breakpoints between those three sections should be given in the airfoil data file with a character 'b'. For example,

constant/airfoilData/clarky.dat

 ...
 0.36	0.0916266	
 0.34	0.0915079	
 0.32	0.0911857			/* Upper section until this point */
 0.3	0.0906804	b     	/* Break point here */
 0.28	0.0900016			/* Front section from this point */
 0.26	0.089084	
 0.24	0.0878308	
 ...


Then the airfoil data will be separated and generate sectional data file, such as *airfoil.upper.z0*, *airfoil.upper.z1*, *airfoil.endPoint.z0*, etc. The z0 represents the vertices on z=0 plane while z1 corresponds to z=0.1 plane. These manipulate files will be included in the *blockMeshDict.m4* macro file to generate a blockMeshDict. To manipulate the airfoil data, one should run constant/airfoilData/airfoilmanip.sh as following.

<code>
$ constant/airfoilData/airfoilmanip.sh constant/airfoilData/clarky.dat

</code>

As you can see you should give the airfoil data file after the airfoilmanip.sh command, or it will use constant/airfoilData/airfoil.dat as default.
