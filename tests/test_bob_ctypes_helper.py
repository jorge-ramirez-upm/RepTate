import importlib

import pytest


bob_module = importlib.import_module("RepTate.theories.BobCtypesHelper")


def test_bob_loader_failure_raises_bob_error(monkeypatch):
    loader_error = OSError("The specified module could not be found")

    def fail_to_load(path):
        raise loader_error

    monkeypatch.setattr(bob_module, "CDLL", fail_to_load)
    monkeypatch.setattr(
        bob_module.BobCtypesHelper,
        "link_c_functions",
        lambda self: pytest.fail("link_c_functions must not run after a loader failure"),
    )

    with pytest.raises(bob_module.BobError, match="Could not load BoB shared library") as caught:
        bob_module.BobCtypesHelper(object())

    assert caught.value.__cause__ is loader_error
