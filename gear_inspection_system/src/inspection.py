"""
Phase 3: Tolerance gate.
Compare measured defect depths against calibrated limits to
produce a deterministic PASS/FAIL decision.
"""

import cv2
from config import settings


def evaluate_defects(contour, defects, threshold_max=None):
    """
    Walk through the convexity defect array and flag any defect
    whose depth exceeds the allowed tolerance.

    Returns:
        status: "PASS" or "FAIL"
        flagged_defects: list of dicts, one per defect that failed,
                         each with keys: farthest_point, bbox, distance
    """
    if threshold_max is None:
        threshold_max = settings.THRESHOLD_MAX

    flagged_defects = []

    if defects is None:
        return "PASS", flagged_defects

    for i in range(defects.shape[0]):
        start_idx, end_idx, farthest_idx, raw_distance = defects[i, 0]

        # ── Critical fix: OpenCV scales distance by 256 ──
        actual_distance = raw_distance / 256.0

        if actual_distance > threshold_max:
            farthest_point = tuple(contour[farthest_idx][0])

            # Bounding box around the defect region (start -> end span)
            lo, hi = sorted([start_idx, end_idx])
            defect_segment = contour[lo:hi] if hi > lo else contour[hi:lo]

            if len(defect_segment) == 0:
                defect_segment = contour  # fallback: box the whole contour

            x, y, w, h = cv2.boundingRect(defect_segment)

            flagged_defects.append({
                "farthest_point": farthest_point,
                "bbox": (x, y, w, h),
                "distance": actual_distance
            })

    status = "FAIL" if flagged_defects else "PASS"
    return status, flagged_defects


def verify_across_frames(frame_results, frames_required=None):
    """
    PLC-style triple verification: only confirm a FAIL if it shows up
    in at least `frames_required` consecutive frame results.
    This reduces false rejections from a single noisy frame.

    frame_results: list of "PASS"/"FAIL" strings from consecutive frames.
    """
    if frames_required is None:
        frames_required = settings.FRAMES_TO_VERIFY

    if len(frame_results) < frames_required:
        return "PENDING"  # Not enough frames yet to decide

    recent = frame_results[-frames_required:]
    fail_count = recent.count("FAIL")

    return "FAIL" if fail_count == frames_required else "PASS"
