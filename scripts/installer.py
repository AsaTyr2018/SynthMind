#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_REPO_URL = "https://github.com/yourusername/SynthMind.git"
DEFAULT_INSTALL_DIR_LINUX = Path("/opt/SynthMind")
DEFAULT_INSTALL_DIR_WINDOWS = Path.home() / "SynthMind"


def run(cmd, cwd=None):
    """Run a shell command."""
    print(f"[RUN] {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def venv_bin(venv: Path, name: str) -> Path:
    """Return the path to an executable inside the venv."""
    if platform.system() == "Windows":
        return venv / "Scripts" / name
    return venv / "bin" / name


def create_venv(target_dir: Path):
    venv_dir = target_dir / "venv"
    if not venv_dir.exists():
        run(f"{sys.executable} -m venv {venv_dir}")
    pip = venv_bin(venv_dir, "pip")
    run(f"{pip} install --upgrade pip")
    run(f"{pip} install gradio")


def get_default_dir() -> Path:
    if platform.system() == "Windows":
        return DEFAULT_INSTALL_DIR_WINDOWS
    return DEFAULT_INSTALL_DIR_LINUX


def install(args):
    target = Path(args.target or get_default_dir())
    repo = args.repo or DEFAULT_REPO_URL
    if target.exists():
        print(f"Target directory {target} already exists")
        sys.exit(1)
    run(f"git clone {repo} {target}")
    create_venv(target)
    print("Installation complete.")


def update(args):
    target = Path(args.target or get_default_dir())
    if not target.exists():
        print(f"Target directory {target} does not exist")
        sys.exit(1)
    run("git pull", cwd=target)
    create_venv(target)
    print("Update complete.")


def uninstall(args):
    target = Path(args.target or get_default_dir())
    if not target.exists():
        print(f"Target directory {target} does not exist")
        return
    print(f"Removing {target}")
    shutil.rmtree(target)
    print("Uninstall complete.")


parser = argparse.ArgumentParser(description="Manage SynthMind installation")
sub = parser.add_subparsers(dest="cmd", required=True)

p_install = sub.add_parser("install", help="Install SynthMind")
p_install.add_argument("--repo", help="Git repository URL")
p_install.add_argument("--target", help="Installation directory")
p_install.set_defaults(func=install)

p_update = sub.add_parser("update", help="Update SynthMind")
p_update.add_argument("--target", help="Installation directory")
p_update.set_defaults(func=update)

p_uninstall = sub.add_parser("uninstall", help="Remove SynthMind")
p_uninstall.add_argument("--target", help="Installation directory")
p_uninstall.set_defaults(func=uninstall)

args = parser.parse_args()
args.func(args)
