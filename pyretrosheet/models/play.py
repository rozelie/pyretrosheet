"""Encapsulates Retrosheet play data."""
from dataclasses import dataclass
from typing import Literal

from pyretrosheet.models.player import Player

Adjustment = Literal["L", "R"]


@dataclass
class Play:
    """A play as defined in Retrosheet.

    Args:
        inning: the inning the play occurred in
        batter: the batter player
        pitcher: the pitcher player
        count: the count on the batter
        pitches: all the pitches to the batter in the plate appearance
        comments: comments regarding the play, from 'com' lines in Retrosheet data
        batter_adjustment: batter batting from a side not expected
        pitcher_adjustment: pitcher trowing from a side not expected
        raw: the raw Retrosheet play line
    """

    inning: int
    batter: Player
    pitcher: Player
    count: str
    pitches: str
    comments: list[str]
    batter_adjustment: Adjustment | None
    pitcher_adjustment: Adjustment | None
    raw: str

    @classmethod
    def from_retrosheet_play_lines(
        cls,
        play_line: str,
        comment_lines: list[str] | None,
        batter_adjustment: str | None,
        pitcher_adjustment: str | None,
    ) -> "Play":
        """Load a play from Retrosheet play line.

        Args:
            play_line: line from a Retrosheet play
            comment_lines: comment lines reference the play, if present
            batter_adjustment: batter batting from a side not expected, if it occurs
            pitcher_adjustment: pitcher trowing from a side not expected, if it occurs
        """
        raise NotImplementedError()
