import dolfin as df

from m3h3.problem.problem import Problem


class FluidProblem(Problem):

    def __init__(self, geometry, time, *args, **kwargs):
        super().__init__(geometry, time, **kwargs)
