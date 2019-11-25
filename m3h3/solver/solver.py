import dolfin as df

class Solver(object):

    def __init__(self, form, time, interval, dt, **kwargs):
        self._form = form
        self.time = time
        self.interval = interval
        self.dt = dt


    def step(self):
        pass