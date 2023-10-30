#!/usr/bin/env python3

import socket
import os
import argparse
import shutil
from pathlib import Path
import subprocess
import yaml

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
FILE_PATH = Path(FILE_PATH)


def create_override_file(ssh_port: int):
    workspace_path = str(Path.cwd())
    remote_dir = get_remote_dir()
    dict_file = {
        "version": "3.8",
        "services": {
            "remote": {
                "ports": [f"{ssh_port}:22"],
                "volumes": [f"{workspace_path}:/workspace"],
            }
        },
    }
    with open(remote_dir / "docker-compose.override.yml", "w") as f:
        yaml.dump(dict_file, f)


def get_available_port_for_ssh():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def get_remote_dir():
    cwd = Path.cwd()
    remote_dir = cwd / ".remote"
    if not remote_dir.exists():
        remote_dir.mkdir()
        shutil.copy(FILE_PATH / "docker-compose.yml", remote_dir / "docker-compose.yml")

    return remote_dir


def is_docker_compose_running(target_port: int):
    try:
        remote_dir = get_remote_dir()
        output = subprocess.check_output(["docker-compose", "ps"], cwd=remote_dir).decode().strip()
        lines = output.split("\n")
        for line in lines[2:]:  # Skip the header lines
            if str(target_port) in line and "Up" in line:
                return True
        return False
    except subprocess.CalledProcessError:
        return False


def get_port_from_current_override_file():
    try:
        remote_dir = get_remote_dir()
        with open(remote_dir / "docker-compose.override.yml", "r") as f:
            dict_file = yaml.load(f, Loader=yaml.FullLoader)
        port = dict_file["services"]["remote"]["ports"][0].split(":")[0]
        return port
    except:
        return None


def run_docker_compose():
    remote_dir = get_remote_dir()
    subprocess.run(["docker-compose", '-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', "up", "-d"],
                   cwd=remote_dir
                   )


def down_docker_compose():
    remote_dir = get_remote_dir()
    subprocess.run(["docker-compose", '-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', "down"],
                   cwd=remote_dir
                   )


def run_compose_command(command: str):
    remote_dir = get_remote_dir()
    subprocess.run(["docker-compose", '-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', command],
                   cwd=remote_dir
                   )


def run_ssh(port: int):
    target_dir = '/root/workspace'
    os.system(
        f"sshpass -p 'root' ssh -o StrictHostKeyChecking=no -C root@localhost -p {port} -t 'cd {target_dir}; /bin/zsh' 2>/dev/null")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remote environment handler")
    parser.add_argument("--down", "-d", action="store_true", help="Stop the remote environment")
    parser.add_argument("--up", "-u", action="store_true", help="Start the remote environment")
    parser.add_argument("--command", "-c", type=str, help="Run a command in the remote environment")

    args = parser.parse_args()

    remote_dir = get_remote_dir()

    if args.down:
        subprocess.run(["docker-compose", '-f', 'docker-compose.yml', '-f', 'docker-compose.override.yml', "down"],
                       cwd=remote_dir
                       )
        exit(0)

    if args.up:
        create_override_file(get_available_port_for_ssh())
        run_docker_compose()
        exit(0)

    if args.command:
        run_compose_command(args.command)
        exit(0)
    existing_port = get_port_from_current_override_file()
    running = False
    if existing_port:
        running = is_docker_compose_running(existing_port)

    print("Running: ", running)
    if running:
        print("Remote environment is already running")
        port = get_port_from_current_override_file()
        run_ssh(port)
    else:
        available_port = get_available_port_for_ssh()
        create_override_file(available_port)
        run_docker_compose()
        run_ssh(available_port)
