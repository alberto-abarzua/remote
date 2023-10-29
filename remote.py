#!/usr/bin/env python3
import os
import argparse
from pathlib import Path
import yaml

CONFIG_DIR = Path.home() / '.config' / 'remote'

DOCKER_COMPOSE_FILE = os.path.join(CONFIG_DIR, 'main.yml')
DOCKER_COMPOSE_WORKSPACE_FILE = os.path.join(CONFIG_DIR, 'workspace.override.yml')
DOCKER_COMPOSE_SETTINGS_FILE = os.path.join(CONFIG_DIR, 'settings.yml')


def create_override_file(file_path):
    data = {
        'version': '3.8',
        'services': {
            'remote': {
                'volumes': [f"{file_path}:/root/workspace/"]
            }
        }
    }

    with open(DOCKER_COMPOSE_WORKSPACE_FILE, 'w') as f:
        yaml.dump(data, f)


def run_docker_compose():
    cmd = f'docker-compose -f {DOCKER_COMPOSE_FILE} -f {DOCKER_COMPOSE_WORKSPACE_FILE} -f {DOCKER_COMPOSE_SETTINGS_FILE} run --rm --service-ports remote /bin/zsh -c "cd /root/workspace && exec /bin/zsh"'
    print(cmd)
    os.system(cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create workspace.override.yml file and run docker-compose.')
    parser.add_argument('file_path', nargs='?', default=os.getcwd(), type=Path, help='File path to be mounted.')

    args = parser.parse_args()
    print(args.file_path)

    create_override_file(args.file_path)
    run_docker_compose()
