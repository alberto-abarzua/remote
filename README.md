# Docker images for NeoVim development inside a container


## Images

- `base`: Base image with NeoVim, tmux, ssh, zsh, Python, NodeJS, and C++ development tools, this image has no config files so volumes can be mounted to it.

- `prebuilt`: Image based on `base` with my config files for NeoVim, tmux, zsh and other tools.

## Usage


### Simple way no isntallation needed
Simplest way is to just create a folder inside your project named `remote` and add a `docker-compose.yml` file with the following content:

```yaml

version: "3.8"
services:
  remote:
    image: uintuser/remote:base
    tty: true
    privileged: true
    command: /usr/sbin/sshd -D
    deploy: # Resource constraints
      resources:
        limits:
          cpus: "4"
          memory: 8G
    volumes:
      - type: tmpfs # Use tmpfs for I/O-intensive ops
        target: /tmp
      - type: tmpfs
        target: /root/.cache/
      - local:/root/.local/
      - cache:/root/.cache/
      - tmux_plugins:/root/.tmux/plugins/
        # Workspace folder
      - ../.:/root/workspace/
        # Your config files add or remove as needed
      - $HOME/.config/nvim:/root/.config/nvim
      - $HOME/.config/github-copilot/:/root/.config/github-copilot/
      - $HOME/.zshrc:/root/.zshrc
      - $HOME/.p10k.zsh:/root/.p10k.zsh
      - $HOME/.tmux.conf:/root/.tmux.conf
      - $HOME/.gitconfig:/root/.gitconfig
    ports:
      - "2222:22"
volumes:
  local:
  tmux_plugins:
  cache:

```
Then in the `remote` folder run `docker compose up -d` to start the container and the ssh server.

To connect to the container you can run a shell using 
- `docker compose run remote /bin/zsh` 
or connect to the container using ssh

- `ssh root@localhost -p 2222` the password is `root`.

A more complete ssh command, with compression and no warnings about the host key, would be:

- `sshpass -p 'root' ssh -o StrictHostKeyChecking=no -C root@localhost -p 2222 -t 'cd /root/workspace; /bin/zsh' 2>/dev/null")`

This requires sshpass to be installed. (Use your package manager to install it)


### Install the script

The best way to use this is to clone this repo and symlink `remote.py` to a folder in your `$PATH` and then use `remote.py` to start the container.


Now you can run remote.py at the root of any project and create a `.remote` folder with the `docker-compose.yml` file and the config files you want to mount to the container.

```bash
remote.py
```
The script also has other options that can be viewed using `remote.py --help`


