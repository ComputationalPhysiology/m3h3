from pytest import fixture, raises

import dolfin as df
import m3h3


def test_set_dolfin_compiler_parameters():
    flags = ["-O3", "-ffast-math", "-march=native"]
    assert df.parameters["form_compiler"]["quadrature_degree"] == 4
    assert df.parameters["form_compiler"]["representation"] == "uflacs"
    assert df.parameters["form_compiler"]["cpp_optimize"]
    assert df.parameters["form_compiler"]["cpp_optimize_flags"] == " ".join(flags)


def test_set_electro_parameters(parameters):
    assert m3h3.Physics.ELECTRO.value not in parameters.keys()
    dt = 0.1
    parameter = {"dt": dt}
    parameters.set_electro_parameters(parameters=parameter)
    assert m3h3.Physics.ELECTRO.value in parameters.keys()
    assert parameters[m3h3.Physics.ELECTRO.value]["dt"] == dt
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        parameters.set_electro_parameters(parameters=parameter)


def test_set_solid_parameters(parameters):
    assert m3h3.Physics.SOLID.value not in parameters.keys()
    parameter = {"dummy_parameter": True}
    parameters.set_solid_parameters(parameters=parameter)
    assert m3h3.Physics.SOLID.value in parameters.keys()
    assert parameters[m3h3.Physics.SOLID.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        parameters.set_solid_parameters(parameters=parameter)


def test_set_fluid_parameters(parameters):
    assert m3h3.Physics.FLUID.value not in parameters.keys()
    parameter = {"dummy_parameter": True}
    parameters.set_fluid_parameters(parameters=parameter)
    assert m3h3.Physics.FLUID.value in parameters.keys()
    assert parameters[m3h3.Physics.FLUID.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        parameters.set_fluid_parameters(parameters=parameter)


def test_set_porous_parameters(parameters):
    assert m3h3.Physics.POROUS.value not in parameters.keys()
    parameter = {"dummy_parameter": True}
    parameters.set_porous_parameters(parameters=parameter)
    assert m3h3.Physics.POROUS.value in parameters.keys()
    assert parameters[m3h3.Physics.POROUS.value]["dummy_parameter"]
    parameter = {'invalid_parameter': True}
    with raises(Exception):
        parameters.set_porous_parameters(parameters=parameter)


@fixture
def parameters():
    return m3h3.Parameters("M3H3")
