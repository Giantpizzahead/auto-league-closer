# Auto League Closer

Tired of procrastinating on homework all day while still being hardstuck Bronze? Suffering from a bad case of League withdrawal?

Well, I've got a solution for you! Install the **Auto League Closer**!

This handy program will **automatically close the League of Legends client whenever it's running**, so you can get back to binging YouTube videos - uh, I mean doing homework :)

*This is a mock application to demonstrate a clean project structure, along with steps to distribute Python modules and end user application installers.*

## Installation

Windows: Run the [installer](https://github.com/Giantpizzahead/auto-league-closer/releases/download/v1.0.4/LeagueCloserSetup.exe).

## How It Works

1. Repeatedly checks if League is open using [psutil](https://pypi.org/project/psutil/).
2. Closes League in a \~fancy\~ way using [SikuliX](http://sikulix.com/).

## Using the Python Module

```bash
$ pip install leaguecloser
```

Example usage (also what the installable app does):

```python
import leaguecloser
import time

print("Searching for League...")
while True:
    if leaguecloser.is_league_running():
        print("\nNO LEAGUE ALLOWED!")
        if leaguecloser.close_league():
            print("\nThat's right... now get back to work!")
    time.sleep(3)
```

## Packaging and Building Methods

The Makefile contains good practice methods for the common tasks below:

```bash
$ make run  # Runs the file
$ make test  # Runs all tests
$ make package_create  # Creates (or updates) the leaguecloser package
$ make package_upload  # Uploads the leaguecloser package to PyPi
$ make build_app  # Builds the app into a standalone folder with an executable
```

## Development Setup

First, setup a [virtual environment](https://kylefu.me/cheat_python/envanddeps.html). Then run:

```powershell
> & '.\misc\Dev Setup.ps1'
```
