import dolfin as df

class Problem(object):

    def __init__(self, geometry, time, **kwargs):
        self.mesh = geometry.mesh
        self.time = time


    def _init_form(self, *args, **kwargs):
        pass
