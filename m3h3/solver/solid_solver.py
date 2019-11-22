from dolfin import (Constant)

import pulse

from m3h3 import Physics
from m3h3.solver import Solver


class SolidSolver(Solver):

    def __init__(self, form, time, **kwargs):
        super().__init__(form, time, **kwargs)
