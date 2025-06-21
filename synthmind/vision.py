"""Vision module for SynthMind.

Uses models loaded via :mod:`synthmind.models` to analyse uploaded images.
The required weights are downloaded automatically on first run and cached
under ``models/vision``.
"""

from PIL import Image

from .models import get_vision_model

DEFAULT_VISION_MODEL = "google/vit-base-patch16-224"


def analyze_image(image: Image.Image, model: str | None = None) -> str:
    """Analyse an image and return a description."""

    if image is None:
        return "No image provided."

    repo_id = model or DEFAULT_VISION_MODEL
    processor, vision_model = get_vision_model(repo_id)
    inputs = processor(images=image, return_tensors="pt")
    outputs = vision_model(**inputs)
    logits = outputs.logits.detach()
    predicted = logits.argmax(-1).item()
    label = vision_model.config.id2label.get(predicted, str(predicted))
    return f"Detected: {label}"
