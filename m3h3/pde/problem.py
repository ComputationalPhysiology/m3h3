import dolfin as df

class Problem(object):

    def __init__(self, geometry, time, parameters, **kwargs):
        self.geometry = geometry
        self.time = time
        self.parameters = parameters