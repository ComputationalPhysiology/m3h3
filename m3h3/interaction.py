
class Interaction(object):

    def __init__(self, var1, var2):
        self._var1 = var1
        self._var2 = var2


    def to_list(self):
        return [self._var1, self._var2]
