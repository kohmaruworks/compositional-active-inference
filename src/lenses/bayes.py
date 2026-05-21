"""Bayesian lenses (deterministic baseline, before lifting to channels).

A lens ``A <-> B`` is the pair (``get: A -> B``, ``put: (A, B) -> A``).
The three lens laws are::

    put-get :  get(put(a, b)) == b
    put-put :  put(put(a, b), b') == put(a, b')
    get-put :  put(a, get(a)) == a

Composition is defined on objects ``A <-> B`` and ``B <-> C`` by::

    (m . l).get(a)    = m.get(l.get(a))
    (m . l).put(a, c) = l.put(a, m.put(l.get(a), c))

and preserves all three laws when each component does. This module realises
the deterministic skeleton; the Bayesian (stochastic) extension upgrades
``put`` to a backward channel which will live in ``src/lenses/`` alongside
this file.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


@dataclass(frozen=True)
class Lens(Generic[A, B]):
    get: Callable[[A], B]
    put: Callable[[A, B], A]

    def then(self, other: "Lens[B, C]") -> "Lens[A, C]":
        get_l, put_l = self.get, self.put
        get_r, put_r = other.get, other.put

        def composed_get(a: A) -> C:
            return get_r(get_l(a))

        def composed_put(a: A, c: C) -> A:
            return put_l(a, put_r(get_l(a), c))

        return Lens(get=composed_get, put=composed_put)


def identity_lens() -> Lens[Any, Any]:
    return Lens(get=lambda a: a, put=lambda _a, b: b)
