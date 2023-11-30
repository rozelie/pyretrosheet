"""Exceptions for models and their parsing."""


class ParseError(Exception):
    """Raise on Retrosheet data parsing errors."""

    def __init__(
        self, looking_for_value: str, raw_value: str, game_line: str | None = None, file_path: str | None = None
    ):
        self.looking_for_value = looking_for_value
        self.raw_value = raw_value
        self.game_line = game_line
        self.file_path = file_path
        message = f"Unable to parse '{looking_for_value}' from '{raw_value}'"
        if game_line:
            message = f"{message} in line '{game_line}'"
        if file_path:
            message = f"{message} from '{file_path}'"

        super().__init__(message)
