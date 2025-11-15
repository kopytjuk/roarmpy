"""Mechanical description for the RoArm M3.

This module defines the zero (home) end-effector pose `M`, the screw
axes matrix `S` and the axis points `Q_list` for the RoArm-M3 Pro.
"""

from typing import List

import numpy as np

# Dimensions in millimetres (mm)
_L_MM = {
    "L1": 44.0,
    "L2A": 240.0,
    "L2B": 30.0,
    "L3": 144.0,
    "L4A": 55.0,
    "L4B": 10.0,
    "L5": 123.0,  # end-effector length
}

_MM_TO_M = 1_000.0

# Convert dimensions to metres and expose convenient names
L1 = _L_MM["L1"] / _MM_TO_M
L2A = _L_MM["L2A"] / _MM_TO_M
L2B = _L_MM["L2B"] / _MM_TO_M
L3 = _L_MM["L3"] / _MM_TO_M
L4A = _L_MM["L4A"] / _MM_TO_M
L4B = _L_MM["L4B"] / _MM_TO_M
L5 = _L_MM["L5"] / _MM_TO_M


# Home (zero) end-effector pose: 4x4 homogeneous transform
# The robot is in its Γ position with the end-effector frame located
# at the tip of the robot with x,y,z axes in the same direction as the base-frame
M: np.ndarray = np.eye(4, dtype=float)
M[:3, 3] = [L2B + L3 + L4A + L5, 0.0, L1 + L2A - L4B]


def _screw_axis(omega: np.ndarray, q: np.ndarray) -> np.ndarray:
    """Return a 6-vector screw axis (omega, v) given omega (rotation vector)
    and a point q.

    v = -omega x q (so we compute cross(-omega, q)).
    """
    omega = np.asarray(omega, dtype=float)
    q = np.asarray(q, dtype=float)
    v = np.cross(-omega, q)
    return np.concatenate((omega, v))


# Define screw axes and points on axes (Q_list)

q_1 = np.array([0.0, 0.0, 0.0])
S1 = np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0])

omega_2 = np.array([0.0, 1.0, 0.0])
q_2 = np.array([0.0, 0.0, L1])
S2 = _screw_axis(omega_2, q_2)

omega_3 = np.array([0.0, 1.0, 0.0])
q_3 = np.array([L2B, 0.0, L1 + L2A])
S3 = _screw_axis(omega_3, q_3)

omega_4 = np.array([0.0, 1.0, 0.0])
q_4 = np.array([L2B + L3, 0.0, L1 + L2A])
S4 = _screw_axis(omega_4, q_4)

omega_5 = np.array([1.0, 0.0, 0.0])
q_5 = np.array([L2B + L3 + L4A, 0.0, L1 + L2A - L4B])
S5 = _screw_axis(omega_5, q_5)


Q_list: List[np.ndarray] = [q_1, q_2, q_3, q_4, q_5]
S_list: List[np.ndarray] = [S1, S2, S3, S4, S5]

S = np.column_stack(S_list)

__all__ = ["M", "S", "Q_list", "S_list"]
