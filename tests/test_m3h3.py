from pytest import fixture, raises

import dolfin as df
from m3h3 import *
from geometry import Geometry2D


def test_m3h3(geo):
    ia1 = Interaction(Physics.ELECTRO, Physics.SOLID)
    ia2 = Interaction(Physics.SOLID, Physics.FLUID)
    with raises(Exception):
        M3H3(geo, physics=[Physics.ELECTRO, Physics.SOLID],
                                                    interactions=[ia1, ia2])
        M3H3(geo, physics=[Physics.ELECTRO], interactions=[ia2])
        M3H3(geo, physics=[Physics.ELECTRO], interactions=[ia1])
    m = M3H3(geo, physics=[Physics.ELECTRO, Physics.SOLID])
    assert m


def test_solve(m3h3):
    # TODO:
    pass


@fixture
def m3h3(geo):
    ia = Interaction(Physics.ELECTRO, Physics.SOLID)
    physics = [Physics.ELECTRO, Physics.SOLID]
    return M3H3(geo, physics, interactions=[ia])


@fixture
def geo():
    mesh = df.UnitSquareMesh(2, 2)
    return Geometry2D(mesh)
