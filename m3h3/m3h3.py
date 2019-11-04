import numpy as np

from dolfin import (Constant)

from geometry import Geometry, MultiGeometry

from m3h3 import parameters, Physics
from m3h3.problem.electro_problem import ElectroProblem
from m3h3.problem.solid_problem import SolidProblem
from m3h3.problem.fluid_problem import FluidProblem
from m3h3.problem.porous_problem import PorousProblem


class M3H3(object):

    def __init__(self, geometry, interactions=[]):
        physics = [Physics(p) for p in parameters.keys() if Physics.has_value(p)]

        self._setup_geometries(geometry, physics)

        # If multiple physics are defined, check that all are involved in an
        # interaction and that physics involved in an interaction are set up
        if len(physics) == 0 and len(interactions) > 0:
            msg = "At least one interaction has been set up, but no physics\n"\
                    "Interactions: {}".format(interactions)
            raise KeyError(msg)
        if len(physics) > 1:
            int_physics = set(np.array([ia.to_list() for ia in interactions]).flat)
            for p in int_physics:
                if p not in physics:
                    msg = "Physics {} appears in interaction, but is not set "\
                            "up.".format(p)
                    raise KeyError(msg)
            for p in physics:
                if p not in int_physics:
                    msg = "Physcis {} is set up, but does not appear in any "\
                            "interaction.".format(p)
                    raise KeyError(msg)

        self.interval = (parameters['start_time'], parameters['end_time'])

        if Physics.ELECTRO in physics:
            self._setup_electro_problem(parameters[str(Physics.ELECTRO)])
        if Physics.SOLID in physics:
            self._setup_solid_problem(parameters[str(Physics.SOLID)])
        if Physics.FLUID in physics:
            self._setup_fluid_problem(parameters[str(Physics.FLUID)])
        if Physics.POROUS in physics:
            self._setup_porous_problem(parameters[str(Physics.POROUS)])


    def solver(self):
        if self.electro_problem:
            return self.electro_problem.solver()
        if self.solid_problem:
            return self.solid_problem.solver()
        if self.fluid_problem:
            return self.fluid_problem.solver()
        if self.porous_problem:
            return self.porous_problem.solver()


    def _setup_geometries(self, geometry, physics):
        self.geometries = {}

        if isinstance(geometry, MultiGeometry):
            for phys in physics:
                try:
                    self.geometries[phys] = geometry.geometries[phys.value]
                except KeyError:
                    msg = "Could not find a geometry for {} physics in "\
                            "MultiGeometry. Ensure that geometry labels "\
                            "correspond to values in Physics "\
                            "enum.".format(phys.value)
        else:
            for phys in physics:
                self.geometries[phys] = geometry.copy(deepcopy=True)


    def _setup_electro_problem(self, parameter):
        self.electro_problem = ElectroProblem(self.geometries[Physics.ELECTRO],
                                                parameter, self.interval)


    def _setup_solid_problem(self, parameter):
        self.solid_problem = SolidProblem(self.geometries[Physics.SOLID],
                                                parameter)


    def _setup_fluid_problem(self, parameter):
        self.fluid_problem = FluidProblem(self.geometries[Physics.FLUID],
                                                parameter)


    def _setup_porous_problem(self, parameter):
        self.porous_problem = PorousProblem(self.geometries[Physics.POROUS],
                                                parameter)
