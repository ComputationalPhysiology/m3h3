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
        self._set_initial_conditions()


    def solver(self):
        return self.epsolver.solve(self.interval, self.parameters['dt'])


    def _set_initial_conditions(self):
        (vs_, vs, vur) = self.epsolver.solution_fields()
        vs_.assign(self.cell_model.initial_conditions())
