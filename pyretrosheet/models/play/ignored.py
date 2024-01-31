"""Handle ignored Retrosheet data."""


def trim_ignored_characters(play_or_modifier: str) -> str:
    """Trim ignored characters from play data.

    Args:
        play_or_modifier: a raw Retrosheet play or modifier

    From Retrosheet event file description:
        A play record ending in a number sign, #, indicates that there is some uncertainty in the play.
        Occasionally, a com record may follow providing additional information.
        A play record may also contain exclamation points, "!" indicating an exceptional play and
        question marks "?" indicating some uncertainty in the play,
        "+" indicating a hard hit ball, and "-" for softly hit balls.
        These characters can be safely ignored.
    """
    if play_or_modifier.endswith(("#", "!", "?", "+", "-")):
        return play_or_modifier[:-1]

    return play_or_modifier
