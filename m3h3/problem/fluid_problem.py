import dolfin as df

from m3h3.problem.problem import Problem


class FluidProblem(Problem):

    def __init__(self, geometry, time, parameters, **kwargs):
        super().__init__(geometry, time, parameters, **kwargs)
        self._form = self._init_form()


    def _init_form(self):
        return 0
