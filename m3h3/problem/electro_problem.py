from dolfin import (Constant)

import cbcbeat

from m3h3 import Parameters, Physics
from m3h3.problem import Problem


class ElectroProblem(Problem):

    def __init__(self, geometry, time, **kwargs):
        super().__init__(geometry, time, **kwargs)
        cell_model = self.get_cell_model()
        self._form = self._init_form(cell_model)


    def get_cell_model(self):
        model = parameters[Physics.ELECTRO.value]['cell_model']
        if model == "Tentusscher_panfilov_2006_epi_cell":
            return cbcbeat.Tentusscher_panfilov_2006_M_cell()


    def _init_form(self, cell_model):
        M_i = parameters[Physics.ELECTRO.value]['M_i']
        M_e = parameters[Physics.ELECTRO.value]['M_e']
        return cbcbeat.CardiacModel(self.mesh, self.time, M_i, M_e, cell_model)
