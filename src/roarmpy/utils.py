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


def pose_from_transform(
    T: np.ndarray,
) -> tuple[float, float, float, float, float, float]:
    """
    Extract position and Euler angles from a transformation matrix.
    
    Inverse operation of transform_from_pose().
    
    Args:
        T: 4x4 transformation matrix (SE(3))
        
    Returns:
        Tuple of (x, y, z, roll_rad, pitch_rad, yaw_rad)
    """
    # Extract position
    position = T[:3, 3]
    x, y, z = position[0], position[1], position[2]
    
    # Extract rotation matrix and convert to Euler angles
    rotation_matrix = T[:3, :3]
    rot = R.from_matrix(rotation_matrix)
    
    # Convert to zyx convention (same as used in transform_from_pose)
    yaw_rad, pitch_rad, roll_rad = rot.as_euler("zyx")
    
    return x, y, z, roll_rad, pitch_rad, yaw_rad
