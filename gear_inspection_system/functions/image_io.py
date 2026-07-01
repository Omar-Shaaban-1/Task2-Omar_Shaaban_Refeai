"""
Image input/output helper functions.
"""

import cv2
import os


def load_image(path):
    """
    Load an image from disk. Raises a clear error if the file
    doesn't exist or OpenCV fails to decode it.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Image not found: {path}")

    img = cv2.imread(path)

    if img is None:
        raise ValueError(f"OpenCV could not decode image: {path}")

    return img


def save_image(img, path):
    """
    Save an image to disk, creating parent folders if needed.
    """
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    success = cv2.imwrite(path, img)

    if not success:
        raise IOError(f"Failed to save image to: {path}")

    return path


def list_images(folder, extensions=(".jpg", ".jpeg", ".png", ".bmp")):
    """
    Return a sorted list of full paths to all image files in a folder.
    """
    if not os.path.exists(folder):
        raise FileNotFoundError(f"Folder not found: {folder}")

    files = [
        os.path.join(folder, f)
        for f in sorted(os.listdir(folder))
        if f.lower().endswith(extensions)
    ]
    return files
