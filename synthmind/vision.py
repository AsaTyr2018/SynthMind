"""Placeholder vision module for SynthMind."""

from PIL import Image


def analyze_image(image: Image.Image) -> str:
    """Return a simple description of the uploaded image.

    Parameters
    ----------
    image: PIL.Image.Image
        Image to analyze.
    """
    if image is None:
        return "No image provided."
    width, height = image.size
    return f"Received an image of size {width}x{height}px"
