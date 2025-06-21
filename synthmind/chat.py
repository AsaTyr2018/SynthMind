"""Chat module for SynthMind.

This module loads language models on demand using the helpers in
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

    ``persona`` is appended as a system prompt after the user text. Only the
    newly generated tokens are returned so that the prompt itself is not echoed
    in the chat history. The model weights are downloaded and cached on first
    use.
    """

    repo_id = model or DEFAULT_LLM
    tokenizer, llm = get_llm(repo_id)

    history = history or []
    context = ""
    for h in history[-2:]:
        context += f"User: {h[0]}\nAssistant: {h[1]}\n"

    prompt_parts = []
    if context:
        prompt_parts.append(context)
    prompt_parts.append(f"User: {user_input}")
    if persona:
        prompt_parts.append(f"System: {persona}")
    prompt_parts.append("Assistant:")
    prompt = "\n".join(prompt_parts)

    inputs = tokenizer(prompt, return_tensors="pt")
    generated = llm.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_new_tokens=50,
    )
    new_tokens = generated[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
