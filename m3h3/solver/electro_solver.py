from dolfin import (Constant)

import cbcbeat

from m3h3 import Physics
from m3h3.solver import Solver


class ElectroSolver(Solver):

    def __init__(self, form, time, interval, dt, parameters, **kwargs):
        super().__init__(form, time, interval, dt, parameters, **kwargs)


    def _init_solver(self):
        self.solver = self._form.solve(self.interval, self.dt)
        self.solution_fields = self._form.solution_fields()


    def step(self):
        time = float(self.time)
        (t0, t1), self.solution_fields = next(self.solver)