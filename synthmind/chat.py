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
    persona: str | None = None,
) -> str:
    """Generate a response using the selected LLM.

    The model is downloaded and loaded automatically on first use.
    """

    repo_id = model or DEFAULT_LLM
    tokenizer, llm = get_llm(repo_id)

    history = history or []
    context = ""
    for h in history[-2:]:
        context += f"User: {h[0]}\nAssistant: {h[1]}\n"
    prompt_parts = []
    if persona:
        prompt_parts.append(persona)
    if context:
        prompt_parts.append(context)
    prompt_parts.append(f"User: {user_input}\nAssistant:")
    prompt = "\n".join(prompt_parts)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = llm.generate(**inputs, max_new_tokens=50)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
