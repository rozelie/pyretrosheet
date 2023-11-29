"""Exceptions for models and their parsing."""


class ParseError(Exception):
    """Raise on Retrosheet data parsing errors."""

    def __init__(self, looking_for_value: str, raw_value: str):
        super().__init__(f"Unable to parse '{looking_for_value}' from '{raw_value}'")
