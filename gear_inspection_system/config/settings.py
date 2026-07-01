"""
Central configuration for the gear inspection pipeline.
Change values here instead of digging through pipeline code.
"""

# ── Phase 1: Pre-processing ──
GAUSSIAN_KERNEL = (5, 5)     # Must be odd numbers (3,3) (5,5) (7,7)...
GAUSSIAN_SIGMA = 0           # 0 = auto-calculated from kernel size
BINARY_THRESH = 127          # Pixel intensity cutoff for binarization (0-255)
BINARY_MAX_VAL = 255

# ── Phase 3: Tolerance gate ──
THRESHOLD_MAX = 15           # Max allowed convexity defect depth (pixels)
                              # Calibrate this using your 10 "good" parts:
                              # run them through and set this just above
                              # the largest defect depth they produce.

# ── PLC / verification logic ──
FRAMES_TO_VERIFY = 3         # Triple-frame verification before actuating reject

# ── Paths ──
DATA_DIR = "data/raw"
GOOD_DIR = "data/raw/good"
DEFECTIVE_DIR = "data/raw/defective"
PROCESSED_DIR = "data/processed"
RESULTS_DIR = "data/results"

# ── Drawing ──
BOX_COLOR = (0, 0, 255)      # Red, BGR format
BOX_THICKNESS = 2
FONT = "FONT_HERSHEY_SIMPLEX"
FONT_SCALE = 0.6
PASS_COLOR = (0, 255, 0)     # Green
FAIL_COLOR = (0, 0, 255)     # Red
