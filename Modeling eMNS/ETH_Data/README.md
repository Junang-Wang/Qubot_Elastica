# Synthetic Magnetic Fields Dataset for Electromagnetic Navigation System

This dataset contains data simulating an Electromagnetic Navigation System (eMNS) with Ne=8 electromagnets. 
The data is obtained by generating data with the multipole electromagnet model (MPEM) [1] and models the CardioMag [2]. 
Note that because this model is linear, electromagnet saturation is ignored, and the magnetic field is a linear function of the 
electromagnet currents.

The dataset contains magnetic fields corresponding to 3,787 distinct sets of electromagnet currents. The magnetic fields are calculated on
regular grids of size Ng x Ng x Ng covering the workspace of the CardioMag. Data is provided for Ng = 3, 4, 5, 6, 7, 8, 16, 32.
The MPEM generates magnetic fields from dipoles in free space. The magnetic fields are curl and divergence free, and contain no noise.

The data is stored using the HDF5 file format.

## List of Files
* currents_3787.csv: each row contains eight electromagnet currents in Amperes.
* currents_3787.h5 containts the same as above but in the H5 file format.

For each value of Ng, the mpem_synthetic_<Ng>_h5 folder contains
* args.txt : some metadata including the max and min values of the fields, Ng, the number of currents
* positions.h5: the grid positions of the magnetic field measurements. The positions are stored in variables xg, yg, zg as Ng x Ng x Ng arrays.
Note that the grids are defined in the z,y,x axis ordering. Positions are defined in meters.

The fields and gradients are contained in the v folder. For each 3,787 set of currents there is a file storing both the magnetic field and magnetic field vector 
called <num>.h5 where num is the number of the current vector. 

Inside that file is a variable called fields which contains the magnetic field vector at each position on the grid. Note the axis ordering is dim, z, y, x where dim are the x,y,z components of the field, and the remaining axes correspond to the position grid.

There is another variable called gradients which contains the gradient matrix at each position on the grid. The axis ordering is dimG1, dimG2, z, y, x where dimG1 corresponds to the columns of the gradient matrix, dimG2 the rows of the gradient matrix and the remaining axes correspond to the position grid.

## References
[1] A. J. Petruska, J. Edelmann, and B. J. Nelson, “Model-Based Calibration for Magnetic Manipulation,” IEEE Trans. Magn., vol. 53, no. 7, pp. 1–6, 2017.

[2] R. Yu, S. L. Charreyron, Q. Boehler, C. Weibel, C. C. Y. Poon, and B. J. Nelson, “Modeling Electromagnetic Navigation Systems for Medical Applications using Random Forests and Artificial Neural Networks,” in to appear at IEEE Int. Conf.. Rob. Autom. 2020, 2020.

## Dataset version
* 1.0 (current) The first version of this dataset 

Copyright 2020, Samuel Charreyron, All rights reserved