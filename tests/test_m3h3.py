from pytest import fixture, raises

import dolfin as df
from m3h3 import *
from m3h3.material import LinearElastic
from geometry import HeartGeometry, Microstructure, MarkerFunctions2D


def test_m3h3(geo, linear_elastic_material):
    ia1 = Interaction(Physics.ELECTRO, Physics.SOLID)
    ia2 = Interaction(Physics.SOLID, Physics.FLUID)
    with raises(Exception):
        parameters = Parameters("M3H3")
        parameters.set_electro_parameters()
        M3H3(geo, [Physics.ELECTRO], parameters, interactions=[ia2])
        M3H3(geo, [Physics.ELECTRO], parameters, interactions=[ia1])
        parameters.set_solid_parameters()
        M3H3(geo, [Physics.ELECTRO, Physics.SOLID], parameters,
                                                    interactions=[ia1, ia2])
    m = M3H3(geo, [Physics.ELECTRO, Physics.SOLID], parameters,
                material=linear_elastic_material)
    assert m


def test_setup_problems(m3h3):
    assert m3h3.electro_problem
    assert m3h3.solid_problem
    with raises(Exception):
        m3h3.fluid_problem
        m3h3.porous_problem


def test_solve(m3h3):
    # TODO:
    pass


@fixture
def m3h3(geo, linear_elastic_material):
    parameters = Parameters("M3H3")
    ia = Interaction(Physics.ELECTRO, Physics.SOLID)
    return M3H3(geo, parameters, interactions=[ia],
                material=linear_elastic_material)


@fixture
def mesh():
    return df.UnitCubeMesh(2, 2, 2)


@fixture
def markers():
    return {'BASE': (10, 1), 'ENDO': (30, 1), 'EPI': (40, 1), 'NONE': (0, 2)}


@fixture
def microstructure(mesh):
    VFS = df.VectorFunctionSpace(mesh, 'P', 1)
    f0 = df.interpolate(df.Constant((1.0, 0.0, 0.0)), VFS)
    s0 = df.interpolate(df.Constant((0.0, 1.0, 0.0)), VFS)
    n0 = df.interpolate(df.Constant((0.0, 0.0, 1.0)), VFS)
    return Microstructure(f0=f0, s0=s0, n0=n0)


@fixture
def markerfunctions(mesh, markers):
    class Base(df.SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and df.near(x[1], 0)

    class Endo(df.SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and df.near(x[0], 0)

    class Epi(df.SubDomain):
        def inside(self, x, on_boundary):
            return on_boundary and df.near(x[0], 1.0)

    ffun = df.MeshFunction("size_t", mesh, mesh.topology().dim()-1)
    ffun.set_all(markers['NONE'][0])
    base = Base()
    base.mark(ffun, markers['BASE'][0])
    endo = Endo()
    endo.mark(ffun, markers['ENDO'][0])
    epi = Epi()
    epi.mark(ffun, markers['EPI'][0])
    return MarkerFunctions2D(ffun=ffun)


@fixture
def geo(mesh, markers, microstructure, markerfunctions):
    return HeartGeometry(mesh, markers=markers, microstructure=microstructure,
                        markerfunctions=markerfunctions)


@fixture
def linear_elastic_material(geo):
    activation = df.Function(df.FunctionSpace(geo.mesh, "R", 0))
    activation.vector().zero()
    matparams = LinearElastic.default_parameters()
    return LinearElastic(activation=activation, parameters=matparams,
                            active_model="active_strain")