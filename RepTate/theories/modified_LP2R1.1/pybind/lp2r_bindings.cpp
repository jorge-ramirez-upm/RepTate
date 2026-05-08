#include "lp2r_solver.h"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;
using namespace reptate_lp2r;

PYBIND11_MODULE(_lp2r, m)
{
    m.doc() = "pybind11 bindings for the RepTate LP2R linear rheology solver";

    py::class_<LP2RMaterial>(m, "Material")
        .def(py::init<>())
        .def_readwrite("m_kuhn", &LP2RMaterial::m_kuhn)
        .def_readwrite("m_e", &LP2RMaterial::m_e)
        .def_readwrite("g0", &LP2RMaterial::g0)
        .def_readwrite("tau_e", &LP2RMaterial::tau_e)
        .def_readwrite("g_glass", &LP2RMaterial::g_glass)
        .def_readwrite("tau_glass", &LP2RMaterial::tau_glass)
        .def_readwrite("beta_glass", &LP2RMaterial::beta_glass);

    py::class_<LP2RControls>(m, "Controls")
        .def(py::init<>())
        .def_readwrite("alpha", &LP2RControls::alpha)
        .def_readwrite("t_cr_start", &LP2RControls::t_cr_start)
        .def_readwrite("delta_cr", &LP2RControls::delta_cr)
        .def_readwrite("b_zeta", &LP2RControls::b_zeta)
        .def_readwrite("a_eq", &LP2RControls::a_eq)
        .def_readwrite("b_eq", &LP2RControls::b_eq)
        .def_readwrite("ret_pref", &LP2RControls::ret_pref)
        .def_readwrite("ret_pref_0", &LP2RControls::ret_pref_0)
        .def_readwrite("ret_switch_exponent", &LP2RControls::ret_switch_exponent)
        .def_readwrite("rept_switch_factor", &LP2RControls::rept_switch_factor)
        .def_readwrite("rouse_switch_factor", &LP2RControls::rouse_switch_factor)
        .def_readwrite("disentanglement_switch", &LP2RControls::disentanglement_switch)
        .def_readwrite("start_time", &LP2RControls::start_time)
        .def_readwrite("time_ratio", &LP2RControls::time_ratio);

    py::class_<LP2RResult>(m, "Result")
        .def_readonly("omega", &LP2RResult::omega)
        .def_readonly("gp", &LP2RResult::gp)
        .def_readonly("gpp", &LP2RResult::gpp)
        .def_readonly("eta", &LP2RResult::eta)
        .def_readonly("mn", &LP2RResult::mn)
        .def_readonly("mw", &LP2RResult::mw)
        .def_readonly("pdi", &LP2RResult::pdi)
        .def_readonly("eta0", &LP2RResult::eta0);

    py::class_<LP2RSolver>(m, "Solver")
        .def(py::init<LP2RMaterial, LP2RControls>(), py::arg("material"), py::arg("controls"))
        .def("add_lognormal_component", &LP2RSolver::add_lognormal_component,
             py::arg("weight"), py::arg("n"), py::arg("mw"), py::arg("pdi"))
        .def("add_discrete_component", &LP2RSolver::add_discrete_component,
             py::arg("mass"), py::arg("weight"), py::arg("component_weight") = 1.0)
        .def("prepare", &LP2RSolver::prepare)
        .def("step", &LP2RSolver::step)
        .def("run_relaxation", &LP2RSolver::run_relaxation)
        .def("calculate_spectra", &LP2RSolver::calculate_spectra,
             py::arg("freq_min"), py::arg("freq_max"), py::arg("freq_ratio"))
        .def("run", &LP2RSolver::run,
             py::arg("freq_min"), py::arg("freq_max"), py::arg("freq_ratio"))
        .def("cancel", &LP2RSolver::cancel)
        .def("cancelled", &LP2RSolver::cancelled)
        .def("progress", &LP2RSolver::progress)
        .def("prepared", &LP2RSolver::prepared);
}
