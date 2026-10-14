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

"""This class implements PDDL preferences."""

import functools
from typing import Mapping, Optional

from pddl.helpers.cache_hash import cache_hash
from pddl.logic.base import Formula
from pddl.logic.functions import FunctionExpression
from pddl.logic.terms import Term, Variable
from pddl.parser.symbols import Symbols


@cache_hash
@functools.total_ordering
class Preference(Formula):
    """A class for a PDDL preference, e.g., '(preference name (p ?x))'."""

    def __init__(self, body: Formula, name: Optional[str] = None) -> None:
        """Initialize a preference."""
        self._body = body
        self._name = name

    @property
    def body(self) -> Formula:
        """Get the preferred condition."""
        return self._body

    @property
    def name(self) -> Optional[str]:
        """Get the preference name, if any."""
        return self._name

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "Preference":
        """Instantiate the preference with a mapping from variables to terms."""
        return Preference(self.body.instantiate(mapping), self.name)

    def __str__(self) -> str:
        """Get the string representation."""
        if self.name is None:
            return f"({Symbols.PREFERENCE.value} {self.body})"
        return f"({Symbols.PREFERENCE.value} {self.name} {self.body})"

    def __repr__(self) -> str:
        """Get the unambiguous string representation."""
        return f"{type(self).__name__}({self.body}, name={self.name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return (
            isinstance(other, Preference)
            and self.body == other.body
            and self.name == other.name
        )

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.body, self.name))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, Preference):
            return (str(self.body), str(self.name)) < (
                str(other.body),
                str(other.name),
            )
        return NotImplemented


@cache_hash
@functools.total_ordering
class IsViolated(FunctionExpression):
    """The '(is-violated <pref-name>)' metric expression."""

    def __init__(self, pref_name: str) -> None:
        """Initialize the expression."""
        self._pref_name = pref_name

    @property
    def pref_name(self) -> str:
        """Get the preference name."""
        return self._pref_name

    def instantiate(self, mapping: Mapping[Variable, Term]) -> "IsViolated":
        """Instantiate the expression (no variables, returns self)."""
        return self

    def __str__(self) -> str:
        """Get the string representation."""
        return f"({Symbols.IS_VIOLATED.value} {self.pref_name})"

    def __repr__(self) -> str:
        """Get the unambiguous string representation."""
        return f"{type(self).__name__}({self.pref_name})"

    def __eq__(self, other) -> bool:
        """Compare with another object."""
        return isinstance(other, IsViolated) and self.pref_name == other.pref_name

    def __hash__(self) -> int:
        """Compute the hash of the object."""
        return hash((type(self), self.pref_name))

    def __lt__(self, other):
        """Compare with another object."""
        if isinstance(other, IsViolated):
            return self.pref_name < other.pref_name
        return NotImplemented
