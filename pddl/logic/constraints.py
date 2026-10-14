#
# Copyright 2021-2025 WhiteMech
#
# ------------------------------
#
# This file is part of pddl.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""This class implements PDDL constraints."""

import functools
from typing import Mapping, Union

from pddl.helpers.cache_hash import cache_hash
from pddl.logic.base import BinaryOp, Formula, UnaryOp
from pddl.logic.terms import Term, Variable
from pddl.parser.symbols import Symbols


class Always(UnaryOp):
    """The '(always gd)' constraint."""

    SYMBOL = Symbols.ALWAYS.value


class Sometime(UnaryOp):
    """The '(sometime gd)' constraint."""

    SYMBOL = Symbols.SOMETIME.value


class AtMostOnce(UnaryOp):
    """The '(at-most-once gd)' constraint."""

    SYMBOL = Symbols.AT_MOST_ONCE.value


class SometimeAfter(BinaryOp):
    """The '(sometime-after gd gd)' constraint."""

    SYMBOL = Symbols.SOMETIME_AFTER.value


class SometimeBefore(BinaryOp):
    """The '(sometime-before gd gd)' constraint."""

    SYMBOL = Symbols.SOMETIME_BEFORE.value


@cache_hash
@functools.total_ordering
class Within(Formula):
    """The '(within <num> gd)' constraint."""

    def __init__(self, time: Union[int, float], body: Formula) -> None:
        """Initialize the constraint."""
        self._time = time
        self._body = body

    @property
    def time(self) -> Union[int, float]:
        """Get the time bound."""
        return self._time

    @property
    def body(self) -> Formula:
        """Get the constrained goal description."""
        return self._body

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "Within":
        """Instantiate the constraint with a mapping from variables to terms."""
        return Within(self.time, self.body.instantiate(mapping))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({Symbols.WITHIN.value} {self.time} {self.body})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.time}, {self.body})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, Within)
            and self.time == other.time
            and self.body == other.body
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.time, self.body))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, Within):
            return str(self) < str(other)
        return NotImplemented


@cache_hash
@functools.total_ordering
class HoldAfter(Formula):
    """The '(hold-after <num> gd)' constraint."""

    def __init__(self, time: Union[int, float], body: Formula) -> None:
        """Initialize the constraint."""
        self._time = time
        self._body = body

    @property
    def time(self) -> Union[int, float]:
        """Get the time bound."""
        return self._time

    @property
    def body(self) -> Formula:
        """Get the constrained goal description."""
        return self._body

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "HoldAfter":
        """Instantiate the constraint with a mapping from variables to terms."""
        return HoldAfter(self.time, self.body.instantiate(mapping))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({Symbols.HOLD_AFTER.value} {self.time} {self.body})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.time}, {self.body})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, HoldAfter)
            and self.time == other.time
            and self.body == other.body
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.time, self.body))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, HoldAfter):
            return str(self) < str(other)
        return NotImplemented


@cache_hash
@functools.total_ordering
class AlwaysWithin(Formula):
    """The '(always-within <num> gd gd)' constraint."""

    def __init__(
        self, time: Union[int, float], first: Formula, second: Formula
    ) -> None:
        """Initialize the constraint."""
        self._time = time
        self._first = first
        self._second = second

    @property
    def time(self) -> Union[int, float]:
        """Get the time bound."""
        return self._time

    @property
    def first(self) -> Formula:
        """Get the first goal description."""
        return self._first

    @property
    def second(self) -> Formula:
        """Get the second goal description."""
        return self._second

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "AlwaysWithin":
        """Instantiate the constraint with a mapping from variables to terms."""
        return AlwaysWithin(
            self.time,
            self.first.instantiate(mapping),
            self.second.instantiate(mapping),
        )

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({Symbols.ALWAYS_WITHIN.value} {self.time} {self.first} {self.second})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.time}, {self.first}, {self.second})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, AlwaysWithin)
            and self.time == other.time
            and self.first == other.first
            and self.second == other.second
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.time, self.first, self.second))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, AlwaysWithin):
            return str(self) < str(other)
        return NotImplemented


@cache_hash
@functools.total_ordering
class HoldDuring(Formula):
    """The '(hold-during <num> <num> gd)' constraint."""

    def __init__(
        self, start: Union[int, float], end: Union[int, float], body: Formula
    ) -> None:
        """Initialize the constraint."""
        self._start = start
        self._end = end
        self._body = body

    @property
    def start(self) -> Union[int, float]:
        """Get the start time."""
        return self._start

    @property
    def end(self) -> Union[int, float]:
        """Get the end time."""
        return self._end

    @property
    def body(self) -> Formula:
        """Get the constrained goal description."""
        return self._body

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "HoldDuring":
        """Instantiate the constraint with a mapping from variables to terms."""
        return HoldDuring(self.start, self.end, self.body.instantiate(mapping))

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({Symbols.HOLD_DURING.value} {self.start} {self.end} {self.body})"

    def __repr__(self) -> str:
        """Get an unambiguous string representation."""
        return f"{type(self).__name__}({self.start}, {self.end}, {self.body})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, HoldDuring)
            and self.start == other.start
            and self.end == other.end
            and self.body == other.body
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.start, self.end, self.body))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, HoldDuring):
            return str(self) < str(other)
        return NotImplemented
