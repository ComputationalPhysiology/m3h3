from pytest import fixture, raises

import dolfin as df
from m3h3 import *
from geometry import Geometry2D


def test_m3h3(geo):
    ia1 = Interaction(Physics.ELECTRO, Physics.SOLID)
    ia2 = Interaction(Physics.SOLID, Physics.FLUID)
    with raises(Exception):
        assert M3H3(geo, interactions=[ia1, ia2])
        assert M3H3(geo, interactions=[ia2])
        assert M3H3(geo, interactions=[ia1])
    assert M3H3(geo)
    set_electro_parameters()
    set_solid_parameters()
    with raises(Exception):
        assert M3H3(geo, interactions=[ia1, ia2])
        assert M3H3(geo, interactions=[ia2])
    assert M3H3(geo, interactions=[ia1])


def test_solve(m3h3):
    solutions = m3h3.solver()
    dt = parameters['Electro']['dt']
    time_range = m3h3.interval[1]-m3h3.interval[0]
    steps = int(time_range/dt)
    assert len(solutions) == steps


@fixture
def m3h3(geo):
    ia = Interaction(Physics.ELECTRO, Physics.SOLID)
    return M3H3(geo, interactions=[ia])


@fixture
def geo():
    mesh = df.UnitSquareMesh(2, 2)
    return Geometry2D(mesh)
