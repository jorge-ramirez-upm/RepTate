def test_import_reptate():
    import RepTate  # noqa

    assert RepTate is not None


def test_import_rc_and_ui():
    import RepTate.gui.Reptate_rc  # noqa
    import RepTate.gui.Tool_rc  # noqa
    import RepTate.gui.Ui_ToolTab  # noqa


def test_import_tools():
    import RepTate.tools.polymer_data  # noqa
    import RepTate.tools.ToolResampleData  # noqa


def test_version_exists():
    import RepTate

    assert hasattr(RepTate, "__version__")
    assert isinstance(RepTate.__version__, str)
    assert len(RepTate.__version__) > 0
