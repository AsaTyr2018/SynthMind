"""Chat module for SynthMind.

This module now loads language models on demand using the helpers in
``synthmind.models``. Models are downloaded automatically the first time
they are requested and cached in ``models/llm``.
"""

from typing import List, Tuple, Optional

from .models import get_llm

DEFAULT_LLM = "distilgpt2"


def generate_response(
    user_input: str,
    history: List[Tuple[str, str]] | None = None,
    model: Optional[str] = None,
) -> str:
    """Generate a response using the selected LLM.

    The model is downloaded and loaded automatically on first use.
    """

    repo_id = model or DEFAULT_LLM
    tokenizer, llm = get_llm(repo_id)

    inputs = tokenizer(user_input, return_tensors="pt")
    outputs = llm.generate(**inputs, max_new_tokens=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
