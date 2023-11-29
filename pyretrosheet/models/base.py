"""Represents a Retrosheet base encoding."""
from enum import Enum


class Base(Enum):
    """Retrosheet base encodings."""

    BATTER_AT_HOME = "B"
    FIRST_BASE = "1"
    SECOND_BASE = "2"
    THIRD_BASE = "3"
    HOME = "H"
