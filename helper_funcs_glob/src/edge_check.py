import numpy as np
import math


def edge_check(trajectory: np.ndarray,
               bound1: np.ndarray,
               bound2: np.ndarray,
               l_veh_real: float,
               w_veh_real: float) -> np.ndarray:
    """
    Created by:
    Alexander Heilmeier

    Created on:
    05.05.2018

    Documentation:
    Calculate minimum distance between vehicle and track boundaries for every trajectory point. Vehicle dimensions are
    taken into account for this calculation. Vehicle orientation is assumed to be the same as the heading of the
    trajectory.

    Inputs:
    trajectory:     array containing the trajectory information. Required are x, y, psi for every point.
    bound1/2:       array containing the track boundaries [x, y]
    l/w_veh_real:   real vehicle length and width in m.

    Outputs:
    min_dists:      minimum distance to boundaries for every trajectory point
    """

    # ------------------------------------------------------------------------------------------------------------------
    # CALCULATE MINIMUM DISTANCES --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    bounds = np.vstack((bound1, bound2))

    # calculate static vehicle edge positions
    fl = np.array([-w_veh_real / 2, l_veh_real / 2])
    fr = np.array([w_veh_real / 2, l_veh_real / 2])
    rl = np.array([-w_veh_real / 2, -l_veh_real / 2])
    rr = np.array([w_veh_real / 2, -l_veh_real / 2])

    # loop through all the centerline points
    min_dists = np.zeros(trajectory.shape[0])
    mat_rot = np.zeros((2, 2))

    for i in range(trajectory.shape[0]):
        mat_rot[0, 0] = math.cos(trajectory[i, 3])
        mat_rot[0, 1] = -math.sin(trajectory[i, 3])
        mat_rot[1, 0] = math.sin(trajectory[i, 3])
        mat_rot[1, 1] = math.cos(trajectory[i, 3])

        # calculate positions of vehicle edges
        fl_ = trajectory[i, 1:3] + np.matmul(mat_rot, fl)
        fr_ = trajectory[i, 1:3] + np.matmul(mat_rot, fr)
        rl_ = trajectory[i, 1:3] + np.matmul(mat_rot, rl)
        rr_ = trajectory[i, 1:3] + np.matmul(mat_rot, rr)

        # get minimum distances of vehicle edges to boundaries
        fl__mindist = np.sqrt(np.power(bounds[:, 0] - fl_[0], 2) + np.power(bounds[:, 1] - fl_[1], 2))
        fr__mindist = np.sqrt(np.power(bounds[:, 0] - fr_[0], 2) + np.power(bounds[:, 1] - fr_[1], 2))
        rl__mindist = np.sqrt(np.power(bounds[:, 0] - rl_[0], 2) + np.power(bounds[:, 1] - rl_[1], 2))
        rr__mindist = np.sqrt(np.power(bounds[:, 0] - rr_[0], 2) + np.power(bounds[:, 1] - rr_[1], 2))

        # save overall minimum distance of current vehicle position
        min_dists[i] = np.amin((fl__mindist, fr__mindist, rl__mindist, rr__mindist))

    return min_dists


# testing --------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
