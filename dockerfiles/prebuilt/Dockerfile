FROM ubuntu:latest

## =======================
#          Setup
## =======================

ENV DEBIAN_FRONTEND=non-interactive
ENV NVM_DIR=/root/.nvm
ENV PATH="/usr/local/bin/:${PATH}"

RUN apt-get update \
    && apt-get install -y \
    curl \
    git \
    tmux \
    zsh \
    unzip \
    locales \
    kitty-terminfo \
    neofetch \
    software-properties-common

RUN chsh -s $(which zsh)

# Locale and encoding
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8


## =======================
#      Coding Tools
## =======================

RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
RUN chmod u+x nvim.appimage
RUN ./nvim.appimage --appimage-extract
RUN ln -s /squashfs-root/AppRun /usr/bin/nvim

# --- Tmux

RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

## =======================
#     Languages & Deps 
## =======================

RUN apt-get install -y \
    cmake \
    make \
    clang \
    llvm \
    build-essential \
    clang-tools

# --- NodeJS

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash \
    && . "$NVM_DIR/nvm.sh" \
    && nvm install node
ENV NVM_DIR /root/.nvm
RUN echo 'export NVM_DIR="/root/.nvm"' >> /etc/zsh/zshenv \
    && echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /etc/zsh/zshenv \
    && echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /etc/zsh/zshenv
ENV PATH="/root/.nvm/versions/node/v16.13.0/bin/:${PATH}"

# --- Python
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y python3.11 \
    python3.10-venv \
    python3-pip

RUN pip3 install pdm

# Clone the dotfiles repository
RUN git clone https://github.com/alberto-abarzua/dotfiles.git /root/dotfiles

# Change to the repository directory
WORKDIR /root/dotfiles

# Run install.py
RUN python3 install.py

CMD ["/bin/zsh"]
