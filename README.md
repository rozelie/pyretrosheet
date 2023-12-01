# pyretrosheet

> `pyretrosheet` is under active development and a formal release has not yet been made (but hopefully will be soon!).`

Load, analyze, and enrich [retrosheet.org](https://www.retrosheet.org) MLB data.

Retrosheet provides play-by-play and other miscellaneous MLB data (at the time of writing, includes all play-by-play 
data for all AL and NL seasons from 1919 to 2022).

`pyretrosheet` provides functionality for:
- downloading Retrosheet play-by-play data
- parsing and loading play-by-play data into Python objects to make the data easier to understand and analyze
- enriching data to include player and summary statistics not encoded directly by Retrosheet

`pyretrosheet` does **not** provide functionality for:
- downloading/using MLB data from sources other than Retrosheet

# Usage
**TODO**

# Data Availability
## Retrosheet Event File Coverage
[Retrosheet's Event File Spec](https://www.retrosheet.org/eventfile.htm) defines the encoding for event files 
(play-by-play game data).

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
Retrosheet does not provide player-level nor aggregate statistics.

`pyretrosheet` provides an interface to enrich the data to include:
- **TODO**

# Contributing
## `Makefile` targets
```
help: Show this help.
setup: Install the package and dev dependencies into a virtualenv.
run:  Run the package.
test:  Run pytest on the tests dir.
test_all_data: Run pytest on all Retrosheet data.
format: Run black and isort on package and tests dirs.
lint:  Run ruff and mypy on package files.
docker_build: Build a Docker image for the package.
docker_run:  Run the Docker image for the package.
publish_to_testpypi:  Publish the package to test.pypi.org.
publish_to_pypi:  Publish the package to pypi.org.
```

## Todo
- Parse out 'info' fields into `pyretrosheet.models.Game` properties
- Implement versions for a release
- Encoding pitches from `play` data
- Implement index of game files to easily lookup games for:
    - a specific team within a year
    - a specific game
- Determine top-level interface for querying data
- Verify enriched data with alternative sources like Baseball Reference

# Credits
- Project skeleton generated via `cookiecutter https://github.com/rozelie/Python-Project-Cookiecutter`

## Retrosheet Notice
The information used here was obtained free of charge from and is copyrighted by Retrosheet. Interested
parties may contact Retrosheet at 20 Sunset Rd., Newark, DE 19711.