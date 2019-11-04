from enum import Enum

import dolfin as df
from dolfin import (LogLevel, LUSolver, Parameters, PETScKrylovSolver)

import cbcbeat

import m3h3


class Physics(Enum):
    ELECTRO = "Electro"
    SOLID = "Solid"
    FLUID = "Fluid"
    POROUS = "Porous"

    def __str__(self):
        return self.value

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


def set_dolfin_compiler_parameters():
    """Sets dolfin parameters to speed up the compiler.
    """
    flags = ["-O3", "-ffast-math", "-march=native"]
    df.parameters["form_compiler"]["quadrature_degree"] = 4
    df.parameters["form_compiler"]["representation"] = "uflacs"
    df.parameters["form_compiler"]["cpp_optimize"] = True
    df.parameters["form_compiler"]["cpp_optimize_flags"] = " ".join(flags)


def set_default_parameters():
    m3h3.parameters.add("log_level", df.get_log_level())
    m3h3.log(m3h3.parameters["log_level"], "Log level is set to {}".format(
        m3h3.parameters["log_level"]
    ))
    m3h3.parameters.add("start_time", 0.0)
    m3h3.parameters.add("end_time", 1.0)


def set_electro_parameters(parameters=None):
    """Sets parameters for electrophysiology problems and solver. If argument
    is None, default parameters are applied
    """
    if Physics.ELECTRO.value not in m3h3.parameters.keys():
        _set_electro_default_parameters()

    if parameters is not None:
        try:
            m3h3.parameters[Physics.ELECTRO.value].update(parameters)
        except:
            msg = "'{}' contains invalid parameter keywords.".format(parameters)
            raise NameError(msg)
    return m3h3.parameters[Physics.ELECTRO.value]


def set_solid_parameters(parameters=None):
    """Sets default parameters for solid mechanics problems.
    """
    if Physics.SOLID.value not in m3h3.parameters.keys():
        _set_solid_default_parameters()

    if parameters is not None:
        try:
            m3h3.parameters[Physics.SOLID.value].update(parameters)
        except:
            msg = "'{}' contains invalid parameter keywords.".format(parameters)
            raise NameError(msg)
    return m3h3.parameters[Physics.SOLID.value]


def set_fluid_parameters(parameters=None):
    """Sets default parameters for fluid dynamics problems.
    """
    if Physics.FLUID.value not in m3h3.parameters.keys():
        _set_fluid_default_parameters()

    if parameters is not None:
        try:
            m3h3.parameters[Physics.FLUID.value].update(parameters)
        except:
            msg = "'{}' contains invalid parameter keywords.".format(parameters)
            raise NameError(msg)
    return m3h3.parameters[Physics.FLUID.value]


def set_porous_parameters(parameters=None):
    """Sets default parameters for porous mechanics problems.
    """
    if Physics.POROUS.value not in m3h3.parameters.keys():
        _set_porous_default_parameters()

    if parameters is not None:
        try:
            m3h3.parameters[Physics.POROUS.value].update(parameters)
        except:
            msg = "'{}' contains invalid parameter keywords.".format(parameters)
            raise NameError(msg)
    return m3h3.parameters[Physics.POROUS.value]


def _set_electro_default_parameters():
    electro = df.Parameters(Physics.ELECTRO.value)

    # Set default parameters
    electro.add("dt", 1e-3)
    electro.add("polynomial_degree", 1)
    electro.add("Mi", 1.0)
    electro.add("Me", 2.0)

    # Add default parameters from both LU and Krylov solvers
    electro.add(LUSolver.default_parameters())
    electro.add(PETScKrylovSolver.default_parameters())

    electro.add(cbcbeat.SplittingSolver.default_parameters())
    electro["SplittingSolver"]["theta"] = 0.5
    electro["SplittingSolver"]["pde_solver"] = "bidomain"
    electro["SplittingSolver"]["CardiacODESolver"]["scheme"] = "RL1"
    electro["SplittingSolver"]["BidomainSolver"]["linear_solver_type"] =\
                                                                    "iterative"
    electro["SplittingSolver"]["BidomainSolver"]["algorithm"] = "cg"
    electro["SplittingSolver"]["BidomainSolver"]["preconditioner"] = "petsc_amg"
    electro["SplittingSolver"]["enable_adjoint"] = False

    m3h3.parameters.add(electro)


def _set_solid_default_parameters():
    solid = df.Parameters(Physics.SOLID.value)
    solid.add("dummy_parameter", False)
    m3h3.parameters.add(solid)


def _set_fluid_default_parameters():
    fluid = df.Parameters(Physics.FLUID.value)
    fluid.add("dummy_parameter", False)
    m3h3.parameters.add(fluid)


def _set_porous_default_parameters():
    porous = df.Parameters(Physics.POROUS.value)
    porous.add("dummy_parameter", False)
    m3h3.parameters.add(porous)


def reset_m3h3_parameters():
    m3h3.parameters = df.Parameters("M3H3")
