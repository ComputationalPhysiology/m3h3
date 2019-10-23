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
