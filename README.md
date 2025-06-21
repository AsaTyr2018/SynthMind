# SynthMind

SynthMind is a multimodal chat application that combines a large language model (LLM) with a Stable Diffusion model. The interface is built with Gradio and styled like a chat application. Models are downloaded automatically from Hugging Face on first use and cached locally.

## Features

- Chat interface with tabs for Chat, Personas, App Settings, and Model Selection
- Local LLM model listing from the `models/llm` directory
- Image generation and image analysis modes in the chat window
- Automatic model download and loading for the LLM, Stable Diffusion and vision models
- Installer script to create a virtual environment and manage system-wide installations

## Getting Started

For quick setup run the installer:

```bash
bash scripts/install.sh install
```

By default the installer places SynthMind in /opt/SynthMind on Linux or prompts for a location on Windows. Use `bash scripts/install.sh update` to upgrade and `bash scripts/install.sh uninstall` to remove the application.

### Local run

After installation or when running from a cloned repository activate the virtual environment and launch:

```bash
source venv/bin/activate
python -m synthmind.app
```

This will open a Gradio interface in your web browser.

### System-wide installation

Use the installer for management:

```bash
bash scripts/install.sh install
bash scripts/install.sh update
bash scripts/install.sh uninstall
```

### Requirements

SynthMind relies on the PyTorch library for its chat model. Install all
dependencies using the provided `requirements.txt` file:

```bash
pip install --upgrade pip
pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt
```

The `install.sh` script performs this step automatically when creating the
virtual environment.
