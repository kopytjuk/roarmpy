import math
import time

from roarmpy.roarm_client import RoArmClient
from roarmpy.robot_kinematics import RobotArmKinematics
from roarmpy.robots import RoArmM3Spec

roarm_m3_kinematics = RobotArmKinematics(RoArmM3Spec)

robot_handle = RoArmClient("192.168.0.106", kinematics=roarm_m3_kinematics)

robot_handle.go_home()

time.sleep(3.0)

robot_handle.move_to(0.40, 0.0, 0.10, math.pi/4, 0.0)

time.sleep(3.0)

robot_handle.go_home()
