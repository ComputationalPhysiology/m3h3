import dolfin as df

import pulse
from pulse.utils import get_lv_marker

from m3h3.problem.problem import Problem


class SolidProblem(pulse.MechanicsProblem):

    def __init__(self, geometry, time, parameters, **kwargs):
        bcs_parameters = parameters["BoundaryConditions"]
        self._set_boundary_conditions(**bcs_parameters)
        super().__init__(geometry, kwargs['material'])


    def _set_boundary_conditions(self, **bcs_parameters):
        # Neumann BCs
        lv_pressure = pulse.NeumannBC(
                            traction=Constant(0.0, name="lv_pressure"),
                            marker=self.geometry.get_lv_marker(), name="lv"
                        )
        neumann_bc = [lv_pressure]

        if self.geometry.has_rv():
            rv_pressure = pulse.NeumannBC(
                                traction=Constant(0.0, name="rv_pressure"),
                                marker=self.geometry.get_rv_marker(), name="rv"
                            )
            neumann_bc += [rv_pressure]

        # Robin BC
        robin_bc = []
        if pericardium_spring > 0.0:
            robin_bc += [pulse.RobinBC(
                            value=dolfin.Constant(pericardium_spring),
                            marker=self.geometry.get_epi_marker()
                        )]

        if base_spring > 0.0:
            robin_bc += [pulse.RobinBC(
                            value=dolfin.Constant(base_spring),
                            marker=self.geometry.get_base_marker()
                        )]

        # Dirichlet BC
        if base_bc == "fixed":
            dirichlet_bc = [partial(
                                dirichlet_fix_base, ffun=self.geometry.ffun,
                                marker=self.geometry.get_base_marker(),
                            )]

        elif base_bc == "fix_x":
            dirichlet_bc = [partial(
                                dirichlet_fix_base_directional,
                                ffun=self.geometry.ffun,
                                marker=self.geometry.get_base_marker()
                            )]

        self.bcs = pulse.BoundaryConditions(
            dirichlet=dirichlet_bc, neumann=neumann_bc, robin=robin_bc
        )