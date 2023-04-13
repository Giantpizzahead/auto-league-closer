"""
Runs SikuliX scripts from Python.
"""

import os
import subprocess


def run_sikuli_script(script_path):
    """Runs a SikuliX script from Python.

    Args:
        script_path (str): The path to the script to run.

    Returns:
        int: The exit code of the SikuliX script.
    """
    sikuli_jar = os.path.join(os.path.dirname(__file__), "lib", "sikulixide-2.0.5.jar")
    return subprocess.call(
        ["java", "-jar", sikuli_jar, "-r", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
