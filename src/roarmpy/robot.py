
import modern_robotics as mr
import numpy as np

from roarmpy.robots.robot_spec import RobotSpecification
from roarmpy.utils import normalize_angles


class RobotArm:

    def __init__(self, robot_spec: RobotSpecification):
        self._robot_spec = robot_spec

    @property
    def num_joints(self) -> int:
        return self._robot_spec.screw_axes_matrix.shape[1]

    def forward_kinematics(self, theta_list: np.ndarray | list) -> np.ndarray:
        """Compute the transformation matrix of the robot arm.

        Args:
            theta_list (np.ndarray | list): joint angles in rad

        Returns:
            np.ndarray: 4x4 Transfomation matrix of the end-effector in SE(3)
        """

        theta_list = np.array(theta_list)

        return mr.FKinSpace(
            self._robot_spec.end_effector_zero_config,
            self._robot_spec.screw_axes_matrix,
            theta_list
        )

    def inverse_kinematics(
        self, end_effector_pose: np.ndarray, theta_0: np.ndarray | None = None,
        solver_args: dict | None = None
    ) -> tuple[np.ndarray, bool]:
        """Compute the joint angles from a desired end-effector pose using `mr.IKinSpace`.

        Args:
            end_effector_pose (np.ndarray): desired transfomation matrix of
                the end-effector in SE(3)
            theta_0 (np.ndarray | None, optional): First guess as
                initialization for the optimization. Defaults to `np.zeros`.
            solver_args (dict): keyword arguments passed to `mr.IKinSpace`

        Returns:
            tuple[np.ndarray, bool]: joint angles and success flag
        """

        # initial guess
        if theta_0 is None:
            theta_0 = np.zeros(self.num_joints)

        if solver_args is None:
            solver_args = dict(eomg=0.001, ev=0.001)

        theta_result, success = mr.IKinSpace(
            self.screw_axes_matrix,
            self.end_effector_zero_config,
            end_effector_pose,
            theta_0,
            **solver_args
        )

        theta_result = normalize_angles(theta_result)

        return theta_result, success
