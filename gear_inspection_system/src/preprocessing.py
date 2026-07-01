"""
Phase 1: Signal isolation.
Convert raw photons into a clean, binarized silhouette.
"""

import cv2
from config import settings


def to_grayscale(img):
    """
    Convert a BGR color image to a single-channel grayscale image.
    """
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def apply_blur(gray_img):
    """
    Apply Gaussian blur to reduce high-frequency sensor noise.
    """
    return cv2.GaussianBlur(
        gray_img,
        settings.GAUSSIAN_KERNEL,
        settings.GAUSSIAN_SIGMA
    )


def binarize(blurred_img):
    """
    Threshold the blurred image into a pure black/white silhouette.
    """
    _, thresh = cv2.threshold(
        blurred_img,
        settings.BINARY_THRESH,
        settings.BINARY_MAX_VAL,
        cv2.THRESH_BINARY
    )
    return thresh


def preprocess(img):
    """
    Run the full Phase 1 pipeline: grayscale -> blur -> binarize.
    Returns the final thresholded (binary) image.
    """
    gray = to_grayscale(img)
    blurred = apply_blur(gray)
    thresh = binarize(blurred)
    return thresh
