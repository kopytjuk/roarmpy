import numpy as np
from modern_robotics import FKinSpace

from roarmpy.robots.roarm_m3 import M, S


def test_fkinspace_home_pose():
    """FKinSpace with zero joint angles should return the home pose M."""
    
    thetalist = np.zeros(S.shape[1])
    T = FKinSpace(M, S, thetalist)
    assert np.allclose(T, M, atol=1e-9), (
        f"FKinSpace returned {T}, expected {M}"
    )
