This application is intended to become a multimodal chat appliance, seamlessly combining a large language model (LLM) with a Stable Diffusion model.
Both models will be launched simultaneously via Gradio and are designed to work hand-in-hand, providing a unified user experience.

Interface
The interface will be built using Gradio and styled like a WhatsApp-style chat.
Text and image responses will appear in a continuous chat thread.
The chat input will be located below the conversation window.
A tabbed navigation bar at the top will allow users to switch between:

Chat
Personas
App Settings
Model Selection

Personas
The Personas tab allows users to choose from a set of preconfigured chat personas.
Each persona is defined by:

A background story
A psychological character profile
3–4 sample dialogue interactions

These are passed to the LLM as system prompts to simulate different behaviors or personalities.

Settings
The Settings tab provides controls for fine-tuning the LLM behavior, including:
Temperature
Verbosity
Additional generation parameters

Model Selection
The Model Selection tab displays two columns:
LLM (Chat Model)
SD (Stable Diffusion)
Models are auto-detected from the local directories:

models/llm
models/sd

Supported backends include:
Stable Diffusion: SD 1.5, SDXL
Chat Models: A list of commonly used LLMs (to be specified)

Design
The visual design is:

Dark-themed
Rounded UI elements
Accent color: Orange
