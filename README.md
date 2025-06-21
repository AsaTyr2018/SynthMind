# SynthMind

SynthMind is a multimodal chat application that combines a large language model (LLM) with a Stable Diffusion model. The interface is built with Gradio and styled like a chat application. Models are downloaded automatically from Hugging Face on first use and cached locally.

## Features

- Chat interface with tabs for Chat, Personas, App Settings, and Model Selection
- Local LLM model listing from the `models/llm` directory
- Image generation and image analysis modes in the chat window
- Automatic model download and loading for the LLM, Stable Diffusion and vision models
- Simple setup script to create a virtual environment and install dependencies

## Getting Started

For a quick local setup you can still use `scripts/setup.sh` to create a virtual environment in the
current repository and install the required Python packages (`gradio`, `transformers`, `diffusers`, and `huggingface_hub`). To manage a system wide installation
use the new `scripts/installer.py` script which supports `install`, `update` and `uninstall`
commands. By default the installer places SynthMind in `/opt/SynthMind` on Linux and in a
`SynthMind` directory inside your home folder on Windows.

### Local run

Run `scripts/setup.sh` and then launch the application:

```bash
source venv/bin/activate
python -m synthmind.app
```

This will open a Gradio interface in your web browser.

### System-wide installation

The `scripts/installer.py` helper can clone the repository, set up a virtual environment and update or remove the installation:

```bash
python scripts/installer.py install --repo <git_url>
python scripts/installer.py update
python scripts/installer.py uninstall
```
