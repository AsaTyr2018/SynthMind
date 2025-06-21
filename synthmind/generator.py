"""Placeholder image generation module for SynthMind."""

from PIL import Image, ImageDraw, ImageFont


def generate_image(prompt: str, size: int = 512) -> Image.Image:
    """Return a simple placeholder image with the prompt text.

    Parameters
    ----------
    prompt: str
        Text prompt for image generation.
    size: int
        Output image size in pixels (square).
    """
    # Create a blank image and draw the prompt text on it. This is just a
    # stand-in for a Stable Diffusion call.
    img = Image.new("RGB", (size, size), color="white")
    draw = ImageDraw.Draw(img)
    text = f"Generated:\n{prompt}"
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.multiline_text((10, 10), text, fill="black", font=font)
    return img
