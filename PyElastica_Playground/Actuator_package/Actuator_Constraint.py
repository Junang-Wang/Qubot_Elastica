
from elastica.boundary_conditions import GeneralConstraint 
from functools import reduce
from elastica.typing import SystemType, RodType
import numpy as np 
from numba import njit
from typing import Optional
class ActuatorConstraint(GeneralConstraint):
    """
    Actuator constraint class describe how actuator constrain the passing rod which forbids 2 transitional DOF and 2 bending DOF and only allow twisting and the transition along the rod

    Input:
    spatial_lim: the position actuator locate
    actuator_velocity: the velocity actuator boost
    actuator_omega:    the angular velocity actuator rotate
    constraint_selector: numpy.ndarray
    1D array of type int and size (3,) indicating which translational Degrees of Freedom (DoF) to constrain.
    Entries are integers in {0, 1} (e.g. a binary values of either 0 or 1).
    If entry is 1, the concerning DoF will be constrained, otherwise it will be free for translation.
    Selector shall be specified in the inertial frame
    """
    def __init__(
            self,
            *_arg,
            spatial_lim, 
            actuator_velocity_omega,
            translational_constraint_selector = np.array([True, False, True]),
            rotational_constraint_selector = np.array([True, False, True]),
            **kwargs,
    ):
        self.spatial_lim = spatial_lim
        self.actuator_velocity_omega = actuator_velocity_omega
        try:
            self._system = kwargs["_system"]

        except KeyError:
            raise KeyError(
                "Please use simulator.constrain(...).using(...) syntax to establish constraint."
            )
        constrained_position_idx, positions, directors = self.compute_fixed_data(spatial_lim= spatial_lim,system= self._system)

        try:
            kwargs["constrained_position_idx"] = constrained_position_idx
            kwargs["constrained_director_idx"] = constrained_position_idx
        except KeyError:
            raise KeyError(
                "Please use simulator.constrain(...).using(...) syntax to establish constraint."
            )
        super().__init__(*positions,*directors, translational_constraint_selector=translational_constraint_selector, rotational_constraint_selector=rotational_constraint_selector, **kwargs)

    # @staticmethod
    # @njit(cache=True)
    def compute_fixed_data(
        self, spatial_lim, system
    ):
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

        """
        pos = system.position_collection
        idx = []
        for i,lim in enumerate(spatial_lim):
            if lim:
                lb = lim[0]
                ub = lim[1]
                idx.append( np.asarray( (pos[i]>=lb) & (pos[i] <=ub) ).nonzero()[0])
            else:
                continue
        constrained_position_idx = reduce(np.intersect1d,idx)

        positions = (
            [system.position_collection[..., idx].copy() for idx in constrained_position_idx]
            if constrained_position_idx.size
            else []
        )
        directors = (
            [system.director_collection[..., idx].copy() for idx in constrained_position_idx]
            if constrained_position_idx.size
            else []
        )

        return constrained_position_idx, positions, directors
    

    #------------------------------------------
    def constrain_values(self, system: SystemType, time: float) -> None:

        constrained_position_idx, positions, directors = self.compute_fixed_data(spatial_lim= self.spatial_lim, system= system)
        self._constrained_position_idx = constrained_position_idx
        self._constrained_director_idx = constrained_position_idx
        if len(positions) > 1:
            self.fixed_positions = np.stack(positions, axis=-1) 
            self.fixed_directors = np.stack(directors, axis=-1)
        elif len(positions) == 1:
            self.fixed_positions = positions[0].reshape(3,1)
            self.fixed_directors = directors[0].reshape(3,3,1)
        
        self.fixed_positions[2] = 0 # forcing z coordinate =0  
        system.position_collection[2,self._constrained_director_idx] = 0
        if self.actuator_velocity_omega[1] < 0:
            for i in range(self.fixed_directors.shape[2]):
                # forcing directors to the original direction
                system.director_collection[...,self._constrained_director_idx[i]][self.rotational_constraint_selector] = system.director_collection[...,0][self.rotational_constraint_selector]
            # pass

        if self._constrained_position_idx.size:
            self.nb_constrain_translational_values(
                system.position_collection,
                self.fixed_positions,
                self._constrained_position_idx,
                self.translational_constraint_selector,
            )



    def constrain_rates(self, system: SystemType, time: float) -> None:
        # print(self.constrained_director_idx)
        # print(self.translational_constraint_selector)
        if self._constrained_position_idx.size:
            # boost the rod
            system.velocity_collection[...,self._constrained_position_idx] = self.actuator_velocity_omega[0]
            system.omega_collection[...,self._constrained_director_idx] = self.actuator_velocity_omega[1]

        if self._constrained_position_idx.size:
            self.nb_constrain_translational_rates(
                system.velocity_collection,
                self._constrained_position_idx,
                self.translational_constraint_selector,
            )
        if self._constrained_director_idx.size:
            self.nb_constrain_rotational_rates(
                system.director_collection,
                system.omega_collection,
                self._constrained_director_idx,
                self.rotational_constraint_selector,
            )


