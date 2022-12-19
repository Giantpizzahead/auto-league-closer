from .context import *
from pathlib import Path
import cv2
import pytest


NAVBAR_DIR = DATA_PATH / "leaguenavbar"
NAVBAR_TEMPLATE = NAVBAR_DIR / "navbar_template.png"
EXIT_DIR = DATA_PATH / "leagueexit"
EXIT_TEMPLATE = EXIT_DIR / "exit_template.png"
NEITHER_DIR = DATA_PATH / "neither"

SMILEY_DIR = DATA_PATH / "smiley"
NO_SMILEY_DIR = DATA_PATH / "nosmiley"
SMILEY_TEMPLATES = DATA_PATH / "smileytemplates"
SPEED_DIR = DATA_PATH / "speed"
SPEED_TEMPLATE = SPEED_DIR / "speed_template.png"


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


def _test_find_template_pairs(image_dir, template_dir, expected, confidence=None):
    for path1 in image_dir.glob("*.png"):
        for path2 in template_dir.glob("*.png"):
            print("Testing", path1, "against", path2)
            _test_find_template(path1, path2, expected, confidence=confidence)


def _test_find_template_each(directory, template_path, expected, confidence=None):
    for path in directory.glob("*.png"):
        print("Testing", path, "against", template_path)
        _test_find_template(path, template_path, expected, confidence=confidence)


@pytest.mark.timeout(60)
def test_find_template_smileys():
    _test_find_template_pairs(SMILEY_DIR, SMILEY_TEMPLATES, True)


@pytest.mark.timeout(60)
def test_find_template_no_smileys():
    _test_find_template_pairs(NO_SMILEY_DIR, SMILEY_TEMPLATES, False)


@pytest.mark.timeout(60)
def test_find_template_cross_contamination_1():
    _test_find_template_each(SMILEY_DIR, NAVBAR_TEMPLATE, False)
    _test_find_template_each(NO_SMILEY_DIR, NAVBAR_TEMPLATE, False)
    _test_find_template_each(SMILEY_DIR, EXIT_TEMPLATE, False)
    _test_find_template_each(NO_SMILEY_DIR, EXIT_TEMPLATE, False)


@pytest.mark.timeout(60)
def test_find_template_cross_contamination_2():
    _test_find_template_pairs(NAVBAR_DIR, SMILEY_TEMPLATES, False)
    _test_find_template_pairs(EXIT_DIR, SMILEY_TEMPLATES, False)


# 5 calls to find_template with a time limit of 2 seconds
@pytest.mark.timeout(2)
def test_speed():
    _test_find_template_each(SPEED_DIR, SPEED_TEMPLATE, True)
