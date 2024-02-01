"""Encapsulates Retrosheet play data."""
from dataclasses import dataclass

from pyretrosheet.models.play.description import BatterEvent, RunnerEvent
from pyretrosheet.models.play.event import Event
from pyretrosheet.models.play.modifier import ModifierType
from pyretrosheet.models.team import TeamLocation


@dataclass
class Play:
    """A play as defined in Retrosheet.

    Args:
        inning: the inning the play occurred in
        team_location: the team's location
        batter_id: the player id of the batter
        count: the count on the batter
        pitches: all the pitches to the batter in the plate appearance
        comments: comments regarding the play, from 'com' lines in Retrosheet data
        event: the event describes the play that occurred
        raw: the raw play line
    """

    inning: int
    team_location: TeamLocation
    batter_id: str
    count: str
    pitches: str
    comments: list[str]
    event: Event
    raw: str

    @classmethod
    def from_play_line(cls, play_line: str, comment_lines: list[str] | None) -> "Play":
        """Load a play from a play line.

        Args:
            play_line: line for a play (format: play,inning,home/visitor,player id,count,pitches,event)
                Examples include: 'play,7,0,saboc001,01,CX,8/F78', 'play,1,0,marts002,22,CBCBX,S9/L89S-'
            comment_lines: comment lines that reference the play, if present
        """
        # Handle weird case of 'play,3,1,smitj106,??,,43,2-3' where I think this is an encoding error
        if play_line == "play,3,1,smitj106,??,,43,2-3":
            play_line = "play,3,1,smitj106,??,?,43.2-3"

        _, inning, team_location, batter_id, count, pitches, event = play_line.split(",")
        return cls(
            inning=int(inning),
            team_location=TeamLocation(int(team_location)),
            batter_id=batter_id,
            count=count,
            pitches=pitches,
            comments=[c.split(",")[1] for c in comment_lines or []],
            event=Event.from_play_event(event),
            raw=play_line,
        )

    def is_walk(self) -> bool:
        """Determines if the play resulted in a walk."""
        return self.event.description.batter_event in [
            BatterEvent.WALK,
            BatterEvent.INTENTIONAL_WALK,
        ]

    def is_hit_by_pitch(self) -> bool:
        """Determines if the play resulted in the batter being hit by a pitch."""
        return self.event.description.batter_event == BatterEvent.HIT_BY_PITCH

    def is_sacrifice_fly(self) -> bool:
        """Determines if the play resulted in a sacrifice fly."""
        return any(modifier.type == ModifierType.SACRIFICE_FLY for modifier in self.event.modifiers)

    def is_an_at_bat(self) -> bool:
        """Determines if the play counts as an at bat."""
        is_batter_event_at_bat = self.event.description.batter_event not in [
            BatterEvent.NO_PLAY,
            BatterEvent.CATCHER_INTERFERENCE,
            BatterEvent.ERROR_ON_FOUL_FLY_BALL,
        ]
        is_runner_event_at_bat = self.event.description.runner_event not in [
            RunnerEvent.WILD_PITCH,
            RunnerEvent.CAUGHT_STEALING,
            RunnerEvent.STOLEN_BASE,
            RunnerEvent.OTHER_ADVANCE,
            RunnerEvent.PASSED_BALL,
            RunnerEvent.BALK,
            RunnerEvent.PICKED_OFF,
        ]
        return all(
            [
                is_batter_event_at_bat,
                is_runner_event_at_bat,
                not self.is_walk(),
                not self.is_hit_by_pitch(),
                not self.is_sacrifice_fly(),
            ]
        )

    def is_single(self) -> bool:
        """Determines if the play resulted in a single."""
        return self.event.description.batter_event == BatterEvent.SINGLE

    def is_double(self) -> bool:
        """Determines if the play resulted in a double."""
        return self.event.description.batter_event == BatterEvent.DOUBLE

    def is_triple(self) -> bool:
        """Determines if the play resulted in a triple."""
        return self.event.description.batter_event == BatterEvent.TRIPLE

    def is_home_run(self) -> bool:
        """Determines if the play resulted in a home run."""
        return self.event.description.batter_event in [
            BatterEvent.HOME_RUN_INSIDE_PARK,
            BatterEvent.HOME_RUN_LEAVING_PARK,
        ]

    def is_hit(self) -> bool:
        """Determines if the play resulted in a hit."""
        return any(
            [
                self.is_single(),
                self.is_double(),
                self.is_triple(),
                self.is_home_run(),
            ]
        )

    def batter_gets_on_base(self) -> bool:
        """Determines if the batter on the play gets on base (any base)."""
        return any([self.is_hit(), self.is_walk(), self.is_hit_by_pitch()])
