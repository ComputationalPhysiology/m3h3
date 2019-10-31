import dolfin as df

class Problem(object):

    def __init__(self, geometry, *args, **kwargs):
        self.mesh = geometry.mesh


    def _init_spaces(self, *args, **kwargs):
        pass
