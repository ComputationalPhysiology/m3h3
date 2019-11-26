from enum import Enum

import dolfin as df
from dolfin import (LogLevel, LUSolver, PETScKrylovSolver)

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


    def __eq__(self, other):
        return str(self) == str(other)


    def __hash__(self):
        return hash(str(self))


def set_dolfin_compiler_parameters():
    """Sets dolfin parameters to speed up the compiler.
    """
    flags = ["-O3", "-ffast-math", "-march=native"]
    df.parameters["form_compiler"]["quadrature_degree"] = 4
    df.parameters["form_compiler"]["representation"] = "uflacs"
    df.parameters["form_compiler"]["cpp_optimize"] = True
    df.parameters["form_compiler"]["cpp_optimize_flags"] = " ".join(flags)


class Parameters(df.Parameters):

    def __init__(self, label, **kwargs):
        super().__init__(label, **kwargs)
        set_dolfin_compiler_parameters()
        self.set_default_parameters()


    def set_default_parameters(self):
        self.add("log_level", df.get_log_level())
        m3h3.log(self["log_level"], "Log level is set to {}".format(
            LogLevel(self["log_level"])
        ))
        self.add("start_time", 0.0)
        self.add("end_time", 1.0)


    def set_electro_parameters(self, parameters=None):
        """Sets parameters for electrophysiology problems and solver. If argument
        is None, default parameters are applied
        """
        if not self.has_parameter_set(Physics.ELECTRO.value):
            self._set_electro_default_parameters()
        if self.has_parameter_set(Physics.ELECTRO.value) and parameters:
            self[Physics.ELECTRO.value].update(parameters)


    def set_solid_parameters(self, parameters=None):
        """Sets default parameters for solid mechanics problems.
        """
        if not self.has_parameter_set(Physics.SOLID.value):
            self._set_solid_default_parameters()
        if self.has_parameter_set(Physics.SOLID.value) and parameters:
             self[Physics.SOLID.value].update(parameters)


    def set_fluid_parameters(self, parameters=None):
        """Sets default parameters for fluid dynamics problems.
        """
        if not self.has_parameter_set(Physics.FLUID.value):
            self._set_fluid_default_parameters()
        if self.has_parameter_set(Physics.FLUID.value) and parameters:
            self[Physics.FLUID.value].update(parameters)


    def set_porous_parameters(self, parameters=None):
        """Sets default parameters for porous mechanics problems.
        """
        if not self.has_parameter_set(Physics.POROUS.value):
            self._set_porous_default_parameters()
        if self.has_parameter_set(Physics.POROUS.value) and parameters:
            self[Physics.POROUS.value].update(parameters)


    def _set_electro_default_parameters(self):
        electro = df.Parameters(Physics.ELECTRO.value)

        # Set default parameters
        electro.add("dt", 1e-3)
        electro.add("polynomial_degree", 1)
        electro.add("M_i", 1.0)
        electro.add("M_e", 2.0)
        electro.add("cell_model", "Tentusscher_panfilov_2006_M_cell")

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
        electro["SplittingSolver"]["BidomainSolver"]["preconditioner"] =\
                                                                    "petsc_amg"
        electro["SplittingSolver"]["enable_adjoint"] = False

        self.add(electro)


    def _set_solid_default_parameters(self):
        solid = df.Parameters(Physics.SOLID.value)
        solid.add("dt", 1e-3)
        solid.add("dummy_parameter", False)

        # Add default parameters from both LU and Krylov solvers
        solid.add(LUSolver.default_parameters())
        solid.add(PETScKrylovSolver.default_parameters())

        # Add solver parameters
        solid.add(df.Parameters("Solver"))
        solid["Solver"].add("dummy_parameter", False)

        self.add(solid)


    def _set_fluid_default_parameters(self):
        fluid = df.Parameters(Physics.FLUID.value)
        fluid.add("dt", 1e-3)
        fluid.add("dummy_parameter", False)

        # Add default parameters from both LU and Krylov solvers
        fluid.add(LUSolver.default_parameters())
        fluid.add(PETScKrylovSolver.default_parameters())

        # Add solver parameters
        fluid.add(df.Parameters("Solver"))
        fluid["Solver"].add("dummy_parameter", False)

        self.add(fluid)


    def _set_porous_default_parameters(self):
        porous = df.Parameters(Physics.POROUS.value)
        porous.add("dt", 1e-3)
        porous.add("dummy_parameter", False)

        # Add default parameters from both LU and Krylov solvers
        porous.add(LUSolver.default_parameters())
        porous.add(PETScKrylovSolver.default_parameters())

        # Add solver parameters
        porous.add(df.Parameters("Solver"))
        porous["Solver"].add("dummy_parameter", False)

        self.add(porous)