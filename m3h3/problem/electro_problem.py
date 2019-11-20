from dolfin import (Constant)

import cbcbeat

from m3h3.problem.problem import Problem


class ElectroProblem(Problem):

    def __init__(self, geometry, parameters, interval, **kwargs):
        super().__init__(geometry, interval, **kwargs)
        self.parameters = parameters
        mesh = geometry.mesh

        M_i = self.parameters['Mi']
        M_e = self.parameters['Me']

        self.interval = interval
        time = Constant(self.interval[0])

        self.cell_model = cbcbeat.Tentusscher_panfilov_2006_epi_cell()
        cardiac_model = cbcbeat.CardiacModel(mesh, time, M_i, M_e,
                                                self.cell_model)
        self.epsolver = cbcbeat.SplittingSolver(cardiac_model,
                                    params=self.parameters['SplittingSolver'])
        self.set_initial_conditions()


    def solver(self):
        dt = self.parameters['dt']
        time_range = self.interval[1]-self.interval[0]
        steps = int(time_range/dt)
        solutions = []
        for step in range(steps):
             yield self.solve_time_step()


    def solve_time_step(self):
        pass


    def set_initial_conditions(self):
        (vs_, vs, vur) = self.epsolver.solution_fields()
        vs_.assign(self.cell_model.initial_conditions())
