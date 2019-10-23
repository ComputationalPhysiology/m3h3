import dolfin as df
from dolfin import Parameters, LogLevel

parameters = df.Parameters("M3H3")


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
    electro = df.Parameters("Electro")
    parameters.add(electro)


def set_solid_default_parameters():
    """Sets default parameters for solid mechanics problems.
    """
    solid = df.Parameters("Solid")
    parameters.add(solid)


def set_fluid_default_parameters():
    """Sets default parameters for fluid dynamics problems.
    """
    fluid = df.Parameters("Fluid")
    parameters.add(fluid)


def set_porous_default_parameters():
    """Sets default parameters for porous mechanics problems.
    """
    porous = df.Parameters("Porous")
    parameters.add(porous)
