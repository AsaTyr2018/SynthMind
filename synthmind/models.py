# -*- coding: utf-8 -*-
"""Utility loaders for SynthMind models.

This module provides helper functions to automatically download and load
models for the chat LLM, vision system and image generator. Models are
fetched from Hugging Face on first use and cached in the ``models``
directory of the repository.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Tuple

try:
    from huggingface_hub import snapshot_download
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        AutoModel,
        AutoProcessor,
    )
    from diffusers import StableDiffusionPipeline
except Exception:  # pragma: no cover - optional dependencies
    snapshot_download = None  # type: ignore

# Root directories for the different model types
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
LLM_DIR = MODELS_DIR / "llm"
VISION_DIR = MODELS_DIR / "vision"
GEN_DIR = MODELS_DIR / "sd"

for _d in (LLM_DIR, VISION_DIR, GEN_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# Simple caches so that models are loaded once per process
_LOADED_LLMS: dict[str, Tuple[Any, Any]] = {}
_LOADED_VISION: dict[str, Any] = {}
_LOADED_GEN: dict[str, StableDiffusionPipeline] = {}


def _ensure_download(repo_id: str, target_dir: Path) -> Path:
    """Download ``repo_id`` from Hugging Face if not already present."""
    local_dir = target_dir / repo_id.replace("/", "_")
    if not local_dir.exists():
        if snapshot_download is None:
            raise RuntimeError(
                "huggingface_hub is required to download models"
            )
        snapshot_download(repo_id, local_dir=local_dir)
    return local_dir


def get_llm(repo_id: str, device: str | None = None) -> Tuple[Any, Any]:
    """Return tokenizer and model for ``repo_id``.

    The model is downloaded on first use and cached for subsequent calls.
    """
    if repo_id not in _LOADED_LLMS:
        path = _ensure_download(repo_id, LLM_DIR)
        tokenizer = AutoTokenizer.from_pretrained(path)
        model = AutoModelForCausalLM.from_pretrained(path)
        if device:
            model.to(device)
        _LOADED_LLMS[repo_id] = (tokenizer, model)
    return _LOADED_LLMS[repo_id]


def get_vision_model(repo_id: str, device: str | None = None) -> Any:
    """Return a vision model for ``repo_id``.

    Downloads the model on first call and caches the instance.
    """
    if repo_id not in _LOADED_VISION:
        path = _ensure_download(repo_id, VISION_DIR)
        processor = AutoProcessor.from_pretrained(path)
        model = AutoModel.from_pretrained(path)
        if device:
            model.to(device)
        _LOADED_VISION[repo_id] = (processor, model)
    return _LOADED_VISION[repo_id]


def get_image_generator(repo_id: str, device: str | None = None) -> StableDiffusionPipeline:
    """Return a Stable Diffusion pipeline for ``repo_id``.

    The pipeline is downloaded on first use and then reused.
    """
    if repo_id not in _LOADED_GEN:
        path = _ensure_download(repo_id, GEN_DIR)
        pipe = StableDiffusionPipeline.from_pretrained(path)
        if device:
            pipe.to(device)
        _LOADED_GEN[repo_id] = pipe
    return _LOADED_GEN[repo_id]
