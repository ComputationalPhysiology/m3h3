import dolfin as df

import pulse

from m3h3.problem.problem import Problem


class SolidProblem(Problem):

    def __init__(self, geometry, time, *args, **kwargs):
        super().__init__(geometry, time, **kwargs)


    def set_initial_conditions(self):
        pass


    def set_material(self):
        pass
