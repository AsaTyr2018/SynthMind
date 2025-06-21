import gradio as gr
import socket
import ollama
import json
from pathlib import Path

PERSONA_DIR = Path(__file__).resolve().parent.parent / "persona"
PERSONA_DIR.mkdir(exist_ok=True)


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
        return gr.update(), update_persona_list()
    data = {
        "name": name,
        "background": background,
        "character": character,
        "dialog_examples": [d for d in [d1, d2, d3] if d.strip()],
    }
    path = PERSONA_DIR / f"{name}.json"
    with path.open("w") as f:
        json.dump(data, f, indent=2)
    return gr.update(choices=list_personas(), value=name), update_persona_list()


def delete_persona(name):
    """Remove persona JSON file."""
    path = PERSONA_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
    return (
        "",
        "",
        "",
        "",
        "",
        "",
        gr.update(choices=list_personas(), value=None),
        update_persona_list(),
    )


def update_persona_list():
    names = list_personas()
    if not names:
        return "No personas found."
    return "\n".join(f"- {n}" for n in names)


# LLM integration with Ollama
def list_llm_models():
    try:
        return [m["name"] for m in ollama.list().get("models", [])]
    except Exception:
        return []

def download_llm_model(name):
    try:
        ollama.pull(name)
        return f"Downloaded {name}"
    except Exception as e:
        return f"Error: {e}"

def generate_response(user_input, history, model):
    messages = [{"role": "user", "content": user_input}]
    for u, b in history:
        messages.insert(0, {"role": "assistant", "content": b})
        messages.insert(0, {"role": "user", "content": u})
    try:
        resp = ollama.chat(model=model, messages=messages)
        return resp["message"]["content"]
    except Exception as e:
        return f"Error: {e}"



def generate_image(prompt):
    """Placeholder image generation function."""
    # TODO: integrate Stable Diffusion here
    return None


# Chat interface elements
chatbot = gr.Chatbot()
chat_input = gr.Textbox(placeholder="Type a message...", scale=8, lines=1)
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
    gr.Markdown("# SynthMind")
    with gr.Tab("Chat"):
        with gr.Column():
            chatbot.render()
        with gr.Row():
            chat_input.render()
            send_btn.render()
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
            return load_persona(name)

        persona_select.change(
            load_selected,
            persona_select,
            [name_box, background_box, character_box, dialog1, dialog2, dialog3],
        )

        save_btn.click(
            save_persona,
            [name_box, background_box, character_box, dialog1, dialog2, dialog3],
            [persona_select, persona_list_md],
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
        model_dropdown = gr.Dropdown(list_llm_models(), label="Available LLM Models")
        refresh_models_btn = gr.Button("Refresh")
        download_box = gr.Textbox(label="Model to download")
        download_btn = gr.Button("Download")
        download_msg = gr.Markdown()
        refresh_models_btn.click(lambda: gr.update(choices=list_llm_models()), None, model_dropdown)
        download_btn.click(lambda name: (download_llm_model(name), gr.update(choices=list_llm_models())), download_box, [download_msg, model_dropdown])
    send_btn.click(
        lambda msg, history, model: (history + [(msg, generate_response(msg, history, model))], ""),
        [chat_input, chatbot, model_dropdown],
        [chatbot, chat_input]
    )
    chat_input.submit(
        lambda msg, history, model: (history + [(msg, generate_response(msg, history, model))], ""),
        [chat_input, chatbot, model_dropdown],
        [chatbot, chat_input]
    )

demo.launch(server_name=get_local_ip())
