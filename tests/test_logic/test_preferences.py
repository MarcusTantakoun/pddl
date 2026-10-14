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

"""Test pddl.logic.preferences module."""

from pddl.logic import Predicate, constants, variables
from pddl.logic.preferences import IsViolated, Preference


def test_preferences_str_named() -> None:
    """Test the string of a named preference."""
    assert str(Preference(Predicate("p"), name="pref1")) == "(preference pref1 (p))"


def test_preference_str_anaonymous() -> None:
    """Test the string of an anonymous preference."""
    assert str(Preference(Predicate("p"))) == "(preference (p))"


def test_preference_equality_and_hash() -> None:
    """Test equality and hashing of preferences."""
    p = Predicate("p")
    assert Preference(p, name="a") == Preference(p, name="a")
    assert hash(Preference(p, name="a")) == hash(Preference(p, name="a"))
    assert Preference(p, name="a") != Preference(p, name="b")
    assert Preference(p) != Preference(p, name="a")


def test_preference_instantiate() -> None:
    """Test instantiation of a preference."""
    x = variables("x")[0]
    o = constants("o")[0]
    pref = Preference(Predicate("P", x), name="pref1")
    assert pref.instantiate({x: o}) == Preference(Predicate("p", o), name="pref1")


def test_preference_ordering() -> None:
    """Test ordering of preferences."""
    assert Preference(Predicate("p"), name="a") < Preference(Predicate("p"), name="b")


def test_is_violated_str() -> None:
    """Test the string of an is-violated expression."""
    assert str(IsViolated("pref1")) == "(is-violated pref1)"


def test_preference_repr_and_ordering_not_implemented() -> None:
    """Test the repr of a preference and the NotImplemented branch of __lt__."""
    assert (
        repr(Preference(Predicate("p"), name="pref1")) == "Preference((p), name=pref1)"
    )
    assert Preference(Predicate("p"), name="a").__lt__("x") is NotImplemented


def test_is_violated_dunders() -> None:
    """Test instantiate, repr, hash and ordering of IsViolated."""
    v = IsViolated("pref1")
    assert v.instantiate({}) is v
    assert repr(v) == "IsViolated(pref1)"
    assert hash(v) == hash(IsViolated("pref1"))
    assert v < IsViolated("pref2")
    assert v.__lt__("x") is NotImplemented
