import textwrap

import numpy as np
import pytest

from RepTate.theories.TheoryBaumgaertelWinter import read_maxwell_modes_file
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
