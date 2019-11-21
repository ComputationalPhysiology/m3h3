from dolfin import (Constant)

import cbcbeat

from m3h3 import parameters, Physics
from m3h3.solver import Solver


class ElectroSolver(Solver):

    def __init__(self, form, time, **kwargs):
        super().__init__(form, time, **kwargs)
