from m3h3.utils import (log, set_log_level)

from m3h3.setup_parameters import (Physics, set_default_parameters,
                set_dolfin_compiler_parameters, set_electro_parameters,
                set_solid_parameters, set_fluid_parameters,
                set_porous_parameters, reset_m3h3_parameters)

from dolfin import Parameters
parameters = Parameters("M3H3")

from m3h3.interaction import Interaction
from m3h3.m3h3 import M3H3

set_dolfin_compiler_parameters()
set_default_parameters()
