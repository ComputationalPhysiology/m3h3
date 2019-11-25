from dolfin import (Constant)

import cbcbeat

from m3h3 import Physics
from m3h3.solver import Solver


class ElectroSolver(Solver):

    def __init__(self, form, time, interval, dt, **kwargs):
        super().__init__(form, time, interval, dt, **kwargs)


    def _init_solver(self):
        self.solver = cbcbeat.SplittingSolver(self._form,
                                    params=self.parameters['SplittingSolver'])


    def step(self):
        return self.solver.step((self.time, Constant(self.time+self.dt)))