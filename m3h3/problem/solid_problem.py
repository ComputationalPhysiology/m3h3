import dolfin as df

from m3h3.problem.problem import Problem


class SolidProblem(Problem):

    def __init__(self, geometry, parameters, *args, **kwargs):
        super().__init__(geometry, *args, **kwargs)
