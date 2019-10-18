Design specification
================================

This page outlines the design specification that M3H3 is built against.


Physiological basis
======================

Historically, the physiology of the heart has mostly been studied in separation to resolve specific questions related to either electrophysiology, soft tissue mechanics or hemodynamics. However, in reality, the different branches of physics that involved in the functioning of the heart in health as well as disease, are highly interconnected, both across spatial and time scales.

.. image:: /_static/images/multiphysics_schematic.png

Some of these interactions have a larger influence on other interactions than others. We will refer to these as "forward" interactions, while the exact definition of a "forward interaction" remains to be decided on.


Software design
=======================

Parts of the problem have been tackled before, and we have the following FEniCS based software available:

* `fenics-geometry`: based on Henrik's pulse.geometry (https://github.com/ComputationalPhysiology/pulse), extended to handle arbitrary geometries.
* `cbcbeat`: mono- and bidomain module of electrophysiology, including cell ODE models.
* `pulse`: cardiac specific solid mechanics module.
* `oasis`: hemodynamics specific Navier-Stokes module.
* `perspect`: perfusion module.

M3H3 specifically does *not* aim at reinventing the wheel, and therefore it will be a wrapper module in the first instance.


Architecture
-------------------

```
from dolfin import *
from geometry import *

class M3H3(object)

	class Parameters (object)
	class Problem(object)

		class ElectroProblem(Problem): import cbcbeat
		class SolidProblem(Problem): import pulse
		class FluidProblem(Problem): import oasis
		class PorousProblem(Problem): import perspect


	class Interaction(object)

	class Solver(object)
  
		class ElectroSolver(Solver): import cbcbeat
		class SolidSolver(Solver): import pulse
		class FluidSolver(Solver): import oasis
		class PorousSolver(Solver): import perspect
```


User interface
=======================

M3H3's "hello world" will consist of setting up an simulation of electrophysiology driven contraction:

```
from m3h3 import *
from geometry import *

# Load a heart mesh including markers and marker functions
# from file
geo = HeartGeometry.load_from_file(‘heart_mesh.h5’)

# By instantiating parameters of a certain physics module we
# tell m3h3 which physics to involve in the simulation. In
# this case we are only interested in simulating EP and soft
# tissue dyamics at the continuum level.
electro_params = Parameters.ep_default_parameters()
solid_params = Parameters.solid_default_parameters()

# The user specifies the interactions included in the
# simulation by instantiating Interaction objects
ep2solid = Interaction(“ep”, “solid”)

# Once all physics and interactions are defined we can
# instantiate the M3H3 object
m3h3 = M3H3(geo, electro_params, solid_params, fluid_params, porous_params, ep2solid, solid2fluid, solid2porous)

# Loop over time
for t in time:
	# do some preprocessing

	m2h2.solve()

  # do some postprocessing, for example saving to file
```
