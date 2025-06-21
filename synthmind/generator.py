"""Image generation module for SynthMind.

Stable Diffusion pipelines are automatically downloaded and cached in
``models/sd`` using the helpers from :mod:`synthmind.models`.
"""

from PIL import Image

from .models import get_image_generator

DEFAULT_SD_MODEL = "runwayml/stable-diffusion-v1-5"


def generate_image(prompt: str, size: int = 512, model: str | None = None) -> Image.Image:
    """Generate an image from ``prompt`` using Stable Diffusion."""

    repo_id = model or DEFAULT_SD_MODEL
    pipe = get_image_generator(repo_id)
    image = pipe(prompt, height=size, width=size).images[0]
    return image
