import gradio as gr
import socket
import json
from pathlib import Path

from .chat import generate_response
from .generator import generate_image
from .vision import analyze_image

PERSONA_DIR = Path(__file__).resolve().parent.parent / "persona"
PERSONA_DIR.mkdir(exist_ok=True)
LLM_MODELS_DIR = Path(__file__).resolve().parent.parent / "models" / "llm"


def list_personas():
    """Return a list of available persona names."""
    return sorted([p.stem for p in PERSONA_DIR.glob("*.json")])


def load_persona(name):
    """Load a persona JSON file."""
    path = PERSONA_DIR / f"{name}.json"
    if not path.exists():
        return "", "", "", "", "", ""
    with path.open() as f:
        data = json.load(f)
    dialogs = data.get("dialog_examples", [])
    dialogs += ["", "", ""]
    return (
        data.get("name", name),
        data.get("background", ""),
        data.get("character", ""),
        dialogs[0],
        dialogs[1],
        dialogs[2],
    )


def save_persona(name, background, character, d1, d2, d3):
    """Save persona data to a JSON file."""
    if not name:
        choices = list_personas()
        return (
            gr.update(choices=choices, value=None),
            update_persona_list(),
            gr.update(choices=choices, value=None),
            None,
        )
    data = {
        "name": name,
        "background": background,
        "character": character,
        "dialog_examples": [d for d in [d1, d2, d3] if d.strip()],
    }
    path = PERSONA_DIR / f"{name}.json"
    with path.open("w") as f:
        json.dump(data, f, indent=2)
    choices = list_personas()
    return (
        gr.update(choices=choices, value=name),
        update_persona_list(),
        gr.update(choices=choices, value=name),
        name,
    )


def delete_persona(name):
    """Remove persona JSON file."""
    path = PERSONA_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
    choices = list_personas()
    return (
        "",
        "",
        "",
        "",
        "",
        "",
        gr.update(choices=choices, value=None),
        update_persona_list(),
        gr.update(choices=choices, value=None),
        None,
    )


def update_persona_list():
    names = list_personas()
    if not names:
        return "No personas found."
    return "\n".join(f"- {n}" for n in names)


def get_persona_prompt(name: str) -> str:
    """Return a short prompt string for ``name``."""
    if not name:
        return ""
    path = PERSONA_DIR / f"{name}.json"
    if not path.exists():
        return ""
    with path.open() as f:
        data = json.load(f)
    parts = []
    if data.get("background"):
        parts.append(f"Background: {data['background']}")
    if data.get("character"):
        parts.append(f"Character: {data['character']}")
    examples = data.get("dialog_examples", [])[:2]
    for ex in examples:
        parts.append(ex)
    return "\n".join(parts)


# LLM model handling
def list_llm_models():
    """Return available LLM models from the local models directory."""
    if not LLM_MODELS_DIR.exists():
        return []
    models = []
    for p in LLM_MODELS_DIR.iterdir():
        if p.is_file():
            models.append(p.stem)
        elif p.is_dir():
            models.append(p.name)
    return sorted(models)


# Chat interface elements
chatbot = gr.Chatbot()
chat_input = gr.Textbox(placeholder="Type a message...", scale=8, lines=1)
image_input = gr.Image(type="pil", visible=False)
persona_state = gr.State(value=None)
chat_persona_select = gr.Dropdown(list_personas(), label="Persona", value=None)
mode_select = gr.Radio([
    "Chat",
    "Generate Image",
    "Analyze Image",
],
    value="Chat",
    label="Mode",
)
send_btn = gr.Button("Send", scale=1)


# Determine local network IP address for the Gradio server
def get_local_ip() -> str:
    """Return the local network IP address for this machine."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This address doesn't need to be reachable
        s.connect(("10.255.255.255", 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


theme = gr.themes.Soft(primary_hue="orange")

with gr.Blocks(theme=theme) as demo:
    # Register persona_state so Gradio tracks it properly.
    persona_state.render()

    gr.Markdown("# SynthMind")
    with gr.Tab("Chat"):
        with gr.Column():
            chatbot.render()
        with gr.Row():
            chat_input.render()
            send_btn.render()
        with gr.Row():
            chat_persona_select.render()
            mode_select.render()
            image_input.render()
    with gr.Tab("Personas"):
        gr.Markdown("## Personas Editor")
        persona_select = gr.Dropdown(list_personas(), label="Select Persona")
        persona_list_md = gr.Markdown(update_persona_list())
        name_box = gr.Textbox(label="Name")
        background_box = gr.Textbox(label="Background", lines=3)
        character_box = gr.Textbox(label="Character", lines=3)
        dialog1 = gr.Textbox(label="Example Dialog 1", lines=1)
        dialog2 = gr.Textbox(label="Example Dialog 2", lines=1)
        dialog3 = gr.Textbox(label="Example Dialog 3", lines=1)
        with gr.Row():
            save_btn = gr.Button("Save Persona")
            delete_btn = gr.Button("Delete Persona")

        def load_selected(name):
            data = load_persona(name)
            return (*data, name, gr.update(value=name))

        persona_select.change(
            load_selected,
            persona_select,
            [
                name_box,
                background_box,
                character_box,
                dialog1,
                dialog2,
                dialog3,
                persona_state,
                chat_persona_select,
            ],
        )

        save_btn.click(
            save_persona,
            [
                name_box,
                background_box,
                character_box,
                dialog1,
                dialog2,
                dialog3,
            ],
            [
                persona_select,
                persona_list_md,
                chat_persona_select,
                persona_state,
            ],
        )

        delete_btn.click(
            delete_persona,
            persona_select,
            [
                name_box,
                background_box,
                character_box,
                dialog1,
                dialog2,
                dialog3,
                persona_select,
                persona_list_md,
                chat_persona_select,
                persona_state,
            ],
        )
    with gr.Tab("App Settings"):
        gr.Markdown("## Settings")
        gr.Slider(
            minimum=0,
            maximum=1.5,
            value=0.7,
            label="temperature",
            info="Randomness of the output; higher values increase variety",
        )
        gr.Slider(
            minimum=0,
            maximum=1,
            value=0.9,
            label="top_p",
            info="Limits tokens to a cumulative probability mass",
        )
        gr.Slider(
            minimum=1,
            maximum=100,
            step=1,
            value=50,
            label="top_k",
            info="Choose from the top k most likely tokens",
        )
        gr.Slider(
            minimum=1,
            maximum=512,
            step=1,
            value=256,
            label="max_tokens",
            info="Maximum number of tokens to generate",
        )
        gr.Slider(
            minimum=0.5,
            maximum=2.0,
            value=1.1,
            label="repetition_penalty",
            info="Penalty applied to repeated text",
        )
        gr.Slider(
            minimum=0,
            maximum=1,
            value=0.6,
            label="presence_penalty",
            info="Discourages introducing topics already mentioned",
        )
        gr.Slider(
            minimum=0,
            maximum=1,
            value=0.5,
            label="frequency_penalty",
            info="Reduces likelihood of frequent tokens",
        )
        gr.Textbox(
            value='["\n", "###"]',
            label="stop",
            info="Stop generation when any of these sequences appear",
        )
        gr.Number(
            value=None,
            label="logprobs",
            info="Return log probabilities for generated tokens",
        )
        gr.Checkbox(
            value=False,
            label="echo",
            info="Include the prompt text in the output",
        )
        gr.Number(
            value=None,
            label="seed",
            info="Random seed for reproducible results",
        )
    with gr.Tab("Model Selection"):
        gr.Markdown("## Model Selection")
        model_dropdown = gr.Dropdown(
            list_llm_models(),
            label="Available LLM Models",
        )
        refresh_models_btn = gr.Button("Refresh")
        refresh_models_btn.click(
            lambda: gr.update(choices=list_llm_models()),
            None,
            model_dropdown,
        )

    def process_message(msg, history, mode, image, model, persona_name):
        if mode == "Generate Image":
            img = generate_image(msg)
            return history + [(msg, img)], "", None
        if mode == "Analyze Image":
            if image is None:
                return history + [(msg, "Please upload an image.")], "", None
            analysis = analyze_image(image)
            return history + [(image, analysis)], "", None
        # default Chat mode
        persona_prompt = get_persona_prompt(persona_name)
        response = generate_response(msg, history, model, persona_prompt)
        return history + [(msg, response)], "", None

    send_btn.click(
        process_message,
        [
            chat_input,
            chatbot,
            mode_select,
            image_input,
            model_dropdown,
            persona_state,
        ],
        [chatbot, chat_input, image_input],
    )
    chat_input.submit(
        process_message,
        [
            chat_input,
            chatbot,
            mode_select,
            image_input,
            model_dropdown,
            persona_state,
        ],
        [chatbot, chat_input, image_input],
    )

    chat_persona_select.change(
        lambda x: x,
        chat_persona_select,
        persona_state,
    )

    def toggle_image_input(mode):
        return gr.update(visible=mode == "Analyze Image")

    mode_select.change(toggle_image_input, mode_select, image_input)

demo.launch(server_name=get_local_ip())
