from .context import *
from pathlib import Path
import cv2
import pytest


NAVBAR_DIR = DATA_PATH / "leaguenavbar"
NAVBAR_TEMPLATE = NAVBAR_DIR / "navbar_template.png"
EXIT_DIR = DATA_PATH / "leagueexit"
EXIT_TEMPLATE = EXIT_DIR / "exit_template.png"
NEITHER_DIR = DATA_PATH / "neither"


def _test_find_template(
    image_path: Path, template_path: Path, expected, confidence=None
):
    image = cv2.imread(str(image_path))
    template = cv2.imread(str(template_path))
    result = (
        findimg.find_template(image, template, confidence)
        if confidence
        else findimg.find_template(image, template, preprocessed=False)
    )
    assert bool(result) == expected


def _test_find_template_each(directory, template_path, expected, confidence=None):
    for path in directory.glob("*.png"):
        print("Testing", path, "against", template_path)
        _test_find_template(path, template_path, expected, confidence=confidence)


def test_find_template_simple():
    # Match templates to themselves
    _test_find_template(NAVBAR_TEMPLATE, NAVBAR_TEMPLATE, True)
    _test_find_template(EXIT_TEMPLATE, EXIT_TEMPLATE, True)
    # Templates shouldn't match each other
    _test_find_template(NAVBAR_TEMPLATE, EXIT_TEMPLATE, False)
    _test_find_template(EXIT_TEMPLATE, NAVBAR_TEMPLATE, False)


@pytest.mark.timeout(30)
def test_find_template_navbar():
    _test_find_template_each(NAVBAR_DIR, NAVBAR_TEMPLATE, True)


@pytest.mark.timeout(15)
def test_find_template_exit():
    _test_find_template_each(EXIT_DIR, EXIT_TEMPLATE, True)


@pytest.mark.timeout(15)
def test_find_template_neither():
    _test_find_template_each(NEITHER_DIR, NAVBAR_TEMPLATE, False)
    _test_find_template_each(NEITHER_DIR, EXIT_TEMPLATE, False)
