import dolfin as df

import pulse

from m3h3.problem.problem import Problem


class SolidProblem(Problem):

    def __init__(self, geometry, parameters, interval, **kwargs):
        super().__init__(geometry, interval, **kwargs)
        self.parameters = parameters
        mesh = geometry.mesh

        self.solidsolver = None


    def solver(self):
        return self.epsolver.solve(self.interval, self.parameters['dt'])


    def set_initial_conditions(self):
        pass


    def set_material(self):
        pass
