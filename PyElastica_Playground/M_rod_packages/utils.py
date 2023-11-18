from elastica import * 
from numba import njit

class ArbitarypointForces(NoForces):
    """
    This class applies constant forces on the endpoint nodes.

        Attributes
        ----------
        applied_force: numpy.array
            Forces applied to the system
        node_index: numpy.array
            Node_indices where forces applied in the system.
        ramp_up_time: float
            Applied forces are ramped up until ramp up time.

    """

    def __init__(self, applied_forces, node_indices, ramp_up_time):
        super().__init__()
        self.node_indices = node_indices
        self.applied_forces = applied_forces
        assert ramp_up_time > 0.0
        self.ramp_up_time = ramp_up_time


    def apply_forces(self, system: SystemType, time=0.0):
        self.compute_end_point_forces(
            system.external_forces,
            self.applied_forces,
            self.node_indices,
            time,
            self.ramp_up_time,
        )

    @staticmethod
    @njit(cache=True)
    def compute_end_point_forces(
        external_forces, applied_forces, node_indices, time, ramp_up_time
    ):
        """
        Compute end point forces that are applied on the rod using numba njit decorator.

        Parameters
        ----------
        applied_force: numpy.array
            Forces applied to the system
        node_index: numpy.array
            Node_indices where forces applied in the system.
        ramp_up_time: float
            Applied forces are ramped up until ramp up time.
        time: float

        Returns
        -------

        """
        factor = min(1.0, time / ramp_up_time)
        for index in node_indices:
            external_forces[..., index] += applied_forces * factor
