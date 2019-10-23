import m3h3
import dolfin as df


def test_set_dolfin_compiler_parameters():
    flags = ["-O3", "-ffast-math", "-march=native"]
    assert df.parameters["form_compiler"]["quadrature_degree"] == 4
    assert df.parameters["form_compiler"]["representation"] == "uflacs"
    assert df.parameters["form_compiler"]["cpp_optimize"]
    assert df.parameters["form_compiler"]["cpp_optimize_flags"] == " ".join(flags)


def test_set_electro_default_parameters():
    assert "Electro" not in m3h3.parameters.keys()
    m3h3.set_electro_default_parameters()
    assert "Electro" in m3h3.parameters.keys()


def test_set_solid_default_parameters():
    assert "Solid" not in m3h3.parameters.keys()
    m3h3.set_solid_default_parameters()
    assert "Solid" in m3h3.parameters.keys()


def test_set_fluid_default_parameters():
    assert "Fluid" not in m3h3.parameters.keys()
    m3h3.set_fluid_default_parameters()
    assert "Fluid" in m3h3.parameters.keys()


def test_set_porous_default_parameters():
    assert "Porous" not in m3h3.parameters.keys()
    m3h3.set_porous_default_parameters()
    assert "Porous" in m3h3.parameters.keys()
