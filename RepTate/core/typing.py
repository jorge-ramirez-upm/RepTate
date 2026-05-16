"""Shared typing aliases for RepTate's core data flow."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, TypeAlias, TYPE_CHECKING

import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    from RepTate.core.DataTable import DataTable


FloatArray: TypeAlias = npt.NDArray[np.float64]
AnyArray: TypeAlias = npt.NDArray[Any]
FileParameterValue: TypeAlias = Any
FileParameters: TypeAlias = dict[str, FileParameterValue]


class FileLike(Protocol):
    """Minimal file contract used by theory calculation functions."""

    file_name_short: str
    data_table: DataTable
    file_parameters: FileParameters
    file_type: Any
    active: bool
    with_extra_x: bool


TheoryFunction: TypeAlias = Callable[[FileLike], None]
