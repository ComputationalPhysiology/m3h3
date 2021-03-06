"""This demo shows how to set up a pure electrophysiology simulation in M3H3.
The simulation uses a 2D rectangular domain with a stimulus presented in the
bottom left corner.


This demo shows how to
======================

- define a geometry using the fenics-geometry module,
- load and set parameters for the simulation,
- define a stimulus for the underlying ODE model
"""


import dolfin as df
import numpy as np

import m3h3
from m3h3 import M3H3, Parameters, Physics, Stimulus
from geometry import Geometry2D, MarkerFunctions2D


comm = df.MPI.comm_world

# Define geometry parameters
Lx = 20. # mm
Ly = 7.  # mm
dx = 0.5

# Create geometry
N = lambda v: int(np.rint(v))
mesh = df.RectangleMesh(comm, df.Point(0.0, 0.0), df.Point(Lx, Ly),
                            N(Lx/dx), N(Ly/dx))

# Setup stimulation protocol
class PacingCells(df.SubDomain):
    def inside(self, x, on_boundary):
        return pow(x[0], 2) + pow(x[1], 2) < 1.0

markers = {'STIMULUS': 1, 'NONE': 0}
mf = df.MeshFunction('size_t', mesh, mesh.geometric_dimension()-1)
mf.set_all(0)
pacing_cells = PacingCells()
pacing_cells.mark(mf, markers['STIMULUS'])
markerfunctions = MarkerFunctions2D(ffun=mf)

geo = Geometry2D(mesh, markers=markers, markerfunctions=markerfunctions)

# Setup parameters
parameters = Parameters('M3H3')
parameters['end_time'] = 800.0 # ms

parameters.set_electro_parameters()
eparam = parameters[str(Physics.ELECTRO)]
eparam['M_i'] = 1.0
eparam['M_e'] = 2.0
eparam['I_s'].update({'period': 400, 'amplitude': 100, 'duration': 5})
eparam['dt'] = 1e-3

starttime = parameters['start_time']
endtime = parameters['end_time']
dt = eparam['dt']
time = df.Constant(starttime)
steps = int((endtime-starttime)/dt)

# Setup simulation
model = M3H3(geo, parameters, time=time)

# File for output
f = df.XDMFFile(comm, "demo_electrophysiology.xdmf")
f.parameters["flush_output"] = True
f.parameters["rewrite_function_mesh"] = True
f.parameters["functions_share_mesh"] = True


# Loop over time
for step in range(steps):
    time, fields = model.step()
    if time % 10 < dt:
        for field in fields:
            if field is not None:
                f.write(field, int(time))

f.close()
