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
        new_time = time+self.dt
        self.solver.step((time, new_time))
        return self.solver.solution_fields()