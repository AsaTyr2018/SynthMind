#!/usr/bin/env bash
set -e

REPO_URL="https://github.com/AsaTyr2018/SynthMind.git"
DEFAULT_INSTALL_DIR_LINUX="/opt/SynthMind"

run() {
    echo "[RUN] $*"
    eval "$*"
}

venv_bin() {
    local venv="$1"
    local name="$2"
    if [[ "$(uname)" == "Windows_NT" ]]; then
        echo "$venv/Scripts/$name"
    else
        echo "$venv/bin/$name"
    fi
}

ensure_dir() {
    local path="$1"
    if [[ ! -d "$path" ]]; then
        mkdir -p "$path" 2>/dev/null || sudo mkdir -p "$path"
    fi
    if [[ ! -w "$path" ]]; then
        sudo chown -R "$(id -u)":"$(id -g)" "$path"
    fi
}

create_venv() {
    local target="$1"
    local venv="$target/venv"
    if [[ ! -d "$venv" ]]; then
        run "python3 -m venv \"$venv\""
    fi
    local pip
    pip=$(venv_bin "$venv" pip)
    run "\"$pip\" install --upgrade pip"
    run "\"$pip\" install --extra-index-url https://download.pytorch.org/whl/cpu -r \"$target/requirements.txt\""
}

get_default_dir() {
    if [[ "$(uname)" == "Windows_NT" ]]; then
        read -r -p "Installation directory [e.g. C:\\SynthMind]: " dest
        echo "$dest"
    else
        echo "$DEFAULT_INSTALL_DIR_LINUX"
    fi
}

install_cmd() {
    local target="${TARGET:-$(get_default_dir)}"
    if [[ -e "$target" ]]; then
        echo "Target directory $target already exists"
        exit 1
    fi
    ensure_dir "$(dirname "$target")"
    run "git clone $REPO_URL \"$target\""
    create_venv "$target"
    echo "Installation complete."
}

update_cmd() {
    local target="${TARGET:-$(get_default_dir)}"
    if [[ ! -d "$target" ]]; then
        echo "Target directory $target does not exist"
        exit 1
    fi
    run "git -C \"$target\" pull"
    create_venv "$target"
    echo "Update complete."
}

uninstall_cmd() {
    local target="${TARGET:-$(get_default_dir)}"
    if [[ ! -d "$target" ]]; then
        echo "Target directory $target does not exist"
        return
    fi
    if [[ "$(uname)" == "Windows_NT" ]]; then
        rm -rf "$target"
    else
        sudo rm -rf "$target"
    fi
    echo "Uninstall complete."
}

display_usage() {
    echo "Usage: $0 {install|update|uninstall} [--target DIR]"
    exit 1
}

COMMAND="$1"
shift || true
TARGET=""
while [[ $# -gt 0 ]]; do
    case "$1" in
        --target)
            TARGET="$2"; shift 2 ;;
        *)
            echo "Unknown argument: $1"; display_usage ;;
    esac
done

case "$COMMAND" in
    install) install_cmd ;;
    update) update_cmd ;;
    uninstall) uninstall_cmd ;;
    *) display_usage ;;
esac
