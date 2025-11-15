# roarmpy

![logo](docs/logo_small.png)

A minimal Python library to interface RoArm robot arms.

## Minimal example

```python
import math
import time

from roarmpy.roarm_client import RoArmClient
from roarmpy.robot_kinematics import RobotArmKinematics
from roarmpy.robots import RoArmM3Spec

roarm_m3_kinematics = RobotArmKinematics(RoArmM3Spec)

robot_handle = RoArmClient("<IP of the Robot>", kinematics=roarm_m3_kinematics)

# go to home position - looks like Γ
robot_handle.go_home()

time.sleep(3.0)

# move robot arm and the end effector
robot_handle.move_to(0.40, 0.0, 0.15, math.pi/4, 0.0)

time.sleep(3.0)

robot_handle.go_home()
```
