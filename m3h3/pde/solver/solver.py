import dolfin as df

class Solver(object):

    def __init__(self, form, time, interval, dt, parameters, **kwargs):
        self._form = form
        self.time = time
        self.interval = interval
        self.dt = dt
        self.parameters = parameters
        self._init_solver()


    def _init_solver(self):
        pass


    def step(self):
        pass