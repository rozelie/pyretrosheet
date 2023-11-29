"""Team data and identifiers."""
from enum import Enum


class TeamLocation(Enum):
    """Retrosheet encoding of a team's location."""

    VISITING = 0
    HOME = 1
