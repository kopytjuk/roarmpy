import json
import math
from typing import Any, Dict

import requests

from roarmpy.robot_kinematics import RobotArmKinematics
from roarmpy.utils import transform_from_pose


class RoArmClient:
    """
    Robot class for controlling a painting robot via HTTP commands.

        ip_address (str): IP address of the robot.

    Methods:
        move_to(x, y, z, speed): Move robot to specified coordinates.
        home(): Move robot to home position.
        get_state(): Retrieve current state of the robot.
    """

    def __init__(
        self,
        ip_address: str,
        kinematics: RobotArmKinematics,
        debug_mode: bool = False,
    ):
        self._ip_address = ip_address
        self._session = requests.Session()
        self._debug_mode = debug_mode
        self._kinematics = kinematics

    def move_to(
        self,
        x: float,
        y: float,
        z: float,
        pitch_rad: float = 0.0,
        roll_rad: float = 0.0,
        speed: float | None = 0.25,
    ):
        T_target = transform_from_pose(x, y, z, roll_rad, pitch_rad, yaw_rad = 0.0)

        joint_angles, success = self._kinematics.inverse_kinematics(T_target)

        if not success:
            print("Movement not possible")
            return
        
        self.set_joint_angles(*joint_angles)

    def move_to_internal(
        self,
        x: float,
        y: float,
        z: float,
        pitch_rad: float = 0.0,
        roll_rad: float = 0.0,
        speed: float | None = 0.25,
    ) -> None:
        """Move robot to specified coordinates using the robot's internal inverse
        kinematics model."""
        command = {
            "T": 104 if speed is not None else 1041,
            "x": float(x),
            "y": float(y),
            "z": float(z),
            "t": math.pi / 2 + pitch_rad,
            "r": roll_rad,
            "g": 3.14,
            "spd": speed,
        }
        self._send_command(command)

    def go_home(self) -> None:
        """Move robot to home position."""
        command = {"T": 100}
        self._send_command(command)

    def set_joint_angles(
        self,
        j1: float,
        j2: float,
        j3: float,
        j4: float,
        j5: float,
        gripper: float = 3.15,
        speed: float = 0.2,
        acc: float = 10,
    ):
        command = {
            "T": 102,
            "base": j1,
            "shoulder": j2,
            "elbow": j3 + math.pi / 2,
            "wrist": j4,
            "roll": j5,
            "hand": gripper,
            "spd": speed,
            "acc": 10,
        }
        self._send_command(command)

    def get_state(self) -> dict:
        """Return robot state

        tit, b, s, e, t, r, g: Represent the End joint posture, base joint,
        shoulder joint, elbow joint, wrist joint 1, and wrist joint 2, End joint angle respectively, and are displayed in radians.

        Returns:
            dict: state dictionary
        """
        command = {"T": 105}
        response = self._send_command(command)
        robot_state = json.loads(response)
        return robot_state

    def get_joint_angles(self) -> tuple[float, float, float, float, float]:
        robot_state = self.get_state()
        return (
            robot_state["b"],
            robot_state["s"],
            robot_state["e"] - math.pi / 2,
            robot_state["t"],
            robot_state["r"],
        )

    def _send_command(self, command: Dict[str, Any]) -> str:
        """Send a command to the robot."""
        url = f"http://{self._ip_address}/js?json={json.dumps(command)}"
        response = self._session.get(url)
        return response.text
