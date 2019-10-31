from dolfin import (FiniteElement, FunctionSpace)

import dolfin as df

from m3h3.problem.problem import Problem


class ElectroProblem(Problem):

    def __init__(self, geometry, parameters, *args, **kwargs):
        super().__init__(geometry, *args, **kwargs)
        self.parameters = parameters

        # Create function spaces
        self._init_spaces()


    def _init_spaces(self):
        k = self.parameters["polynomial_degree"]
        Ve = FiniteElement("CG", self.mesh.ufl_cell(), k)
        V = FunctionSpace(self.mesh, "CG", k)
        Ue = FiniteElement("CG", self.mesh.ufl_cell(), k)
        U = FunctionSpace(self.mesh, "CG", k)
