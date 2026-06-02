import textwrap

import numpy as np
import pytest

from RepTate.theories.TheoryBaumgaertelWinter import read_maxwell_modes_file
from RepTate.theories.TheoryBaumgaertelWinter import TheoryBaumgaertelWinter
from RepTate.theories.TheoryBaumgaertelWinter import _format_decision
from RepTate.theories.TheoryBaumgaertelWinter import _format_residual
from RepTate.theories.TheoryBaumgaertelWinter import _format_residual_change
from RepTate.theories.TheoryBaumgaertelWinter import _format_simplification_report_table
from RepTate.theories.TheoryBaumgaertelWinter import _SimplificationReportEvent


def test_read_maxwell_modes_file_valid_reptate_format(tmp_path):
    path = tmp_path / "modes.txt"
    path.write_text(
        textwrap.dedent(
            """
            # Maxwell modes
            #number of modes
            4

            #   i          tau_i            G_i
                1       0.00049825          99779
                2      0.000762803        178.269
                3          5.65798     0.00618056
                4          50763.6       0.988396

            #end
            """
        )
    )

    tau, G = read_maxwell_modes_file(str(path))

    np.testing.assert_allclose(tau, [0.00049825, 0.000762803, 5.65798, 50763.6])
    np.testing.assert_allclose(G, [99779, 178.269, 0.00618056, 0.988396])


def test_read_maxwell_modes_file_rejects_count_mismatch(tmp_path):
    path = tmp_path / "modes.txt"
    path.write_text(
        textwrap.dedent(
            """
            #number of modes
            2
            1 1.0 10.0
            """
        )
    )

    with pytest.raises(ValueError, match="Expected 2 modes"):
        read_maxwell_modes_file(str(path))


def test_read_maxwell_modes_file_rejects_malformed_line(tmp_path):
    path = tmp_path / "modes.txt"
    path.write_text("1 1.0 10.0 extra\n")

    with pytest.raises(ValueError, match="Malformed Maxwell mode line"):
        read_maxwell_modes_file(str(path))


def test_read_maxwell_modes_file_rejects_nonpositive_modes(tmp_path):
    path = tmp_path / "modes.txt"
    path.write_text("1 1.0 0.0\n")

    with pytest.raises(ValueError, match="positive tau_i and G_i"):
        read_maxwell_modes_file(str(path))


def test_simplification_report_formatting_helpers():
    assert _format_residual(0.02746) == "2.746e-02"
    assert _format_residual_change(0.02, 0.021) == "Δ = +5%"
    assert _format_decision(True) == '<font color="green">accepted</font>'
    assert _format_decision(False) == '<font color="red">rejected</font>'


def test_simplification_report_table_contains_expected_row():
    html = _format_simplification_report_table(
        [
            _SimplificationReportEvent(
                pass_number=1,
                operation="trial deletion",
                modes_before=2,
                modes_after=1,
                residual_before=2.789e-2,
                residual_after=3.976e-1,
                accepted=False,
                note="best candidate rejected",
                mode_index=0,
            )
        ]
    )

    assert "<table" in html
    assert "trial deletion" in html
    assert "2 &rarr; 1" in html
    assert '<font color="red">rejected</font>' in html
    assert "best candidate rejected; mode 0" in html


def test_baumgaertel_winter_pack_unpack_modes_roundtrip():
    theory = TheoryBaumgaertelWinter.__new__(TheoryBaumgaertelWinter)
    tau = np.array([0.01, 1.0, 100.0])
    G = np.array([10.0, 20.0, 30.0])

    packed = theory._pack_modes(tau, G)
    unpacked_tau, unpacked_G = theory._unpack_modes(packed)

    np.testing.assert_allclose(packed, [-2.0, 0.0, 2.0, 1.0, 1.0 + np.log10(2.0), 1.0 + np.log10(3.0)])
    np.testing.assert_allclose(unpacked_tau, tau)
    np.testing.assert_allclose(unpacked_G, G)


def test_baumgaertel_winter_merge_close_modes_uses_modulus_weighted_log_tau():
    theory = TheoryBaumgaertelWinter.__new__(TheoryBaumgaertelWinter)
    theory.min_logtau_separation = 0.25
    tau = np.array([1.0, 10.0, 1.1])
    G = np.array([2.0, 5.0, 4.0])

    merged_tau, merged_G, n_merged = theory._merge_close_mode_arrays(tau, G)

    expected_logtau = (2.0 * np.log10(1.0) + 4.0 * np.log10(1.1)) / 6.0
    np.testing.assert_allclose(merged_tau, [10.0**expected_logtau, 10.0])
    np.testing.assert_allclose(merged_G, [6.0, 5.0])
    assert n_merged == 1


def test_baumgaertel_winter_weak_mode_candidates_keep_strongest_mode():
    theory = TheoryBaumgaertelWinter.__new__(TheoryBaumgaertelWinter)
    theory.weak_mode_threshold = 0.2

    assert theory._weak_mode_indices(np.array([1.0, 100.0, 2.0])) == [0, 2]

    theory.weak_mode_threshold = 2.0
    assert theory._weak_mode_indices(np.array([1.0, 2.0, 3.0])) == [0, 1]


def test_baumgaertel_winter_residual_increase_acceptance_uses_floor_and_threshold():
    theory = TheoryBaumgaertelWinter.__new__(TheoryBaumgaertelWinter)
    theory.max_residual_increase = 0.05

    assert theory._residual_increase_is_acceptable(0.1, 0.09) is True
    assert theory._residual_increase_is_acceptable(0.1, 0.104) is True
    assert theory._residual_increase_is_acceptable(0.1, 0.106) is False
    assert theory._residual_increase_is_acceptable(0.0, 1.0e-10) is True
    assert theory._residual_increase_is_acceptable(0.0, 1.0e-6) is False
    assert theory._residual_increase_is_acceptable(0.1, np.inf) is False
