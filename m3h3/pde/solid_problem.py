from functools import partial

from dolfin import Constant, DirichletBC

import pulse
from pulse.utils import get_lv_marker

from m3h3.pde import Problem


def dirichlet_fix_base(W, ffun, marker):
    """Fix the basal plane.
    """
    V = W if W.sub(0).num_sub_spaces() == 0 else W.sub(0)
    geometric_dim = V.num_sub_spaces()
    bc = DirichletBC(V, Constant([0]*geometric_dim), ffun, marker)
    return bc


def dirichlet_fix_base_directional(W, ffun, marker, direction=0):
    V = W if W.sub(0).num_sub_spaces() == 0 else W.sub(0)
    bc = DirichletBC(V.sub(direction), Constant(0.0), ffun, marker)
    return bc


def boundary_conditions(geometry, **bcs_parameters):
    try:
        pericardium_spring = bcs_parameters['pericardium_spring']
        base_spring = bcs_parameters['base_spring']
        base_bc = bcs_parameters['base_bc']
    except KeyError:
        msg = "Not all boundary conditions have been set. You have provided "\
                "{}".format(bcs_parameters.keys())
        raise KeyError(msg)
    # Neumann BCs
    lv_pressure = pulse.NeumannBC(
                        traction=Constant(0.0, name="lv_pressure"),
                        marker=geometry.get_lv_marker(), name="lv"
                    )
    neumann_bc = [lv_pressure]

    if geometry.has_rv():
        rv_pressure = pulse.NeumannBC(
                            traction=Constant(0.0, name="rv_pressure"),
                            marker=geometry.get_rv_marker(), name="rv"
                        )
        neumann_bc += [rv_pressure]

    # Robin BC
    robin_bc = []
    if pericardium_spring > 0.0:
        robin_bc += [pulse.RobinBC(
                        value=Constant(pericardium_spring),
                        marker=geometry.get_epi_marker()
                    )]

    if base_spring > 0.0:
        robin_bc += [pulse.RobinBC(
                        value=Constant(base_spring),
                        marker=geometry.get_base_marker()
                    )]

    # Dirichlet BC
    if base_bc == "fixed":
        dirichlet_bc = [partial(
                            dirichlet_fix_base, ffun=geometry.ffun, 
                            marker=geometry.get_base_marker(),
                        )]

    elif base_bc == "fix_x":
        dirichlet_bc = [partial(
                            dirichlet_fix_base_directional,
                            ffun=geometry.ffun,
                            marker=geometry.get_base_marker()
                        )]

    return pulse.BoundaryConditions(
        dirichlet=dirichlet_bc, neumann=neumann_bc, robin=robin_bc
    )


class SolidProblem(pulse.MechanicsProblem):

    def __init__(self, geometry, time, parameters, **kwargs):
        bcs_parameters = parameters["BoundaryConditions"]
        bcs = boundary_conditions(geometry, **bcs_parameters)
        super().__init__(geometry, kwargs['material'], bcs=bcs)
        self._form = self._virtual_work
        self._jacobian = 0