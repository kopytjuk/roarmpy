
import numpy as np
import pytest

from roarmpy.robot_kinematics import RobotArmKinematics
from roarmpy.robots import RoArmM3Spec


@pytest.fixture
def roarm_m3_kinematics() -> RobotArmKinematics:
    return RobotArmKinematics(RoArmM3Spec)


def test_kinematics(roarm_m3_kinematics: RobotArmKinematics):

    joint_angles_deg = [0., -21.43748512,  56.68905942, -10.25157431,
                                   0.]
    joint_angles_rad = np.deg2rad(joint_angles_deg)
    T = roarm_m3_kinematics.forward_kinematics(joint_angles_rad)

    join_angles_inv, success = roarm_m3_kinematics.inverse_kinematics(T, theta_0=None)

    join_angles_inv_deg = np.rad2deg(join_angles_inv)

    assert success, "Inverse kinematics failed to find a solution"
    
    assert np.allclose(joint_angles_deg, join_angles_inv_deg, atol=0.1), (
        f"Inverse kinematics returned {join_angles_inv_deg}, "
        f"expected {joint_angles_deg}"
    )
