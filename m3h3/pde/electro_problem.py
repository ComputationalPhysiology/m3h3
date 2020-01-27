# -*- coding: utf-8 -*-
"""This module implements the variational form for electrophysiology problems
"""

from dolfin import (grad, inner, Constant, FiniteElement, Function,
                    FunctionAssigner, FunctionSpace, Measure, MixedElement,
                    TestFunctions, TrialFunctions, UserExpression)
import cbcbeat

from m3h3.pde import Problem
from m3h3.ode import *


class Stimulus(UserExpression):

    def __init__(self, markers, stimulus_marker, **kwargs):
        super().__init__(degree=kwargs['degree'])
        self.markers = markers
        self.stimulus_marker = stimulus_marker
        self.amplitude = kwargs['amplitude']
        self.period = kwargs['period']
        self.duration = kwargs['duration']
        self.t = kwargs['t']

    def eval_cell(self, values, x, cell):
        periodic_t = float(self.t) % self.period
        if self.markers[cell.index] == self.stimulus_marker\
                                            and periodic_t < self.duration:
            values[0] = self.amplitude
        else:
            values[0] = 0
            
    def value_shape(self):
        return ()


class ElectroProblem(Problem):
    """This class implements the variational form for electrophysiology
    problems.
    """

    def __init__(self, geometry, time, parameters, **kwargs):
        super().__init__(geometry, time, parameters, **kwargs)
        self.geometry = geometry
        self.time = time
        self._init_fields()
        self._init_form(**kwargs)
        # self._set_initial_conditions()
        self.cell_model = self.get_cell_model()


    def get_cell_model(self):
        """Returns the cell model specified in the parameters.
        """
        model = self.parameters['cell_model']
        if model == "Tentusscher_panfilov_2006_M_cell":
            return Tentusscher_panfilov_2006_M_cell()


    def add_stimulus(self, stimulus):
        k = (v-v_)/dt
        stim_markers = set(stimulus.markers.array())
        dx = Measure("dx", domain=self.geometry.mesh, subdomain_data=I_s)
        self._form += -k*I_s*w*dx


    def _init_fields(self):
        k = self.parameters['polynomial_degree']
        Ve = FiniteElement('P', self.geometry.ufl_cell(), k)
        Ue = FiniteElement('P', self.geometry.ufl_cell(), k)
        V = FunctionSpace(self.geometry.mesh, Ve)
        U = FunctionSpace(self.geometry.mesh, Ue)

        use_constraint = self.parameters['use_average_u_constraint']
        if use_constraint:
            Re = FiniteElement('R', self.geometry.ufl_cell(), 0)
            R = FunctionSpace(self.geometry.mesh, Re)
            VURe = MixedElement([Ve, Ue, Re])
            self.solution_space = FunctionSpace(self.geometry.mesh, VURe)
        else:
            VURe = MixedElement([Ve, Ue])
            self.solution_space = FunctionSpace(self.geometry.mesh, VURe)

        self.current_space = V
        self.merger = FunctionAssigner(self.current_space,
                                                    self.solution_space.sub(0))
        self.prev_current = Function(self.current_space, name="prev_current")
        self.solution = Function(self.solution_space, name="solution")


    def _init_form(self, **kwargs):
        M_i = self.parameters['M_i']
        M_e = self.parameters['M_e']
        I_a = self.parameters['I_a'] # externally applied current
        dt = self.parameters['dt']
        theta = self.parameters['theta']

        use_constraint = self.parameters['use_average_u_constraint']
        if use_constraint:
            v, u, l = TrialFunctions(self.solution_space)
            w, q, lbd = TestFunctions(self.solution_space)
        else:
            v, u = TrialFunctions(self.solution_space)
            w, q = TestFunctions(self.solution_space)

        dx = self.geometry.dx
        v_ = self.prev_current
        k = Constant(1/dt)
        t = float(self.time)
        self.time.assign(t + theta*dt)

        # bidomain equation
        Vmid = theta*v + (1-theta)*v_
        theta_parabolic = (inner(M_i*grad(Vmid), grad(w))*dx\
                                            + inner(M_i*grad(u), grad(w))*dx)
        theta_elliptic = (inner(M_i*grad(Vmid), grad(q))*dx\
                                    + inner((M_i + M_e)*grad(u), grad(q))*dx)
        self._form = k*(v-v_)*w*dx + theta_parabolic + theta_elliptic

        if use_constraint:
            self._form += (lbd*u + l*q)*dx

        # external current
        self._form += I_a*q*dx

        # stimulus
        if 'STIMULUS' in self.geometry.markers.keys():
            stim_marker = self.geometry.markers['STIMULUS']
            I_s = Stimulus(self.geometry.markers, stim_marker,
                            amplitude=self.parameters["I_s"]['amplitude'],
                            period=self.parameters["I_s"]['amplitude'],
                            duration=self.parameters["I_s"]['duration'],
                            t=self.time, degree=1)
            self._form += I_s*w*dx


    def get_solution_fields(self):
        return (self.prev_current, self.solution)
