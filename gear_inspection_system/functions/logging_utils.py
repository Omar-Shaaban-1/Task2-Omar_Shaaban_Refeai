"""
Lightweight logging helpers — consistent console output across the pipeline.
"""

from datetime import datetime


def log(message, level="INFO"):
    """
    Print a timestamped log line.
    Levels: INFO, PASS, FAIL, ERROR
    """
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def log_result(filename, status, defect_count=0):
    """
    Print a standardized result line for one inspected image.
    """
    level = "PASS" if status == "PASS" else "FAIL"
    detail = f" ({defect_count} defect(s))" if defect_count else ""
    log(f"{filename} -> {status}{detail}", level=level)
