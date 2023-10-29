#!/usr/bin/env python3

from pathlib import Path
import argparse
import subprocess
import os

CURRENT_DIR = Path(__file__).parent.absolute()


def build_image(folder_name, docker_repo):
    dockerfile_dir = str(CURRENT_DIR / "dockerfiles" / folder_name)
    image_tag = f"{docker_repo}:{folder_name}"
    subprocess.run(["docker", "build", "-t", image_tag, dockerfile_dir])


def push_image(folder_name, docker_repo):
    image_tag = f"{docker_repo}:{folder_name}"
    subprocess.run(["docker", "push", image_tag])


def build_all(docker_repo):
    dockerfiles_dir = CURRENT_DIR / "dockerfiles"
    for folder in os.listdir(dockerfiles_dir):
        if os.path.isdir(dockerfiles_dir / folder):
            build_image(folder, docker_repo)


def push_all(docker_repo):
    dockerfiles_dir = CURRENT_DIR / "dockerfiles"
    for folder in os.listdir(dockerfiles_dir):
        if os.path.isdir(dockerfiles_dir / folder):
            push_image(folder, docker_repo)


def main():
    parser = argparse.ArgumentParser(description="Docker image builder and pusher")
    subparsers = parser.add_subparsers(dest="action")

    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("folder", type=str, help="Name of the folder containing the Dockerfile")

    push_parser = subparsers.add_parser("push")
    push_parser.add_argument("folder", type=str, help="Name of the folder containing the Dockerfile")

    subparsers.add_parser("build-all")

    subparsers.add_parser("push-all")

    args = parser.parse_args()

    docker_repo = "uintuser/remote"

    if args.action == "build":
        build_image(args.folder, docker_repo)
    elif args.action == "push":
        push_image(args.folder, docker_repo)
    elif args.action == "build-all":
        build_all(docker_repo)
    elif args.action == "push-all":
        push_all(docker_repo)


if __name__ == "__main__":
    main()
