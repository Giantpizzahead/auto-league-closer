"""
Handles the detecting and closing of the League client.

Copyright (c) 2023, Giantpizzahead
"""

from . import computer
from . import sikuli
import os


def is_league_running():
    """Returns whether the League client is running."""
    return computer.is_process_running("LeagueClientUx.exe")


def close_league():
    """Closes the League client. Assumes that League is running.
    
    Returns:
        bool: Whether the League client was closed.
    """
    # Try to focus the League window
    try:
        computer.focus_window("League of Legends")
    except Exception as e:
        print("Unable to focus the League window... just wait until it opens :)")
        print(e)
        return False
    # Run the SikuliX script
    script_path = os.path.join(os.path.dirname(__file__), "data", "close_league.sikuli")
    exit_code = sikuli.run_sikuli_script(script_path)
    if exit_code != 0:
        print("SikuliX script failed to run... good luck queuing though :)")
        return False
    return True


def open_league():
    """Opens League (for testing purposes)."""
    computer.open_app("League of Legends")
