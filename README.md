# SynthMind

SynthMind is a multimodal chat application that combines a large language model (LLM) with a Stable Diffusion model. The interface is built with Gradio and styled like a chat application. The project currently provides a basic framework with placeholder implementations for text and image generation as well as image understanding.

## Features

- Chat interface with tabs for Chat, Personas, App Settings, and Model Selection
- Local LLM model listing from the `models/llm` directory
- Image generation and image analysis modes in the chat window
- Placeholder modules for the LLM, Stable Diffusion and vision model
- Simple setup script to create a virtual environment and install dependencies

## Getting Started

Run `scripts/setup.sh` to create a virtual environment and install the required Python packages.
Then launch the application:

```bash
source venv/bin/activate
python -m synthmind.app
```

This will open a Gradio interface in your web browser.
