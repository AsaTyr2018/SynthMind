# SynthMind

SynthMind is a multimodal chat application that combines a large language model (LLM) with a Stable Diffusion model. The interface is built with Gradio and styled like a chat application. The project currently provides a basic foundation with placeholder text and image generation.

## Features

- Chat interface with tabs for Chat, Personas, App Settings, and Model Selection
- Ollama-backed LLM integration with model downloader
- Configurable Ollama host via the `OLLAMA_HOST` environment variable
- Placeholder Stable Diffusion calls
- Simple setup script to create a virtual environment and install dependencies

## Getting Started

Run `scripts/setup.sh` to create a virtual environment and install the required Python packages.
Make sure an Ollama server is running locally or set `OLLAMA_HOST` to point to your Ollama instance.
Then launch the application:

```bash
source venv/bin/activate
python -m synthmind.app
```

This will open a Gradio interface in your web browser.
