from dolfin import (Constant)

import cbcbeat

from m3h3 import Parameters, Physics
from m3h3.problem import Problem


class ElectroProblem(Problem):

    def __init__(self, geometry, time, parameters, **kwargs):
        super().__init__(geometry, time, parameters, **kwargs)
        self.cell_model = self.get_cell_model()
        self._form = self._init_form()
        self._fields = self._get_solution_fields()
        self._set_initial_conditions()


    def get_cell_model(self):
        model = self.parameters['cell_model']
        if model == "Tentusscher_panfilov_2006_M_cell":
            return cbcbeat.Tentusscher_panfilov_2006_epi_cell()


    def _init_form(self):
        M_i = self.parameters['M_i']
        M_e = self.parameters['M_e']
        cardiac_model = cbcbeat.CardiacModel(self.geometry.mesh, self.time,
                                                    M_i, M_e, self.cell_model)
        return cbcbeat.SplittingSolver(cardiac_model,
                                    params=self.parameters["SplittingSolver"])


    def _get_solution_fields(self):
        return self._form.solution_fields()


    def _set_initial_conditions(self):
        self._fields[0].assign(self.cell_model.initial_conditions())
