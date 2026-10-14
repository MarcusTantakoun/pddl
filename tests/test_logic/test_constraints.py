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

"""Test pddl.logic.constraints module."""

from pddl.logic import Predicate, constants, variables
from pddl.logic.constraints import (
    Always,
    AlwaysWithin,
    AtMostOnce,
    HoldAfter,
    HoldDuring,
    Sometime,
    SometimeAfter,
    SometimeBefore,
    Within,
)


def test_unary_constraints_str() -> None:
    """Test the string of unary constraints."""
    p = Predicate("p")
    assert str(Always(p)) == "(always (p))"
    assert str(Sometime(p)) == "(sometime (p))"
    assert str(AtMostOnce(p)) == "(at-most-once (p))"


def test_time_body_constraints_str() -> None:
    """Test the string of time+body constraints."""
    p = Predicate("p")
    assert str(Within(5, p)) == "(within 5 (p))"
    assert str(HoldAfter(3, p)) == "(hold-after 3 (p))"


def test_binary_constraints_str() -> None:
    """Test the string of two-body constraints."""
    p, q = Predicate("p"), Predicate("q")
    assert str(SometimeAfter(p, q)) == "(sometime-after (p) (q))"
    assert str(SometimeBefore(p, q)) == "(sometime-before (p) (q))"


def test_always_within_str() -> None:
    """Test the string of an always-within constraint."""
    p, q = Predicate("p"), Predicate("q")
    assert str(AlwaysWithin(4, p, q)) == "(always-within 4 (p) (q))"


def test_hold_during_str() -> None:
    """Test the string of a hold-during constraint."""
    assert str(HoldDuring(1, 3, Predicate("p"))) == "(hold-during 1 3 (p))"


def test_constraint_equality_and_hash() -> None:
    """Test equality and hashing of constraints."""
    p = Predicate("p")
    assert Always(p) == Always(p)
    assert hash(Always(p)) == hash(Always(p))
    assert Always(p) != Sometime(p)
    assert Within(5, p) != Within(6, p)
    assert SometimeAfter(p, Sometime(p)) != SometimeAfter(Sometime(p), p)


def test_constraint_instantiate() -> None:
    """Test instantiation propogates through each constraint kind."""
    x = variables("x")[0]
    o = constants("o")[0]
    assert Always(Predicate("p", x)).instantiate({x: o}) == Always(Predicate("p", o))
    assert SometimeAfter(Predicate("p", x), Predicate("q", x)).instantiate(
        {x: o}
    ) == SometimeAfter(Predicate("p", o), Predicate("q", o))
    assert HoldDuring(1, 3, Predicate("p", x)).instantiate({x: o}) == HoldDuring(
        1, 3, Predicate("p", o)
    )
    assert AlwaysWithin(4, Predicate("p", x), Predicate("q", x)).instantiate(
        {x: o}
    ) == AlwaysWithin(4, Predicate("p", o), Predicate("q", o))


def test_reused_base_accessors() -> None:
    """Test that reused UnaryOp/BinaryOp accessors are exposed."""
    p, q = Predicate("p"), Predicate("q")
    assert Always(p).argument == p
    assert SometimeAfter(p, q).operands == (p, q)


def test_time_body_constraint_instantiate() -> None:
    """Test instantiation for within and hold-after."""
    x = variables("x")[0]
    o = constants("o")[0]
    assert Within(5, Predicate("p", x)).instantiate({x: o}) == Within(
        5, Predicate("p", o)
    )
    assert HoldAfter(3, Predicate("p", x)).instantiate({x: o}) == HoldAfter(
        3, Predicate("p", o)
    )


def test_standalone_constraint_repr() -> None:
    """Test the repr of the standalone constraint classes."""
    p, q = Predicate("p"), Predicate("q")
    assert repr(Within(5, p)) == "Within(5, (p))"
    assert repr(HoldAfter(3, p)) == "HoldAfter(3, (p))"
    assert repr(AlwaysWithin(4, p, q)) == "AlwaysWithin(4, (p), (q))"
    assert repr(HoldDuring(1, 3, p)) == "HoldDuring(1, 3, (p))"


def test_standalone_constraint_ordering() -> None:
    """Test ordering of the standalone constraint classes."""
    p = Predicate("p")
    assert Within(1, p) < Within(2, p)
    assert HoldAfter(1, p) < HoldAfter(2, p)
    assert AlwaysWithin(1, p, p) < AlwaysWithin(2, p, p)
    assert HoldDuring(0, 1, p) < HoldDuring(0, 2, p)
    assert Within(1, p).__lt__("x") is NotImplemented
    assert HoldAfter(1, p).__lt__("x") is NotImplemented
    assert AlwaysWithin(1, p, p).__lt__("x") is NotImplemented
    assert HoldDuring(0, 1, p).__lt__("x") is NotImplemented
