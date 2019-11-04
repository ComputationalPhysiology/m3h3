import dolfin as df

class Problem(object):

    def __init__(self, geometry, interval, **kwargs):
        self.mesh = geometry.mesh
        self.interval = interval


    def _init_spaces(self, *args, **kwargs):
        pass
