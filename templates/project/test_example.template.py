"""Example tests for a project. Copy to tests/ and adapt.

Cover, at minimum, happy-path, invalid-input, and boundary behaviour.
"""

from __future__ import annotations

import pytest


def add(a: int, b: int) -> int:
    """Placeholder function under test — replace with your project's code."""
    return a + b


def test_happy_path() -> None:
    assert add(2, 3) == 5


def test_boundary_behaviour() -> None:
    assert add(0, 0) == 0


@pytest.mark.parametrize("value", ["1", None, 1.5])
def test_invalid_input_is_rejected(value: object) -> None:
    with pytest.raises(TypeError):
        add(value, 1)  # type: ignore[arg-type]  # deliberately wrong type
