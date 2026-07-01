"""
Tests for src/topology.py
"""

import numpy as np
import cv2
from src.topology import get_largest_contour, get_convex_hull, get_convexity_defects, analyze_topology


def make_square_thresh_image():
    """A clean binary image with one white square — no defects expected."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[30:70, 30:70] = 255
    return img


def make_notched_thresh_image():
    """A square with a notch cut into one side — simulates a broken tooth."""
    img = np.zeros((100, 100), dtype=np.uint8)
    img[30:70, 30:70] = 255
    img[45:55, 60:70] = 0  # carve a notch out of the right edge
    return img


def test_get_largest_contour_finds_shape():
    thresh = make_square_thresh_image()
    contour = get_largest_contour(thresh)
    assert contour is not None
    assert cv2.contourArea(contour) > 0


def test_get_largest_contour_returns_none_for_blank_image():
    blank = np.zeros((100, 100), dtype=np.uint8)
    contour = get_largest_contour(blank)
    assert contour is None


def test_convex_hull_and_defects_on_notched_shape():
    thresh = make_notched_thresh_image()
    contour, hull, defects = analyze_topology(thresh)
    assert contour is not None
    assert hull is not None
    # A notch should produce at least one convexity defect
    assert defects is not None
    assert defects.shape[0] >= 1
