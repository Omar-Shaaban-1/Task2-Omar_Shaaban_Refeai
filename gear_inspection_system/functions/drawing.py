"""
Drawing helper functions — bounding boxes, labels, status overlays.
"""

import cv2


def draw_defect_box(img, x, y, w, h, color=(0, 0, 255), thickness=2):
    """
    Draw a rectangle around a detected defect region.
    """
    cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
    return img


def draw_label(img, text, position, color=(0, 0, 255), scale=0.6):
    """
    Draw a text label at a given (x, y) position.
    """
    cv2.putText(
        img, text, position,
        cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2
    )
    return img


def draw_status_banner(img, status, pass_color=(0, 255, 0), fail_color=(0, 0, 255)):
    """
    Draw a PASS/FAIL status banner in the top-left corner of the image.
    """
    color = pass_color if status == "PASS" else fail_color
    cv2.putText(
        img, f"STATUS: {status}", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2
    )
    return img
