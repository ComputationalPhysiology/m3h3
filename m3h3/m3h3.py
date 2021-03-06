import numpy as np

from dolfin import (Constant, Parameters)

from geometry import HeartGeometry, MultiGeometry

from m3h3.setup_parameters import Parameters, Physics
from m3h3.pde import *
from m3h3.pde.solver import *


class M3H3(object):

    def __init__(self, geometry, parameters, *args, **kwargs):
        self.parameters = parameters
        self.physics = [Physics(p) for p in parameters.keys()
                                                    if Physics.has_value(p)]
        self.interactions = kwargs.get('interactions', [])
        if len(self.interactions) > 0:
            self._check_physics_interactions()

        if 'time' in kwargs.keys():
            self.time = kwargs['time']
            kwargs.pop('time', None)
        else:
            self.time = Constant(self.parameters['start_time'])

        self._setup_geometries(geometry, self.physics)
        self._setup_problems(**kwargs)
        self._setup_solvers(**kwargs)


    def step(self):
        # Setup time stepping if running step function for the first time.
        if self.time.values()[0] == self.parameters['start_time']:
            self.num_steps, self.max_dt = self._get_num_steps()

        time = float(self.time)
        solution_fields = self.get_solution_fields()

        if Physics.ELECTRO in self.physics:
            for _ in range(self.num_steps[Physics.ELECTRO]):
                electro_fields = solution_fields[str(Physics.ELECTRO)]
                self.electro_solver.step(electro_fields[1])

        if Physics.SOLID in self.physics:
            for _ in range(self.num_steps[Physics.SOLID]):
                self.solid_solver.step()

        if Physics.FLUID in self.physics:
            for _ in range(self.num_steps[Physics.FLUID]):
                self.fluid_solver.step()

        if Physics.POROUS in self.physics:
            for _ in range(self.num_steps[Physics.POROUS]):
                self.porous_solver.step()
                
        self.time.assign(time + self.max_dt)
        return time, solution_fields


    def get_solution_fields(self):
        solution_fields = {}
        if Physics.ELECTRO in self.physics:
            solution_fields[str(Physics.ELECTRO)] =\
                                    self.electro_problem._get_solution_fields()
        if Physics.SOLID in self.physics:
            pass
        if Physics.FLUID in self.physics:
            pass
        if Physics.POROUS in self.physics:
            pass
        return solution_fields


    def add_stimulus(self, stimulus):
        assert hasattr(self, 'electro_problem'), \
            "Cannot add stimulus if electrophysiology has not been set up."
        self.electro_problem.add_stimulus(stimulus)


    def _get_num_steps(self):
        dt_physics = self._get_physics_dt()
        min_dt = min(dt_physics.values())
        max_dt = max(dt_physics.values())
        num_steps = {}
        if Physics.ELECTRO in self.physics:
            dt = dt_physics[Physics.ELECTRO]
            if self._check_dt_is_multiple(dt, min_dt):
                num_steps[Physics.ELECTRO] = int(max_dt/dt)
        if Physics.SOLID in self.physics:
            dt = dt_physics[Physics.SOLID]
            if self._check_dt_is_multiple(dt, min_dt):
                num_steps[Physics.SOLID] = int(max_dt/dt)
        if Physics.FLUID in self.physics:
            dt = dt_physics[Physics.FLUID]
            if self._check_dt_is_multiple(dt, min_dt):
                num_steps[Physics.FLUID] = int(max_dt/dt)
        if Physics.POROUS in self.physics:
            dt = dt_physics[Physics.POROUS]
            if self._check_dt_is_multiple(dt, min_dt):
                num_steps[Physics.POROUS] = int(max_dt/dt)
        return num_steps, max_dt


    def _check_dt_is_multiple(self, dt, min_dt):
        if not (dt/min_dt).is_integer():
            msg = "Time step sizes have to be multiples of each other."\
                    "{} is not a multiple of {}".format(dt, min_dt)
            raise ValueError(msg)
        else:
            return True


    def _get_physics_dt(self):
        dt = {}
        if Physics.ELECTRO in self.physics:
            dt[Physics.ELECTRO] = self.parameters[str(Physics.ELECTRO)]['dt']
        if Physics.SOLID in self.physics:
            dt[Physics.SOLID] = self.parameters[str(Physics.SOLID)]['dt']
        if Physics.FLUID in self.physics:
            dt[Physics.FLUID] = self.parameters[str(Physics.FLUID)]['dt']
        if Physics.POROUS in self.physics:
            dt[Physics.POROUS] = self.parameters[str(Physics.POROUS)]['dt']
        return dt


    def _setup_problems(self, **kwargs):
        if Physics.ELECTRO in self.physics:
            self.electro_problem = ElectroProblem(
                                        self.geometries[Physics.ELECTRO],
                                        self.time,
                                        self.parameters[str(Physics.ELECTRO)],
                                        **kwargs)
            
        if Physics.SOLID in self.physics:
            self.solid_problem = SolidProblem(
                                        self.geometries[Physics.SOLID], 
                                        self.time,
                                        self.parameters[str(Physics.SOLID)],
                                        **kwargs)

        if Physics.FLUID in self.physics:
            self.fluid_problem = FluidProblem(
                                        self.geometries[Physics.FLUID],
                                        self.time,
                                        self.parameters[str(Physics.FLUID)],
                                        **kwargs)

        if Physics.POROUS in self.physics:
            self.porous_problem = PorousProblem(
                                        self.geometries[Physics.POROUS],
                                        self.time,
                                        self.parameters[str(Physics.POROUS)],
                                        **kwargs)


    def _setup_solvers(self, **kwargs):
        interval = (self.parameters['start_time'], self.parameters['end_time'])
        solution_fields = self.get_solution_fields()

        if Physics.ELECTRO in self.physics:
            elabel = str(Physics.ELECTRO)
            electro_fields = solution_fields[elabel]
            parameters = self.parameters[elabel]['linear_variational_solver']
            self.electro_solver = BasicBidomainSolver(self.time,
                                    self.electro_problem._form, electro_fields,
                                    parameters, **kwargs)

        if Physics.SOLID in self.physics:
            parameters = self.parameters[str(Physics.SOLID)]
            self.solid_solver = SolidSolver(
                                    self.solid_problem._form, self.time,
                                    interval, parameters['dt'], parameters,
                                    **kwargs)

        if Physics.FLUID in self.physics:
            parameters = self.parameters[str(Physics.FLUID)]
            self.fluid_solver = FluidSolver(
                                    self.fluid_problem._form, self.time,
                                    interval, parameters['dt'], parameters,
                                    **kwargs)

        if Physics.POROUS in self.physics:
            parameters = self.parameters[str(Physics.POROUS)]
            self.porous_solver = PorousSolver(
                                    self.porous_problem._form, self.time,
                                    interval, parameters['dt'], parameters,
                                    **kwargs)


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
                    raise KeyError(msg)

                assert isinstance(self.geometries[phys], HeartGeometry)
        elif len(physics) == 1:
            self.geometries[physics[0]] = geometry
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


    def _setup_electro_problem(self, parameters):
        self.electro_problem = ElectroProblem(self.geometries[Physics.ELECTRO],
                                                self.time, parameters)


    def _setup_solid_problem(self, parameters):
        self.solid_problem = SolidProblem(self.geometries[Physics.SOLID],
                                                self.time, parameters)


    def _setup_fluid_problem(self, parameters):
        self.fluid_problem = FluidProblem(self.geometries[Physics.FLUID],
                                                self.time, parameters)


    def _setup_porous_problem(self, parameters):
        self.porous_problem = PorousProblem(self.geometries[Physics.POROUS],
                                                self.time, parameters)


    def update_parameters(self, physics, parameters):
        if physics == Physics.ELECTRO:
            self.parameters.set_electro_parameters(parameters)
        elif physics == Physics.SOLID:
            self.parameters.set_solid_parameters(parameters)
        elif physics == Physics.FLUID:
            self.parameters.set_fluid_parameters(parameters)
        elif physics == Physics.POROUS:
            self.parameters.set_porous_parameters(parameters)
