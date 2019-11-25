import numpy as np

from dolfin import (Constant, Parameters)

from geometry import Geometry, MultiGeometry

from m3h3.setup_parameters import Parameters, Physics
from m3h3.problem import (ElectroProblem, SolidProblem, FluidProblem,
                        PorousProblem)
from m3h3.solver import (ElectroSolver, SolidSolver, FluidSolver,
                        PorousSolver)


class M3H3(object):

    def __init__(self, geometry, physics, *args, **kwargs):
        self.parameters = Parameters("M3H3")
        self.physics = [Physics(p) for p in physics
                                    if (Physics.has_value(p) or p in Physics)]
        self.interactions = kwargs.get('interactions', [])
        if len(self.interactions) > 0:
            self._check_physics_interactions()

        if Physics.ELECTRO in physics:
            self.parameters.set_electro_parameters()
        if Physics.SOLID in physics:
            self.parameters.set_solid_parameters()
        if Physics.FLUID in physics:
            self.parameters.set_fluid_parameters()
        if Physics.POROUS in physics:
            self.parameters.set_porous_parameters()

        self._setup_geometries(geometry, physics)
        self.time = Constant(self.parameters['start_time'])
        self._setup_problems()
        self._setup_solvers()


    def solver(self):
        yield {}, {}


    def _setup_problems(self):
        if Physics.ELECTRO in self.physics:
            self.electro_problem = ElectroProblem(self.geometries[Physics.ELECTRO],
                                        self.time, self.parameters[str(Physics.ELECTRO)])
        if Physics.SOLID in self.physics:
            self.solid_problem = SolidProblem(self.geometries[Physics.SOLID], 
                                        self.time, self.parameters[str(Physics.SOLID)])
        if Physics.FLUID in self.physics:
            self.fluid_problem = FluidProblem(self.geometries[Physics.FLUID],
                                        self.time, self.parameters[str(Physics.FLUID)])
        if Physics.POROUS in self.physics:
            self.porous_problem = PorousProblem(self.goemetries[Physics.POROUS],
                                        self.time, self.parameters[str(Physics.POROUS)])


    def _setup_solvers(self):
        if Physics.ELECTRO in self.physics:
            self.electro_solver = ElectroSolver(
                    self.electro_problem._form, self.time)
        if Physics.SOLID in self.physics:
            self.solid_solver = SolidSolver(
                    self.solid_problem._form, self.time)
        if Physics.FLUID in self.physics:
            self.fluid_solver = FluidSolver(
                    self.fluid_problem._form, self.time)
        if Physics.POROUS in self.physics:
            self.porous_solver = PorousSolver(
                    self.porous_problem._form, self.time)


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


    def _check_physics_interactions(self):
        # If multiple physics are defined, check that all are involved in an
        # interaction and that physics involved in an interaction are set up
        if len(self.physics) == 0 and len(self.interactions) > 0:
            msg = "At least one interaction has been set up, but no physics\n"\
                    "Interactions: {}".format(self.interactions)
            raise KeyError(msg)
        if len(self.physics) > 1:
            int_physics = set(np.array([ia.to_list()
                                            for ia in self.interactions]).flat)
            for p in int_physics:
                if p not in self.physics:
                    msg = "Physics {} appears in interaction, but is not set "\
                            "up.".format(p)
                    raise KeyError(msg)
            for p in self.physics:
                if p not in int_physics:
                    msg = "Physcis {} is set up, but does not appear in any "\
                            "interaction.".format(p)
                    raise KeyError(msg)


    def _setup_electro_problem(self, parameter):
        self.electro_problem = ElectroProblem(self.geometries[Physics.ELECTRO],
                                                self.time)


    def _setup_solid_problem(self, parameter):
        self.solid_problem = SolidProblem(self.geometries[Physics.SOLID],
                                                self.time)


    def _setup_fluid_problem(self, parameter):
        self.fluid_problem = FluidProblem(self.geometries[Physics.FLUID],
                                                self.time)


    def _setup_porous_problem(self, parameter):
        self.porous_problem = PorousProblem(self.geometries[Physics.POROUS],
                                                self.time)


    def update_parameters(self, physics, parameters):
        if physics == Physics.ELECTRO:
            self.parameters.set_electro_parameters(parameters)
        elif physics == Physics.SOLID:
            self.parameters.set_solid_parameters(parameters)
        elif physics == Physics.FLUID:
            self.parameters.set_fluid_parameters(parameters)
        elif physics == Physics.POROUS:
            self.parameters.set_porous_parameters(parameters)
