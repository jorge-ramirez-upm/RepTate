"""Shared typing aliases for RepTate's core data flow."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol, TypeAlias, TYPE_CHECKING

import numpy as np
import numpy.typing as npt

if TYPE_CHECKING:
    from RepTate.core.DataTable import DataTable
    from RepTate.core.File import File
    from RepTate.core.File import FileParameterSpec


FloatArray: TypeAlias = npt.NDArray[np.float64]
AnyArray: TypeAlias = npt.NDArray[Any]
ModesResult: TypeAlias = tuple[FloatArray, FloatArray, bool]
FileParameterValue: TypeAlias = Any
FileParameters: TypeAlias = dict[str, FileParameterValue]
FileParameterSpecs: TypeAlias = dict[str, "FileParameterSpec"]
AxesArray: TypeAlias = list["AxesLike"]


class AxesLike(Protocol):
    """Minimal matplotlib axes contract used by theories."""

    xaxis: Any
    yaxis: Any
    spines: Any

    def autoscale(self, enable: bool = True, axis: str = "both", tight: bool | None = None) -> None: ...

    def autoscale_view(self, tight: bool | None = None, scalex: bool = True, scaley: bool = True) -> None: ...

    def axvspan(self, xmin: Any, xmax: Any, **kwargs: Any) -> Any: ...

    def axvline(self, x: Any = 0, **kwargs: Any) -> Any: ...

    def axhspan(self, ymin: Any, ymax: Any, **kwargs: Any) -> Any: ...

    def axhline(self, y: Any = 0, **kwargs: Any) -> Any: ...

    def get_xlim(self) -> tuple[Any, Any]: ...

    def get_ylim(self) -> tuple[Any, Any]: ...

    def get_position(self) -> Any: ...

    def relim(self, visible_only: bool = False) -> None: ...

    def set_aspect(self, aspect: Any, adjustable: Any | None = None, anchor: Any | None = None, share: bool = False) -> None: ...

    def set_position(self, pos: Any, which: str = "both") -> None: ...

    def set_subplotspec(self, subplotspec: Any) -> None: ...

    def set_visible(self, b: bool) -> None: ...

    def set_xlabel(self, xlabel: str, **kwargs: Any) -> Any: ...

    def set_ylabel(self, ylabel: str, **kwargs: Any) -> Any: ...

    def set_xscale(self, value: str, **kwargs: Any) -> None: ...

    def set_yscale(self, value: str, **kwargs: Any) -> None: ...

    def tick_params(self, *args: Any, **kwargs: Any) -> None: ...

    def grid(self, visible: Any = None, **kwargs: Any) -> None: ...

    def plot(self, *args: Any, **kwargs: Any) -> Any: ...

    def bar(self, *args: Any, **kwargs: Any) -> Any: ...

    def annotate(self, *args: Any, **kwargs: Any) -> Any: ...

    def legend(self, *args: Any, **kwargs: Any) -> Any: ...


class FileTypeLike(Protocol):
    """Minimal file type contract shared by loaded files and applications."""

    name: str
    extension: str
    description: str
    col_names: list[str]
    basic_file_parameters: list[str]
    col_units: list[str]
    file_parameter_specs: FileParameterSpecs


class FileLike(Protocol):
    """Minimal file contract used by theory calculation functions."""

    file_name_short: str
    file_full_path: str
    data_table: DataTable
    file_parameters: FileParameters
    file_type: FileTypeLike
    active: bool
    with_extra_x: bool
    nextramin: int
    nextramax: int


TheoryFunction: TypeAlias = Callable[[FileLike], None]


class ViewLike(Protocol):
    """Minimal plotting view contract used by theories."""

    name: str
    n: int
    log_x: bool
    log_y: bool
    x_axis: "AxisLike"
    y_axis: "AxisLike"

    def view_proc(
        self,
        dt: DataTable,
        file_parameters: FileParameters | None,
    ) -> tuple[Any, Any, bool]: ...

    def convert_xy_to_display(self, x: Any, y: Any) -> tuple[Any, Any]: ...

    def convert_xy_to_internal(self, x: Any, y: Any) -> tuple[Any, Any]: ...


class AxisLike(Protocol):
    """Minimal unit-aware axis contract exposed by views."""

    quantity: str

    def axis_label(self) -> str: ...

    def convert_from_internal(self, value: Any) -> Any: ...

    def convert_to_internal(self, value: Any) -> Any: ...


class ApplicationLike(Protocol):
    """Minimal application contract accessed through datasets, tools, and plots."""

    logger: Any
    axarr: AxesArray
    current_view: ViewLike
    multiviews: list[ViewLike]
    filetypes: dict[str, FileTypeLike]
    tools: Any
    parent_manager: Any
    datasets: dict[str, "DataSetLike"]
    DataSettabWidget: Any
    sp_nviews: Any
    current_viewtab: int
    viewComboBox: Any

    def update_plot(self) -> None: ...

    def update_Qplot(self) -> None: ...

    def update_all_ds_plots(self) -> None: ...

    def dataset_actions_disabled(self, state: bool) -> None: ...

    def set_view_tools(self, view_name: str) -> None: ...


class DataSetLike(Protocol):
    """Minimal dataset contract used by QTheory and theory implementations."""

    logger: Any
    files: list[File]
    current_file: File | None
    inactive_files: list[str]
    selected_file: File | None
    theories: dict[str, Any]
    parent_application: ApplicationLike
    nplots: int
    width: Any
    actionVertical_Limits: Any
    actionHorizontal_Limits: Any
    actionNew_Theory: Any
    actionMinimize_Error: Any
    actionShow_Limits: Any

    def minpositivecol(self, col: int) -> Any: ...

    def maxcol(self, col: int) -> Any: ...

    def handle_actionCalculate_Theory(self) -> None: ...

    def set_limit_icon(self) -> None: ...

    def do_plot(self, line: str) -> None: ...

    def end_of_computation(self, name: str) -> None: ...
