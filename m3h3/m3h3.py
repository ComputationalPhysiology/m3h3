import numpy as np

from m3h3 import parameters, Physics
from m3h3.problem.electro_problem import ElectroProblem
from m3h3.problem.solid_problem import SolidProblem
from m3h3.problem.fluid_problem import FluidProblem
from m3h3.problem.porous_problem import PorousProblem


class M3H3(object):

    def __init__(self, geometry, interactions=[]):
        physics = [Physics(p) for p in parameters.keys()]
        if Physics.ELECTRO in physics:
            self.setup_electro_problem(parameters[Physics.ELECTRO.value])
        if Physics.SOLID in physics:
            self.setup_solid_problem(parameters[Physics.ELECTRO.value])
        if Physics.FLUID in physics:
            self.setup_fluid_problem(parameters[Physics.ELECTRO.value])
        if Physics.POROUS in physics:
            self.setup_porous_problem(parameters[Physics.ELECTRO.value])

        # If multiple physics are defined, check that all are involved in an
        # interaction and that physics involved in an interaction are set up
        if len(physics) == 0 and len(interactions) > 0:
            msg = "At least one interaction has been set up, but no physics\nInteractions: {}".format(interactions)
            raise KeyError(msg)
        if len(physics) > 1:
            int_physics = set(np.array([ia.to_list() for ia in interactions]).flat)
            for p in int_physics:
                if p not in physics:
                    msg = "Physics {} appears in interaction, but is not set up.".format(p)
                    raise KeyError(msg)
            for p in physics:
                if p not in int_physics:
                    msg = "Physcis {} is set up, but does not appear in any interaction.".format(p)
                    raise KeyError(msg)


    def setup_electro_problem(self, parameter):
        self.electro_problem = ElectroProblem(parameter)


    def setup_solid_problem(self, parameter):
        self.solid_problem = SolidProblem(parameter)


    def setup_fluid_problem(self, parameter):
        self.fluid_problem = FluidProblem(parameter)


    def setup_porous_problem(self, parameter):
        self.porous_problem = PorousProblem(parameter)


    def solve():
        pass
