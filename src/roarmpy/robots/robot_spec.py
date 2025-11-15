from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class RobotSpecification:
    name: str
    M: np.ndarray
    Slist: List[np.ndarray]

    @property
    def end_effector_zero_config(self) -> np.ndarray:
        return self.M

    @property
    def screw_axes_matrix(self) -> np.ndarray:
        return np.column_stack(self.Slist)
