# -*- coding: utf-8 -*-
"""This module implements the variational form for electrophysiology problems
"""

from dolfin import UserExpression
import cbcbeat

from m3h3.problem import Problem


class Stimulus(UserExpression):

    def __init__(self, markers, **kwargs):
        super().__init__(degree=kwargs['degree'])
        self.markers = markers
        self.amplitude = kwargs['amplitude']
        self.period = kwargs['period']
        self.duration = kwargs['duration']
        self.t = kwargs['t']

    def eval_cell(self, values, x, cell):
        periodic_t = float(self.t) % self.period
        if self.markers[cell.index] == 1 and periodic_t < self.duration:
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
        self.cell_model = self.get_cell_model()
        self._form = self._init_form(**kwargs)
        self._fields = self._get_solution_fields()
        self._set_initial_conditions()


    def get_cell_model(self):
        """Returns the cell model specified in the parameters.
        """
        model = self.parameters['cell_model']
        if model == "Tentusscher_panfilov_2006_M_cell":
            return cbcbeat.Tentusscher_panfilov_2006_epi_cell()


    def _init_form(self, **kwargs):
        M_i = self.parameters['M_i']
        M_e = self.parameters['M_e']
        model_kwargs = {k: kwargs[k] for k in kwargs.keys() &\
                                        {'stimulus'}}
        cardiac_model = cbcbeat.CardiacModel(self.geometry.mesh, self.time,
                                        M_i, M_e, self.cell_model,
                                        **model_kwargs)
        return cbcbeat.SplittingSolver(cardiac_model,
                                    params=self.parameters["SplittingSolver"])


    def _get_solution_fields(self):
        return self._form.solution_fields()


    def _set_initial_conditions(self):
        self._fields[0].assign(self.cell_model.initial_conditions())
