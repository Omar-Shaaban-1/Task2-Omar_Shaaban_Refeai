"""
Phase 2: Topological analysis.
Stop looking at pixels, start looking at geometry.
"""

import cv2


def get_largest_contour(thresh_img):
    """
    Find the outer boundary of the part (ignoring internal features
    like holes) and return the largest one found — that's the part.
    Returns None if no contours are found.
    """
    contours, _ = cv2.findContours(
        thresh_img,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return None

    return max(contours, key=cv2.contourArea)


def get_convex_hull(contour):
    """
    Compute the convex hull (the "rubber band" shape) of a contour.
    returnPoints=False gives hull indices, required for convexityDefects.
    """
    return cv2.convexHull(contour, returnPoints=False)


def get_convexity_defects(contour, hull):
    """
    Compute the convexity defects between the contour and its hull.
    Returns None if the contour is already fully convex (no defects).
    """
    if hull is None or len(hull) < 3:
        return None

    try:
        defects = cv2.convexityDefects(contour, hull)
    except cv2.error:
        # Can happen if the hull is malformed (e.g. non-convex sorted hull)
        return None

    return defects


def analyze_topology(thresh_img):
    """
    Run the full Phase 2 pipeline.
    Returns (contour, hull, defects) — any of which may be None
    if the part/shape couldn't be analyzed.
    """
    contour = get_largest_contour(thresh_img)
    if contour is None:
        return None, None, None

    hull = get_convex_hull(contour)
    defects = get_convexity_defects(contour, hull)

    return contour, hull, defects
