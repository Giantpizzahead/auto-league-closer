"""
League Closer TM

Mock module that can detect and close the League of Legends client automatically.
Copyright (c) 2023, Giantpizzahead
"""

from .league import is_league_running, close_league, open_league

__all__ = ["is_league_running", "close_league", "open_league"]
