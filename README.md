# pyretrosheet

[![PyPI version](https://badge.fury.io/py/pyretrosheet.svg)](https://badge.fury.io/py/pyretrosheet) ![Coverage](assets/coverage.svg)

> `pyretrosheet` is under active development and is not feature complete.

Load, analyze, and enrich [retrosheet.org](https://www.retrosheet.org) MLB data using Python representations.

Retrosheet provides play-by-play and other miscellaneous MLB data (at the time of writing, includes all play-by-play 
data for all AL and NL seasons from 1919 to 2022).

`pyretrosheet` provides functionality for:
- downloading Retrosheet play-by-play data
- parsing and loading play-by-play data into Python objects to make the data easier to understand and analyze
- enriching data to include player and summary statistics not encoded directly by Retrosheet

`pyretrosheet` does **not** provide functionality for:
- downloading/using MLB data from sources other than Retrosheet

See [Retrosheet Data Resources](https://www.retrosheet.org/resources/resources1.html) for other tools that parse
Retrosheet event files. At the time of writing, these resources focus on loading/dumping to other data formats like
CSV and SQL databases.

# Usage
```
pip install pyretrosheet
```

## Load Games
By default, data downloaded from [retrosheet.org](https://www.retrosheet.org) is stored at `~/.pyretrosheet/data/`, 
but can be overriden via the `data_dir` argument.

```python
import pyretrosheet

games = pyretrosheet.load_games(year=2022)

print(games[0])
"""
Game(
  id=GameID(home_team_id='SFN', date=datetime.date(2022, 4, 8), game_number=0, raw='id,SFN202204080'),
  home_team_id=SFN,
  visiting_team_id=MIA,
  num_chronological_events=150,
  earned_runs={'bleir001': 1, 'alcas001': 2, 'bassa001': 1, 'benda001': 1, 'webbl001': 1, 'dovac001': 3, 'leond003': 1},
)
"""
```

**TODO**: Add more examples

# Data Availability
## Retrosheet Event File Coverage
[Retrosheet's Event File Spec](https://www.retrosheet.org/eventfile.htm) defines the encoding for event files 
(play-by-play game data). The spec (as of 11/30/2023) can also be found at [docs/event_file_spec.txt](docs/event_file_spec.txt).

There is a wide amount of data encoded into these files and this package does not cover all encodings.

Contributions are welcome for any encodings not covered!

### Covered
- Loading all games from a given event file
- Record types
  - `id`
  - `info`
  - `start`
  - `sub`
  - `play`
  - `data`
  - `com`

### Not Covered
- Record types
  - `play`'s pitching encoding
  - `radj`
  - `badj`
  - `padj`
  - `ladj`
  - `presadj`

- Miscellaneous data
  - replays
  - ejections
  - umpire changes
  - protests
  - suspensions

## Enriched
`pyretrosheet` provides enriched Retrosheet data to provide:
- **TODO**

# Contributing
## `Makefile` targets
```
help: Show this help.
setup: Install the package and dev dependencies into a virtualenv.
test:  Run pytest on the tests dir.
test_all_data:  Run pytest on all Retrosheet data.
format: Run black and isort on package and tests dirs.
lint:  Run ruff and mypy on package files.
coverage:  Run test coverage and update coverage badge
bump_version:  Increment patch version references in the project
publish_to_testpypi:  Publish the package to test.pypi.org.
publish_to_pypi:  Publish the package to pypi.org.
```
## Todo

### Non-Trivial
- ReadTheDocs
- Verify enriched data with alternative sources like Baseball Reference
- Determine top-level interface for querying data
- Implement index of game files to easily lookup games for:
  - a specific team within a year
  - a specific game
- Stats
  - Hits (H)
  - Walks (W)
  - Hit By Pitches (HBP)
  - Sacrifice Flys (SF)
  - At Bats (AB)
  - Singles (S)
  - Doubles (D)
  - Triples (T)
  - Home Runs (HR)
  - Composite
    - Batting Average (BA)
    - Slugging Percentage (SP)
    - On Base Percentage (OBP)
  - Difficult and Needs Lots of Validation
    - Runs (R)
    - Runs Batted In (RBI)
- Aggregate stats
  - Mean, Median, Std. Dev, Min, Max

### Trivial
- Parse out 'info' fields into `pyretrosheet.models.Game` properties
- Encoding pitches from `play` data
- Improve error handling for inability to retrieve Retrosheet data
- Improve README Usage examples
- Add CONTRIBUTING.md
- Add interface to load stats

# Retrosheet Notice
The information used here was obtained free of charge from and is copyrighted by Retrosheet. Interested
parties may contact Retrosheet at 20 Sunset Rd., Newark, DE 19711.

# Credits
- Project skeleton generated via `cookiecutter https://github.com/rozelie/Python-Project-Cookiecutter`
- Thank you Retrosheet team for making your data free and publicly available!
