import dolfin as df

class Solver(object):

    def __init__(self, form, time, **kwargs):
        self._form = form
        self.time = time


    def solve(self, *args, **kwargs):
        pass
