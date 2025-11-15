import numpy as np
from scipy.spatial.transform import Rotation as R


def normalize_angles(angles: np.ndarray) -> np.ndarray:
    normalized_rad = (angles + np.pi) % (2 * np.pi) - np.pi
    return normalized_rad


def transform_from_pose(
    x: float, y: float, z: float, roll_rad: float, pitch_rad: float, yaw_rad: float = 0.0
) -> np.ndarray:

    # end pose as SE(3)
    T_end = np.eye(4, dtype=float)
    T_end[:3, 3] = [x, y, z]

    rot = R.from_euler("zyx", (yaw_rad, pitch_rad, roll_rad))
    T_end[:3, :3] = rot.as_matrix()
    return T_end
