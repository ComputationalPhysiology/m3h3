from m3h3 import parameters, Physics


class M3H3(object):

    def __init__(self, geometry, interactions=[]):
        physics = parameters['M3H3'].keys()
        if Physics.ELECTRO in physics:
            self.setup_electro_problem()
        if Physics.SOLID in physics:
            self.setup_solid_problem()
        if Physics.FLUID in physics:
            self.setup_fluid_problem()
        if Physics.POROUS in physics:
            self.setup_porous_problem()

        # If multiple physics are defined, check that all are involved in an
        # interaction
        if len(physics) > 1:
            int_physics = set([ia.to_list() for ia in interactions])
            for p in physics:
                if p not in int_physics:
                    msg = "Physcis {} is set up, but does not appear in any interaction.".format(p)
                    raise KeyError(msg)





    def setup_electro_problem(self):
        pass


    def setup_solid_problem(self):
        pass


    def setup_fluid_problem(self):
        pass


    def setup_porous_problem(self):
        pass
