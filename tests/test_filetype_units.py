import numpy as np

from RepTate.core.FileType import TXTColumnFile


def test_txt_column_file_attaches_column_specs_and_converts_known_units(tmp_path):
    data_file = tmp_path / "sample.dat"
    data_file.write_text(
        "\n"
        "1 2 3\n"
        "2 4 6\n",
        encoding="latin-1",
    )
    ftype = TXTColumnFile(
        name="Sample",
        extension="dat",
        description="Sample data",
        col_names=["time", "stress", "molar_mass"],
        col_units=["min", "kPa", "g/mol"],
    )

    file = ftype.read_file(str(data_file), parent_dataset=None, axarr=None)

    assert file.data_table.column_names == ["time", "stress", "molar_mass"]
    assert file.data_table.column_units == ["min", "kPa", "g/mol"]
    assert [spec.internal_unit for spec in file.data_table.column_specs] == [
        "s",
        "Pa",
        "g/mol",
    ]
    np.testing.assert_allclose(
        file.data_table.data,
        np.array(
            [
                [60, 2000, 3],
                [120, 4000, 6],
            ]
        ),
    )


def test_txt_column_file_uses_app_units_when_header_has_no_units(tmp_path):
    data_file = tmp_path / "sample_header.dat"
    data_file.write_text(
        "\n"
        "time stress\n"
        "1 2\n"
        "2 4\n",
        encoding="latin-1",
    )
    ftype = TXTColumnFile(
        name="Sample",
        extension="dat",
        description="Sample data",
        col_names=["time", "stress"],
        col_units=["min", "kPa"],
    )

    file = ftype.read_file(str(data_file), parent_dataset=None, axarr=None)

    assert file.data_table.column_names == ["time", "stress"]
    assert file.data_table.column_units == ["min", "kPa"]
    assert [spec.internal_unit for spec in file.data_table.column_specs] == ["s", "Pa"]
    np.testing.assert_allclose(file.data_table.data, np.array([[60, 2000], [120, 4000]]))


def test_txt_column_file_uses_units_declared_in_header(tmp_path):
    data_file = tmp_path / "sample_header_units.dat"
    data_file.write_text(
        "\n"
        "time [h] stress [MPa]\n"
        "1 2\n"
        "2 4\n",
        encoding="latin-1",
    )
    ftype = TXTColumnFile(
        name="Sample",
        extension="dat",
        description="Sample data",
        col_names=["time", "stress"],
        col_units=["min", "kPa"],
    )

    file = ftype.read_file(str(data_file), parent_dataset=None, axarr=None)

    assert file.data_table.column_names == ["time", "stress"]
    assert file.data_table.column_units == ["h", "MPa"]
    assert [spec.internal_unit for spec in file.data_table.column_specs] == ["s", "Pa"]
    np.testing.assert_allclose(
        file.data_table.data,
        np.array([[3600, 2_000_000], [7200, 4_000_000]]),
    )


def test_txt_column_file_converts_mwd_molar_mass_to_g_per_mol(tmp_path):
    data_file = tmp_path / "sample_mwd.dat"
    data_file.write_text(
        "\n"
        "M [kg/mol] W(logM)\n"
        "1 0.2\n"
        "2 0.4\n",
        encoding="latin-1",
    )
    ftype = TXTColumnFile(
        name="GPC Files",
        extension="gpc",
        description="Molecular Weight Distribution",
        col_names=["M", "W(logM)"],
        col_units=["g/mol", "-"],
    )

    file = ftype.read_file(str(data_file), parent_dataset=None, axarr=None)

    assert file.data_table.column_units == ["kg/mol", "-"]
    assert [spec.internal_unit for spec in file.data_table.column_specs] == [
        "g/mol",
        "-",
    ]
    np.testing.assert_allclose(
        file.data_table.data,
        np.array(
            [
                [1000, 0.2],
                [2000, 0.4],
            ]
        ),
    )


def test_txt_column_file_converts_hz_to_rad_per_s_when_app_expects_angular_frequency(tmp_path):
    data_file = tmp_path / "sample_lve.dat"
    data_file.write_text(
        "\n"
        "w [Hz] G' G''\n"
        "1 2 3\n"
        "2 4 6\n",
        encoding="latin-1",
    )
    ftype = TXTColumnFile(
        name="LVE files",
        extension="tts",
        description="LVE files",
        col_names=["w", "G'", "G''"],
        col_units=["rad/s", "Pa", "Pa"],
    )

    file = ftype.read_file(str(data_file), parent_dataset=None, axarr=None)

    assert file.data_table.column_units == ["Hz", "Pa", "Pa"]
    assert [spec.internal_unit for spec in file.data_table.column_specs] == [
        "rad/s",
        "Pa",
        "Pa",
    ]
    np.testing.assert_allclose(
        file.data_table.data,
        np.array(
            [
                [2 * np.pi, 2, 3],
                [4 * np.pi, 4, 6],
            ]
        ),
    )
