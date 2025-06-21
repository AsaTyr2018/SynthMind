#!/bin/bash
# Basic setup script for SynthMind

set -e

REPO_DIR=$(cd "$(dirname "$0")/.." && pwd)
VENV_DIR="$REPO_DIR/venv"

python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

pip install --upgrade pip
pip install gradio transformers diffusers huggingface_hub

echo "Setup complete. Activate the virtual environment using: source $VENV_DIR/bin/activate"
