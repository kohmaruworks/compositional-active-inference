"""Bayesian Lens (deterministic): the three lens laws on generators and composites.

Generator lenses used here::

    l1 : int <-> int   get(a) = a + 1     put(a, b) = b - 1
    l2 : int <-> int   get(b) = b * 2     put(b, c) = c // 2

Both satisfy put-get, put-put, get-put on integers; their composite
``l1.then(l2)`` must satisfy them too.
"""

from __future__ import annotations

import itertools

import pytest

from src.lenses.bayes import Lens, identity_lens


@pytest.fixture
def l1() -> Lens[int, int]:
    return Lens(get=lambda a: a + 1, put=lambda _a, b: b - 1)


@pytest.fixture
def l2() -> Lens[int, int]:
    return Lens(get=lambda b: b * 2, put=lambda _b, c: c // 2)


SAMPLES_A = [-3, -1, 0, 1, 2, 7]
SAMPLES_B = [-2, 0, 4, 10]
SAMPLES_C = [-4, 0, 8, 20]


@pytest.mark.parametrize("a,b", list(itertools.product(SAMPLES_A, SAMPLES_B)))
def test_put_get(l1, a, b):
    assert l1.get(l1.put(a, b)) == b


@pytest.mark.parametrize("a,b,b2", list(itertools.product(SAMPLES_A, SAMPLES_B, SAMPLES_B)))
def test_put_put(l1, a, b, b2):
    assert l1.put(l1.put(a, b), b2) == l1.put(a, b2)


@pytest.mark.parametrize("a", SAMPLES_A)
def test_get_put(l1, a):
    assert l1.put(a, l1.get(a)) == a


@pytest.mark.parametrize("a,c", list(itertools.product(SAMPLES_A, SAMPLES_C)))
def test_composed_put_get(l1, l2, a, c):
    composed = l1.then(l2)
    assert composed.get(composed.put(a, c)) == c


@pytest.mark.parametrize(
    "a,c,c2", list(itertools.product(SAMPLES_A, SAMPLES_C, SAMPLES_C))
)
def test_composed_put_put(l1, l2, a, c, c2):
    composed = l1.then(l2)
    assert composed.put(composed.put(a, c), c2) == composed.put(a, c2)


@pytest.mark.parametrize("a", SAMPLES_A)
def test_composed_get_put(l1, l2, a):
    composed = l1.then(l2)
    assert composed.put(a, composed.get(a)) == a


@pytest.mark.parametrize("a,b", list(itertools.product(SAMPLES_A, SAMPLES_B)))
def test_identity_lens_is_neutral(l1, a, b):
    id_lens = identity_lens()
    composed_left = id_lens.then(l1)
    composed_right = l1.then(id_lens)
    assert composed_left.get(a) == l1.get(a)
    assert composed_left.put(a, b) == l1.put(a, b)
    assert composed_right.get(a) == l1.get(a)
    assert composed_right.put(a, b) == l1.put(a, b)
