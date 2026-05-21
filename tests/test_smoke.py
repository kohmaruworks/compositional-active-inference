"""Smoke tests: package layout + minimal compositional identity law."""

import importlib

import pytest


@pytest.mark.parametrize(
    "module_name",
    [
        "src.categories",
        "src.lenses",
        "src.dynamics",
        "src.cosmology",
    ],
)
def test_module_importable(module_name: str) -> None:
    importlib.import_module(module_name)


def test_identity_composition_law() -> None:
    from discopy.cat import Ob, Box, Id

    x = Ob("X")
    f = Box("f", x, x)
    assert Id(x) >> f == f
    assert f >> Id(x) == f
