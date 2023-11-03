# Docker Images for NeoVim Development Inside a Container

## Images

- **base**: 
  - A foundational image containing NeoVim, tmux, ssh, zsh, Python, NodeJS, and C++ development tools.
  - This image is void of configuration files, allowing volumes to be easily mounted.

- **prebuilt**: 
  - Derived from the `base` image.
  - Preconfigured with settings for NeoVim, tmux, zsh, and other tools.

## Usage

### Using Directly (No Installation Required)

1. Create a folder named `remote` within your project.
2. Add a `docker-compose.yml` file inside the `remote` folder with the following content:

```yaml
version: "3.8"
services:
  remote:
    image: uintuser/remote:base
    tty: true
    privileged: true
    command: /usr/sbin/sshd -D
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 8G
    volumes:
      - type: tmpfs # Optimize I/O operations
        target: /tmp
      - type: tmpfs
        target: /root/.cache/
      - local:/root/.local/
      - cache:/root/.cache/
      - tmux_plugins:/root/.tmux/plugins/
      - ../.:/root/workspace/ # Mount the project's root directory
      - $HOME/.config/nvim:/root/.config/nvim # Mount the configuration files
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

3. Inside the `remote` folder, execute `docker compose up -d` to initialize the container and the ssh server.

4. To access the container:
   - Utilize a shell: `docker compose run remote /bin/zsh`
   - Or, connect via ssh: `ssh root@localhost -p 2222` (password: `root`).
   - For a more comprehensive ssh command with compression and without host key warnings, use:
     - `sshpass -p 'root' ssh -o StrictHostKeyChecking=no -C root@localhost -p 2222 -t 'cd /root/workspace; /bin/zsh' 2>/dev/null`
     - Note: This requires the `sshpass` utility. Install it using your package manager.

### Installation Method

1. Clone this repository.
2. Symlink `remote.py` to a directory within your `$PATH`.
3. Utilize `remote.py` at any project's root directory. This will create a `.remote` folder containing the `docker-compose.yml` file and any configuration files you intend to mount to the container.

Command to initiate:

```bash
remote.py
```

For additional commands and options, use:

```bash
remote.py --help
```
