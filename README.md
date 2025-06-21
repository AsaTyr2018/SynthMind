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
python scripts/install.py install
```

By default the installer places SynthMind in /opt/SynthMind on Linux or prompts for a location on Windows. Use `python scripts/install.py update` to upgrade and `python scripts/install.py uninstall` to remove the application.

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
python scripts/install.py install
python scripts/install.py update
python scripts/install.py uninstall
```
