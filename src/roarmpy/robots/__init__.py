from .roarm_m3 import M, S_list, joint_limits
from .robot_spec import RobotSpecification

RoArmM3Spec = RobotSpecification("RoArm M3", M, S_list, joint_limits)

__all__ = ["RoArmM3Spec"]
