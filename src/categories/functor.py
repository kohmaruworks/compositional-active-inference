"""Minimal Functor abstraction over ``discopy.cat``.

A functor ``F: C -> D`` is the pair of an object map and an arrow map which
preserves identities and composition::

    F(id_X)   = id_{F(X)}
    F(g . f)  = F(g) . F(f)

Here ``D`` is the category of Python types and callables: ``F`` maps each
``discopy.cat.Ob`` to a (carrier) Python type and each generating
``discopy.cat.Box`` to a one-argument Python callable. The arrow map is then
extended to composite arrows by walking ``Arrow.inside`` and composing the
callables; that construction is what makes the composition law automatic on
arrows once it holds on generators.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from discopy.cat import Arrow, Box, Ob


@dataclass
class Functor:
    ob: dict[Ob, Any] = field(default_factory=dict)
    ar: dict[Box, Callable[[Any], Any]] = field(default_factory=dict)

    def on_object(self, x: Ob) -> Any:
        if x not in self.ob:
            raise KeyError(f"Functor has no object map entry for {x!r}")
        return self.ob[x]

    def on_arrow(self, arrow: Arrow) -> Callable[[Any], Any]:
        result: Callable[[Any], Any] = lambda v: v
        for box in arrow.inside:
            if box not in self.ar:
                raise KeyError(f"Functor has no arrow map entry for {box!r}")
            step = self.ar[box]
            prev = result
            result = lambda v, step=step, prev=prev: step(prev(v))
        return result

    def __call__(self, x: Ob | Arrow) -> Any:
        if isinstance(x, Arrow):
            return self.on_arrow(x)
        if isinstance(x, Ob):
            return self.on_object(x)
        raise TypeError(
            f"Functor applies to Ob or Arrow, got {type(x).__name__}"
        )
