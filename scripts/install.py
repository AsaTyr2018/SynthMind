#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/yourusername/SynthMind.git"
DEFAULT_INSTALL_DIR_LINUX = Path("/opt/SynthMind")


def run(cmd, cwd=None):
    print(f"[RUN] {cmd}")
    subprocess.check_call(cmd, shell=True, cwd=cwd)


def venv_bin(venv: Path, name: str) -> Path:
    if platform.system() == "Windows":
        return venv / "Scripts" / name
    return venv / "bin" / name


def ensure_dir(path: Path):
    if not path.exists():
        try:
            path.mkdir(parents=True)
        except PermissionError:
            if platform.system() != "Windows":
                run(f"sudo mkdir -p {path}")
            else:
                raise
    if not os.access(path, os.W_OK):
        if platform.system() != "Windows":
            run(f"sudo chown -R {os.getuid()}:{os.getgid()} {path}")
        else:
            raise PermissionError(f"Write access to {path} denied")


def create_venv(target: Path):
    venv_dir = target / "venv"
    if not venv_dir.exists():
        run(f"{sys.executable} -m venv {venv_dir}")
    pip = venv_bin(venv_dir, "pip")
    run(f"{pip} install --upgrade pip")
    run(f"{pip} install gradio transformers diffusers huggingface_hub")


def get_default_dir() -> Path:
    if platform.system() == "Windows":
        dest = input("Installation directory [e.g. C:\\SynthMind]: ")
        return Path(dest).expanduser()
    return DEFAULT_INSTALL_DIR_LINUX


def install(args):
    target = Path(args.target or get_default_dir())
    if target.exists():
        print(f"Target directory {target} already exists")
        sys.exit(1)
    ensure_dir(target.parent)
    run(f"git clone {REPO_URL} {target}")
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
    if platform.system() != "Windows":
        run(f"sudo rm -rf {target}")
    else:
        shutil.rmtree(target)
    print("Uninstall complete.")


parser = argparse.ArgumentParser(description="Install or manage SynthMind")
sub = parser.add_subparsers(dest="cmd", required=True)

p_install = sub.add_parser("install", help="Install SynthMind")
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
