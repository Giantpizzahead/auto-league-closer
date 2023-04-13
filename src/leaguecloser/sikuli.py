"""
Runs SikuliX scripts from Python.
"""

import os
import requests
import subprocess
import sys

# Get SikuliX jar path depending on if we're frozen or not (PyInstaller)
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    SIKULI_JAR = os.path.join(os.getenv("PROGRAMDATA"), "Auto League Closer", "sikulixide-2.0.5.jar")
else:
    SIKULI_JAR = os.path.join(os.path.dirname(__file__), "lib", "sikulixide-2.0.5.jar")

# Install SikuliX if needed
if not os.path.isfile(SIKULI_JAR):
    print("(First time setup, downloading SikuliX... you better not queue...)")
    # Create directories if missing
    os.makedirs(os.path.dirname(SIKULI_JAR), exist_ok=True)
    # Download SikuliX
    url = "https://launchpad.net/sikuli/sikulix/2.0.5/+download/sikulixide-2.0.5.jar"
    with open(SIKULI_JAR, "wb") as f:
        f.write(requests.get(url).content)


def run_sikuli_script(script_path):
    """Runs a SikuliX script from Python.

    Args:
        script_path (str): The path to the script to run.

    Returns:
        int: The exit code of the SikuliX script.
    """
    # Run Sikuli
    return subprocess.call(
        ["java", "-jar", SIKULI_JAR, "-r", script_path],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
