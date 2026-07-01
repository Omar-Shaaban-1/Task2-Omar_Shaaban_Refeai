# Gear Inspection System

Automated optical inspection pipeline for detecting structural defects
(e.g. broken teeth) on gears using OpenCV.

## Architecture (IPO)

```
Phase 1: Pre-process   -> grayscale, Gaussian blur, threshold
Phase 2: Topology       -> find contour, convex hull, convexity defects
Phase 3: Tolerance gate -> compare defect depth vs threshold, PASS/FAIL
```

## Setup

```bash
pip install -r requirements.txt
```

## Usage

1. Drop your 10 good images into `data/raw/good/`
2. Drop your 10 defective images into `data/raw/defective/`
3. Run:

```bash
python main.py
```

Annotated output images (with PASS/FAIL banner and defect boxes)
are saved to `data/results/`.

## Calibration

Open `config/settings.py` and tune:

- `THRESHOLD_MAX` — run your "good" parts first, check the max
  defect distance they produce, set this just above it.
- `BINARY_THRESH` — adjust if your background/part contrast differs.
- `GAUSSIAN_KERNEL` — increase (e.g. (7,7)) for noisier images.

## Folder structure

```
gear_inspection_system/
├── data/raw/{good,defective}/   ← input images
├── data/results/                ← annotated output
├── src/                          ← pipeline phases
├── functions/                    ← low-level helpers (I/O, drawing, logging)
├── config/settings.py            ← all tunable constants
├── tests/                        ← unit tests
└── main.py                       ← run this
```

## Running tests

```bash
python -m pytest tests/
```
