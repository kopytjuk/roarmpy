import numpy as np


def normalize_angles(angles: np.ndarray) -> np.ndarray:
    normalized_rad = (angles + np.pi) % (2 * np.pi) - np.pi
    return normalized_rad
