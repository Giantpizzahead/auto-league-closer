"""
Locates template images in another image (ex: a screenshot).

Based on https://pyimagesearch.com/2015/01/26/multi-scale-template-matching-using-python-opencv.
"""

from typing import Any, Callable, Optional, Tuple
import numpy as np
import imutils
import cv2
from .context import *


MAX_PROCESS_SIZE = 512
DEFAULT_CONFIDENCE = 0.55
LOG = create_logger(name=__name__, level=logging.WARN)


class Rectangle:
    """Represents a rectangle with the given top-left corner and size."""

    x: int
    y: int
    w: int
    h: int

    def __init__(self, x: int, y: int, w: int, h: int):
        """Creates a rectangle with the given top-left corner and size."""
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def __str__(self) -> str:
        return f"Rectangle({self.x}, {self.y}, {self.w}, {self.h})"

    def __repr__(self) -> str:
        return self.__str__()


class Match(Rectangle):
    """Represents a match with the given top-left corner, size, and confidence."""

    confidence: float

    def __init__(self, x: int, y: int, w: int, h: int, confidence: float):
        """Creates a match with the given top-left corner, size, and confidence."""
        super().__init__(x, y, w, h)
        self.confidence = confidence

    def scale(self, scale: float) -> "Match":
        """Returns a new match scaled by the given amount."""
        return Match(
            int(self.x * scale),
            int(self.y * scale),
            int(self.w * scale),
            int(self.h * scale),
            self.confidence,
        )

    def __str__(self) -> str:
        return f"Match({self.x}, {self.y}, {self.w}, {self.h}, {self.confidence})"

    def __repr__(self) -> str:
        return self.__str__()


def _preprocess_images(image: cv2.Mat, template: cv2.Mat) -> Tuple[cv2.Mat, cv2.Mat]:
    """Preprocesses the images to be used in the template matching algorithm.

    Args:
        image: The image to search in.
        template: The template to search for.

    Returns:
        A tuple of the preprocessed images.
    """
    # Convert to grayscale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # Blur
    # image = cv2.GaussianBlur(image, (3, 3), 0)
    # template = cv2.GaussianBlur(template, (3, 3), 0)

    # Edge detection
    # image = cv2.Canny(image, 50, 200)
    # template = cv2.Canny(template, 50, 200)

    # Downscale max dimension while keeping aspect ratios (to speed up processing)
    max_dim = max(image.shape[0], image.shape[1], template.shape[0], template.shape[1])
    old_image_shape = image.shape
    if max_dim > MAX_PROCESS_SIZE:
        scale = MAX_PROCESS_SIZE / max_dim
        image = imutils.resize(image, width=int(image.shape[1] * scale))
        template = imutils.resize(template, width=int(template.shape[1] * scale))

    actual_ratio = image.shape[1] / float(old_image_shape[1])
    LOG.debug(f"Preprocessed images with scaling factor {actual_ratio:.2f}")
    # cv2.imwrite(str(TEMP_DIR / "image.png"), image)
    # cv2.imwrite(str(TEMP_DIR / "template.png"), template)
    return image, template


def do_preprocess(
    func: Callable[..., Optional[Match]]
) -> Callable[..., Optional[Match]]:
    """Decorator to preprocess images before calling a function that returns a Match."""

    def wrapper(
        image: cv2.Mat, template: cv2.Mat, preprocessed: bool = False, *args, **kwargs
    ):
        to_scale = 1
        if not preprocessed:
            raw_image = image
            image, template = _preprocess_images(image, template)
            to_scale = raw_image.shape[1] / image.shape[1]
        match = func(image, template, preprocessed=preprocessed, *args, **kwargs)
        if match is not None:
            match = match.scale(to_scale)
        return match

    return wrapper


# @do_preprocess
# def find_template(
#     image: cv2.Mat, template: cv2.Mat, confidence: float = 0.5, preprocessed: bool = False
# ) -> Optional[Match]:
#     """Returns the (most likely) location of the template with size scaling, or None if not found.

#     Args:
#         image: The image to search in.
#         template: The template to search for.
#         confidence: The minimum confidence to consider a match.
#         preprocessed: Whether the images have already been preprocessed.

#     Returns:
#         A Match object, or None if not found.
#     """
#     # Credit to https://stackoverflow.com/a/51607041 for the below algorithm
#     # Initiate ORB detector
#     orb = cv2.ORB_create()
#     # Find the keypoints and descriptors with ORB
#     kp1, des1 = orb.detectAndCompute(template, None)
#     kp2, des2 = orb.detectAndCompute(image, None)
#     # Create BFMatcher object
#     bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
#     # Match descriptors
#     matches = bf.match(des1, des2)
#     # Sort them in order of increasing distance
#     matches = sorted(matches, key = lambda x: x.distance)
#     # Only use the best 10 matches to find the bounding box
#     good_matches = list(filter(lambda m: m.distance < 50, matches[:10]))
#     # Show info about matches
#     for match in matches:
#         print(match.distance)
#     print(len(kp1), len(kp2), len(matches), len(good_matches))

#     match = None
#     if len(good_matches) >= 4:
#         # Generate the transformation matrix
#         src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
#         dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
#         M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
#         matchesMask = mask.ravel().tolist()
#         h, w = template.shape[:2]
#         pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)

#         # Get bounding rectangle
#         dst = cv2.perspectiveTransform(pts,M)
#         rect = cv2.boundingRect(dst)
#         match = Match(rect[0], rect[1], rect[2], rect[3], 1)
#     return match


@do_preprocess
def find_template_exact_size(
    image: cv2.Mat,
    template: cv2.Mat,
    confidence: float = DEFAULT_CONFIDENCE,
    preprocessed: bool = False,
) -> Optional[Match]:
    """Returns the likely location of the template with the same size in the image, else None.

    Args:
        image: The image to search in.
        template: The template to search for.
        confidence: The minimum confidence to consider a match.
        preprocessed: Whether the images have already been preprocessed.

    Returns:
        A Match object, or None if not found.
    """
    # Only try matching if the template is smaller than the image
    match = None
    if image.shape[0] >= template.shape[0] and image.shape[1] >= template.shape[1]:
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        # If confidence is met, set match
        if maxVal >= confidence:
            match = Match(
                maxLoc[0], maxLoc[1], template.shape[1], template.shape[0], maxVal
            )

    if match:
        LOG.debug(f"Found exact match: {match}")
    else:
        LOG.debug("No exact match found")
    return match


@do_preprocess
def find_template(
    image: cv2.Mat,
    template: cv2.Mat,
    confidence: float = DEFAULT_CONFIDENCE,
    preprocessed: bool = False,
) -> Optional[Match]:
    """Returns the (most likely) location of the template with size scaling, or None if not found.

    Args:
        image: The image to search in.
        template: The template to search for.
        confidence: The minimum confidence to consider a match.
        preprocessed: Whether the images have already been preprocessed.

    Returns:
        A Match object, or None if not found.
    """

    def choose_match(best_match, new_match, new_ratio):
        if new_match and (
            best_match is None or new_match.confidence > best_match.confidence
        ):
            return new_match.scale(new_ratio)
        else:
            return best_match

    # Try scaling the image and template to multiple sizes
    # Assumes that the template only needs to be resized by a factor in the range [0.5, 2]
    best_match = None
    image_sizes = {
        s: imutils.resize(image, width=int(image.shape[1] * s))
        for s in np.linspace(0.5, 1.0, 10)[::-1]
    }
    template_sizes = {
        s: imutils.resize(template, width=int(template.shape[1] * s))
        for s in np.linspace(0.5, 1.0, 10)[::-1]
    }
    tried_sizes = set()
    for image_scale, resized_image in image_sizes.items():
        for template_scale, resized_template in template_sizes.items():
            actual_ratio = template_scale / image_scale
            # Don't repeat checks
            integer_ratio = round(actual_ratio * 1000)
            if integer_ratio in tried_sizes:
                continue
            tried_sizes.add(integer_ratio)

            LOG.debug(f"Trying effective template scale {actual_ratio:.2f}")
            match = find_template_exact_size(
                resized_image, resized_template, confidence=0, preprocessed=True
            )
            best_match = choose_match(best_match, match, 1 / image_scale)
    if not best_match or best_match.confidence < confidence:
        LOG.info(f"No match found, best match: {best_match}")
        return None
    LOG.info(f"Found match: {best_match}")
    return best_match
