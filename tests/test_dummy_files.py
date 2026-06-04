from types import SimpleNamespace

import numpy as np
import numpy.testing as npt

from RepTate.core.FileType import TXTColumnFile
from RepTate.gui.QDataSet import QDataSet


def _dataset_stub() -> QDataSet:
    dataset = QDataSet.__new__(QDataSet)
    dataset.files = []
    dataset.current_file = None
    dataset.theories = {}
    dataset.parent_application = SimpleNamespace(axarr=None)
    return dataset


def test_dummy_file_fills_all_expected_columns_with_scalar_y_value() -> None:
    ftype = TXTColumnFile(
        name="LVE files",
        extension="tts",
        description="LVE files",
        col_names=["w", "G'", "G''"],
    )

    file, success = _dataset_stub().new_dummy_file(
        xrange=np.array([1.0, 10.0]),
        yval=7.0,
        fparams={},
        file_type=ftype,
    )

    assert success
    npt.assert_allclose(file.data_table.data, np.array([[1.0, 7.0, 7.0], [10.0, 7.0, 7.0]]))


def test_dummy_file_preserves_explicit_extra_column_values() -> None:
    ftype = TXTColumnFile(
        name="React files",
        extension="reac",
        description="React files",
        col_names=["M", "w(M)", "g", "br/1000C"],
    )

    file, success = _dataset_stub().new_dummy_file(
        xrange=np.array([1.0, 2.0]),
        yval=7.0,
        zval=np.array([3.0, 4.0]),
        z2val=np.array([5.0, 6.0]),
        fparams={},
        file_type=ftype,
    )

    assert success
    npt.assert_allclose(file.data_table.data, np.array([[1.0, 7.0, 3.0, 5.0], [2.0, 7.0, 4.0, 6.0]]))
