from unittest.mock import MagicMock, patch

import pytest

from roarmpy.roarm_client import RoArmClient
from roarmpy.robot_kinematics import RobotArmKinematics
from roarmpy.robots import RoArmM3Spec


@pytest.fixture
def roarm_m3_kinematics() -> RobotArmKinematics:
    return RobotArmKinematics(RoArmM3Spec)


def test_move_to_home(roarm_m3_kinematics: RobotArmKinematics):
    with patch(
        "roarmpy.roarm_client.requests.Session"
    ) as mock_session_class:
        # Prepare the mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None

        # Configure the mock session
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        # Run the test
        robot_handle = RoArmClient("0.0.0.0", kinematics=roarm_m3_kinematics)
        robot_handle.go_home()

        # Assertions
        mock_session.get.assert_called_once()


def test_move_to(roarm_m3_kinematics: RobotArmKinematics):
    with (
        patch(
            "roarmpy.roarm_client.requests.Session"
        ) as mock_session_class,
        patch(
            "roarmpy.roarm_client.RoArmClient.get_joint_angles"
        ) as get_joint_angles_mock,
    ):
        # Prepare the mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"key": "value"}
        mock_response.raise_for_status.return_value = None

        # Configure the mock session
        mock_session = MagicMock()
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        # mock return method
        get_joint_angles_mock.return_value = (0.0, 0.0, 0.0, 0.0, 0.0)

        # Run the test
        robot_handle = RoArmClient("0.0.0.0", kinematics=roarm_m3_kinematics)
        robot_handle.move_to(0.4, 0.0, 0.0, 0.0, 0.0, speed=0.1)

        # Assertions
        mock_session.get.assert_called()
