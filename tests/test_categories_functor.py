"""Functor: identity preservation and composition preservation.

Asserts the categorical laws on a small concrete category with three
objects and two generating arrows::

      f       g
    X --> Y --> Z

mapped by ``F`` to integer carriers and Python callables.
"""

from __future__ import annotations

import pytest
from discopy.cat import Box, Id, Ob

from src.categories.functor import Functor


@pytest.fixture
def category():
    X, Y, Z = Ob("X"), Ob("Y"), Ob("Z")
    f = Box("f", X, Y)
    g = Box("g", Y, Z)
    return X, Y, Z, f, g


@pytest.fixture
def F(category):
    X, Y, Z, f, g = category
    return Functor(
        ob={X: int, Y: int, Z: int},
        ar={f: lambda v: v + 1, g: lambda v: v * 2},
    )


@pytest.mark.parametrize("v", [-5, -1, 0, 1, 7, 42])
def test_functor_preserves_identity(category, F, v):
    X, *_ = category
    F_id = F(Id(X))
    assert F_id(v) == v


@pytest.mark.parametrize("v", [-5, -1, 0, 1, 7, 42])
def test_functor_preserves_composition(category, F, v):
    _X, _Y, _Z, f, g = category
    F_composed = F(f >> g)
    assert F_composed(v) == F(g)(F(f)(v))


def test_functor_object_map(category, F):
    X, Y, Z, *_ = category
    assert F(X) is int
    assert F(Y) is int
    assert F(Z) is int


def test_functor_unknown_object_raises(category):
    X, *_ = category
    F = Functor(ob={}, ar={})
    with pytest.raises(KeyError):
        F(X)
