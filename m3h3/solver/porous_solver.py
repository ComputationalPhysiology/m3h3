from dolfin import (Constant)

from m3h3 import Physics
from m3h3.solver import Solver


class PorousSolver(Solver):

    def __init__(self, form, time, **kwargs):
        super().__init__(form, time, **kwargs)
