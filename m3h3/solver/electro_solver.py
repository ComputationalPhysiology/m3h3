from dolfin import (Constant)

import cbcbeat

from m3h3 import Physics
from m3h3.solver import Solver


class ElectroSolver(Solver):

    def __init__(self, form, time, interval, dt, parameters, **kwargs):
        super().__init__(form, time, interval, dt, parameters, **kwargs)


    def _init_solver(self):
        self.solver = self._form


    def step(self):
        time = float(self.time)
        self.solver.step((time-self.dt, time))