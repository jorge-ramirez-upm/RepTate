from __future__ import annotations

from types import SimpleNamespace
from typing import Any, cast

import numpy as np
import pytest

from RepTate.gui.QTheory import QTheory


def _qtheory_stub() -> QTheory:
    return QTheory.__new__(QTheory)


def test_table_as_html_formats_header_and_rows() -> None:
    theory = _qtheory_stub()

    html = theory.table_as_html([["Name", "Value"], ["tau", 1.25], ["G", "3.5"]])

    assert html.startswith('<table border="1" width="100%">')
    assert "<th>Name</th><th>Value</th>" in html
    assert "<td>tau</td><td>1.25</td>" in html
    assert html.endswith("</table><br>")


def test_table_as_html_omits_empty_header_row() -> None:
    theory = _qtheory_stub()

    html = theory.table_as_html([["", ""], ["tau", "1.25"]])

    assert "<th>" not in html
    assert "<td>tau</td><td>1.25</td>" in html


def test_table_as_ascii_joins_rows_with_spaces_and_newlines() -> None:
    theory = _qtheory_stub()

    text = theory.table_as_ascii([["Name", "Value"], ["tau", "1.25"]])

    assert text == "Name Value\ntau 1.25\n"


def test_strip_tags_returns_plain_text() -> None:
    theory = _qtheory_stub()

    assert theory.strip_tags("<b>tau</b><br><i>G</i>") == "tauG"


class _PrintSignalStub:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def emit(self, message: str) -> None:
        self.messages.append(message)


def test_qprint_emits_string_message_with_end_suffix() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    signal = _PrintSignalStub()
    dynamic_theory.print_signal = signal

    theory.Qprint("hello", end="<end>")

    assert signal.messages == ["hello<end>"]


def test_qprint_converts_table_payload_to_html() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    signal = _PrintSignalStub()
    dynamic_theory.print_signal = signal

    theory.Qprint([["Name"], ["tau"]])

    assert len(signal.messages) == 1
    assert "<th>Name</th>" in signal.messages[0]
    assert "<td>tau</td>" in signal.messages[0]
    assert signal.messages[0].endswith("<br><br>")


def test_get_material_parameters_returns_false_without_file_parameters() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    dynamic_theory.parent_dataset = SimpleNamespace(files=[])

    assert theory.get_material_parameters() is False


def test_get_material_parameters_returns_false_without_chemistry() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    dynamic_theory.parent_dataset = SimpleNamespace(
        files=[SimpleNamespace(file_parameters={"T": "25"})]
    )

    assert theory.get_material_parameters() is False


def test_fit_sigma_returns_none_for_absolute_error_fit() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    dynamic_theory.normalizebydata = False

    assert theory._fit_sigma(np.array([1.0, -2.0])) is None


def test_fit_sigma_uses_absolute_experimental_values_for_relative_error_fit() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    dynamic_theory.normalizebydata = True

    sigma = theory._fit_sigma(np.array([1.0, -2.0]))

    assert sigma is not None
    np.testing.assert_allclose(sigma, np.array([1.0, 2.0]))


def test_fit_sigma_rejects_zero_values_for_relative_error_fit() -> None:
    theory = _qtheory_stub()
    dynamic_theory = cast(Any, theory)
    dynamic_theory.normalizebydata = True

    with pytest.raises(ValueError, match="zero values"):
        theory._fit_sigma(np.array([1.0, 0.0]))
