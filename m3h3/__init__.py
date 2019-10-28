from m3h3.setup_parameters import (set_dolfin_compiler_parameters,
                set_electro_default_parameters, set_solid_default_parameters,
                set_fluid_default_parameters, set_porous_default_parameters,
                reset_m3h3_parameters, Physics)

from dolfin import Parameters
parameters = Parameters("M3H3")

from m3h3.interaction import Interaction
from m3h3.m3h3 import M3H3

set_dolfin_compiler_parameters()
