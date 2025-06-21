import gradio as gr
import socket


def generate_response(user_input, history):
    """Placeholder text generation function."""
    # TODO: integrate LLM here
    return "This is a placeholder response."


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
        gr.Markdown("## Personas")
        gr.Dropdown(["Default", "Friendly", "Professional"], label="Select Persona")
        gr.Markdown("(Persona profiles coming soon)")
    with gr.Tab("App Settings"):
        gr.Markdown("## Settings")
        gr.Slider(minimum=0, maximum=1, value=0.7, label="Temperature")
        gr.Markdown("(Additional settings will be available)")
    with gr.Tab("Model Selection"):
        gr.Markdown("## Model Selection")
        with gr.Row():
            gr.Column()
            gr.Column()
        gr.Markdown("(Model selection placeholder)")
    send_btn.click(
        lambda msg, history: (history + [(msg, generate_response(msg, history))], ""),
        [chat_input, chatbot],
        [chatbot, chat_input]
    )
    chat_input.submit(
        lambda msg, history: (history + [(msg, generate_response(msg, history))], ""),
        [chat_input, chatbot],
        [chatbot, chat_input]
    )

demo.launch(server_name=get_local_ip())
