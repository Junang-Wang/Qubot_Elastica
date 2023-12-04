
from elastica.boundary_conditions import GeneralConstraint 

import numpy as np 
from numba import njit
from typing import Optional
class ActuatorConstraint(GeneralConstraint):
    """
    Actuator constraint class describe how actuator constrain the passing rod which forbids 2 transitional DOF and 2 bending DOF and only allow twisting and the transition along the rod
    """
    def __init__(
            self,
            *fixed_data,
            translational_constraint_selector: Optional[np.ndarray] = None,
            rotational_constraint_selector: Optional[np.array] = None,
            **kwargs,
    ):
        super().__init__(*fixed_data,translational_constraint_selector, rotational_constraint_selector, **kwargs)

    @staticmethod
    @njit(cache=True)
    def nb_constrain_translational_values(
        position_collection, fixed_position_collection, indices, constraint_selector
    ) -> None:
        """
        Computes constrain values in numba njit decorator

        Parameters
        ----------
        position_collection : numpy.ndarray
            2D (dim, blocksize) array containing data with `float` type.
        fixed_position_collection : numpy.ndarray
            2D (dim, blocksize) array containing data with `float` type.
        indices : numpy.ndarray
            1D array containing the index of constraining nodes
        constraint_selector: numpy.ndarray
            1D array of type int and size (3,) indicating which translational Degrees of Freedom (DoF) to constrain.
            Entries are integers in {0, 1} (e.g. a binary values of either 0 or 1).
            If entry is 1, the concerning DoF will be constrained, otherwise it will be free for translation.
            Selector shall be specified in the inertial frame
        """
        block_size = indices.size
        for i in range(block_size):
            k = indices[i]
            # First term: add the old position values using the inverse constraint selector (e.g. DoF)
            # Second term: add the fixed position values using the constraint selector (e.g. constraint dimensions)
            position_collection[..., k] = (
                1 - constraint_selector
            ) * position_collection[
                ..., k
            ] + constraint_selector * fixed_position_collection[
                ..., i
            ]

