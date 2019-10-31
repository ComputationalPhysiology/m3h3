from pytest import raises

import dolfin as df
import m3h3


def test_set_dolfin_compiler_parameters():
    flags = ["-O3", "-ffast-math", "-march=native"]
    assert df.parameters["form_compiler"]["quadrature_degree"] == 4
    assert df.parameters["form_compiler"]["representation"] == "uflacs"
    assert df.parameters["form_compiler"]["cpp_optimize"]
    assert df.parameters["form_compiler"]["cpp_optimize_flags"] == " ".join(flags)


def test_set_electro_parameters():
    m3h3.reset_m3h3_parameters()
    assert m3h3.Physics.ELECTRO.value not in m3h3.parameters.keys()
    theta = 0.1
    parameter = {"theta": theta}
    m3h3.set_electro_parameters(parameters=parameter)
    assert m3h3.Physics.ELECTRO.value in m3h3.parameters.keys()
    assert m3h3.parameters[m3h3.Physics.ELECTRO.value]["theta"] == theta
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        m3h3.set_electro_parameters(parameters=parameter)


def test_set_solid_parameters():
    m3h3.reset_m3h3_parameters()
    assert m3h3.Physics.SOLID.value not in m3h3.parameters.keys()
    parameter = {"dummy_parameter": True}
    m3h3.set_solid_parameters(parameters=parameter)
    assert m3h3.parameters[m3h3.Physics.SOLID.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        m3h3.set_solid_parameters(parameters=parameter)


def test_set_fluid_default_parameters():
    m3h3.reset_m3h3_parameters()
    assert m3h3.Physics.FLUID.value not in m3h3.parameters.keys()
    parameter = {"dummy_parameter": True}
    m3h3.set_fluid_parameters(parameters=parameter)
    assert m3h3.parameters[m3h3.Physics.FLUID.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        m3h3.set_fluid_parameters(parameters=parameter)

def test_set_porous_parameters():
    m3h3.reset_m3h3_parameters()
    assert m3h3.Physics.POROUS.value not in m3h3.parameters.keys()
    parameter = {"dummy_parameter": True}
    m3h3.set_porous_parameters(parameters=parameter)
    assert m3h3.parameters[m3h3.Physics.POROUS.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        m3h3.set_porous_parameters(parameters=parameter)
