"""
Tests for src/preprocessing.py
"""

import numpy as np
from src.preprocessing import to_grayscale, apply_blur, binarize, preprocess


def make_dummy_color_image():
    """A 100x100 black image with a white square in the middle."""
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    img[30:70, 30:70] = 255
    return img


def test_to_grayscale_reduces_channels():
    img = make_dummy_color_image()
    gray = to_grayscale(img)
    assert gray.ndim == 2  # single channel


def test_binarize_produces_only_two_values():
    img = make_dummy_color_image()
    gray = to_grayscale(img)
    blurred = apply_blur(gray)
    thresh = binarize(blurred)
    unique_values = set(np.unique(thresh))
    assert unique_values.issubset({0, 255})


def test_preprocess_end_to_end():
    img = make_dummy_color_image()
    result = preprocess(img)
    assert result.shape == (100, 100)
    assert set(np.unique(result)).issubset({0, 255})
