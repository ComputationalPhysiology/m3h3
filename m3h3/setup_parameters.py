from enum import Enum

import dolfin as df
from dolfin import Parameters, LogLevel

import m3h3


class Physics(Enum):
    ELECTRO = "Electro"
    SOLID = "Solid"
    FLUID = "Fluid"
    POROUS = "Porous"


def set_dolfin_compiler_parameters():
    """Sets dolfin parameters to speed up the compiler.
    """
    flags = ["-O3", "-ffast-math", "-march=native"]
    df.parameters["form_compiler"]["quadrature_degree"] = 4
    df.parameters["form_compiler"]["representation"] = "uflacs"
    df.parameters["form_compiler"]["cpp_optimize"] = True
    df.parameters["form_compiler"]["cpp_optimize_flags"] = " ".join(flags)


def set_electro_default_parameters():
    """Sets default parameters for electrophysiology problems.
    """
    electro = df.Parameters(Physics.ELECTRO.value)
    m3h3.parameters.add(electro)
    return electro


def set_solid_default_parameters():
    """Sets default parameters for solid mechanics problems.
    """
    solid = df.Parameters(Physics.SOLID.value)
    m3h3.parameters.add(solid)
    return solid


def set_fluid_default_parameters():
    """Sets default parameters for fluid dynamics problems.
    """
    fluid = df.Parameters(Physics.FLUID.value)
    m3h3.parameters.add(fluid)
    return fluid


def set_porous_default_parameters():
    """Sets default parameters for porous mechanics problems.
    """
    porous = df.Parameters(Physics.POROUS.value)
    m3h3.parameters.add(porous)
    return porous


def reset_m3h3_parameters():
    m3h3.parameters = df.Parameters("M3H3")
