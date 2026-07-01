"""
Tests for src/inspection.py
"""

import numpy as np
from src.topology import analyze_topology
from src.inspection import evaluate_defects, verify_across_frames


def make_square_thresh_image():
    img = np.zeros((100, 100), dtype=np.uint8)
    img[30:70, 30:70] = 255
    return img


def make_notched_thresh_image(notch_depth=10):
    img = np.zeros((100, 100), dtype=np.uint8)
    img[30:70, 30:70] = 255
    img[45:55, 70 - notch_depth:70] = 0
    return img


def test_clean_square_passes():
    thresh = make_square_thresh_image()
    contour, hull, defects = analyze_topology(thresh)
    status, flagged = evaluate_defects(contour, defects, threshold_max=15)
    assert status == "PASS"
    assert flagged == []


def test_deep_notch_fails():
    thresh = make_notched_thresh_image(notch_depth=20)
    contour, hull, defects = analyze_topology(thresh)
    status, flagged = evaluate_defects(contour, defects, threshold_max=5)
    assert status == "FAIL"
    assert len(flagged) >= 1
    assert "distance" in flagged[0]


def test_shallow_notch_within_tolerance_passes():
    thresh = make_notched_thresh_image(notch_depth=3)
    contour, hull, defects = analyze_topology(thresh)
    status, flagged = evaluate_defects(contour, defects, threshold_max=15)
    assert status == "PASS"


def test_verify_across_frames_requires_consecutive_fails():
    assert verify_across_frames(["FAIL", "FAIL", "FAIL"], frames_required=3) == "FAIL"
    assert verify_across_frames(["FAIL", "PASS", "FAIL"], frames_required=3) == "PASS"
    assert verify_across_frames(["FAIL", "FAIL"], frames_required=3) == "PENDING"
