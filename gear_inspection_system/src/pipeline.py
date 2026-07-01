"""
The full inspection pipeline.
Ties Phase 1 (preprocessing) -> Phase 2 (topology) -> Phase 3 (inspection)
together into one function: inspect().
"""

import os

from src.preprocessing import preprocess
from src.topology import analyze_topology
from src.inspection import evaluate_defects
from src.utils import (
    load_image, save_image,
    draw_defect_box, draw_label, draw_status_banner,
    log, log_result,
)
from config import settings


def inspect(image_path, save_result=True, results_dir=None):
    """
    Run the full inspection pipeline on a single image.

    Returns a dict:
        {
            "filename": str,
            "status": "PASS" | "FAIL" | "ERROR",
            "defects": list of flagged defect dicts,
            "output_path": str or None
        }
    """
    filename = os.path.basename(image_path)
    results_dir = results_dir or settings.RESULTS_DIR

    try:
        img = load_image(image_path)
    except (FileNotFoundError, ValueError) as e:
        log(f"{filename}: {e}", level="ERROR")
        return {"filename": filename, "status": "ERROR", "defects": [], "output_path": None}

    # ── Phase 1: Pre-process ──
    thresh = preprocess(img)

    # ── Phase 2: Topology ──
    contour, hull, defects = analyze_topology(thresh)

    if contour is None:
        log(f"{filename}: no part detected in frame", level="ERROR")
        return {"filename": filename, "status": "ERROR", "defects": [], "output_path": None}

    # ── Phase 3: Tolerance gate ──
    status, flagged_defects = evaluate_defects(contour, defects)

    # ── Visualize the verdict ──
    output_img = img.copy()
    for defect in flagged_defects:
        x, y, w, h = defect["bbox"]
        draw_defect_box(output_img, x, y, w, h, color=settings.BOX_COLOR)
        draw_label(output_img, "DEFECT", defect["farthest_point"], color=settings.FAIL_COLOR)

    draw_status_banner(output_img, status, settings.PASS_COLOR, settings.FAIL_COLOR)

    output_path = None
    if save_result:
        output_path = os.path.join(results_dir, filename)
        save_image(output_img, output_path)

    log_result(filename, status, defect_count=len(flagged_defects))

    return {
        "filename": filename,
        "status": status,
        "defects": flagged_defects,
        "output_path": output_path,
    }
