from .roarm_m3 import M, S_list
from .robot_spec import RobotSpecification

RoArmM3Spec = RobotSpecification(M, S_list)

__all__ = ["RoArmM3Spec"]
