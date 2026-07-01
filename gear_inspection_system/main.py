"""
Entry point.
Runs the inspection pipeline over the full validation dataset
(10 good parts + 10 defective parts) and prints a summary.
"""

import os
from src.pipeline import inspect
from src.utils import list_images, log
from config import settings


def run_validation():
    categories = {
        "good": settings.GOOD_DIR,
        "defective": settings.DEFECTIVE_DIR,
    }

    summary = {"correct": 0, "total": 0}

    for label, folder in categories.items():
        if not os.path.exists(folder) or not os.listdir(folder):
            log(f"Skipping '{label}': no images found in {folder}", level="INFO")
            continue

        expected_status = "PASS" if label == "good" else "FAIL"

        for image_path in list_images(folder):
            result = inspect(image_path)
            summary["total"] += 1

            if result["status"] == expected_status:
                summary["correct"] += 1

    if summary["total"] > 0:
        accuracy = (summary["correct"] / summary["total"]) * 100
        log(f"Validation complete: {summary['correct']}/{summary['total']} correct "
            f"({accuracy:.1f}% accuracy)", level="INFO")
    else:
        log("No images found. Add images to data/raw/good and data/raw/defective.",
            level="ERROR")


if __name__ == "__main__":
    run_validation()
