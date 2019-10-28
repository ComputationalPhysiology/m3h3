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
    set_electro_default_parameters()
    set_solid_default_parameters()
    with raises(Exception):
        assert M3H3(geo, interactions=[ia1, ia2])
        assert M3H3(geo, interactions=[ia2])
    print(parameters.keys())
    assert M3H3(geo, interactions=[ia1])


@fixture
def geo():
    mesh = df.UnitSquareMesh(2, 2)
    return Geometry2D(mesh)
