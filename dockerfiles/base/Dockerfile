FROM ubuntu:22.04

## =======================
#          Setup
## =======================

ENV DEBIAN_FRONTEND=non-interactive
ENV PATH="/usr/local/bin/:${PATH}"
RUN mkdir /root/.config && mkdir -p /etc/apt/keyrings
SHELL ["/bin/bash","-o","pipefail","-c"]

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    tmux \
    zsh \
    unzip \
    locales \
    kitty-terminfo \
    neofetch \
    ripgrep \
    openssh-server \
    xauth \
    xclip \
    gnupg \
    software-properties-common \
    && locale-gen en_US.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN chsh -s "$(which zsh)"

## =======================
#      Coding Tools
## =======================

# hadolint ignore=DL3008
RUN curl -SLO https://deb.nodesource.com/nsolid_setup_deb.sh && \
    chmod 500 nsolid_setup_deb.sh && \
    ./nsolid_setup_deb.sh 21 && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -f nsolid_setup_deb.sh && \
    rm -rf /var/lib/apt/lists/*

# --- NeoVim
RUN curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage && \
    chmod u+x nvim.appimage && \
    ./nvim.appimage --appimage-extract && \
    ln -s /squashfs-root/AppRun /usr/bin/nvim


# --- Tmux

RUN git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm

## =======================
#     Languages & Deps 
## =======================

# hadolint ignore=DL3008
RUN apt-get update && apt-get install -y --no-install-recommends \
    cmake \
    make \
    clang \
    llvm \
    build-essential \
    clang-tools \
    clang-tidy \
    clang-format \
    && rm -rf /var/lib/apt/lists/*

# --- Python

# hadolint ignore=DL3008
RUN add-apt-repository ppa:deadsnakes/ppa -y \
    && apt-get update \
    && apt-get install -y --no-install-recommends python3.11 python3.10-venv python3-pip \
    && rm -rf /var/lib/apt/lists/*

# --- Rust

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y 



# hadolint ignore=DL3013
RUN pip3 --no-cache-dir install pdm autopep8 pylint

# --- Docker linter

ARG HADOLINT_VERSION=v2.12.0
ADD https://github.com/hadolint/hadolint/releases/download/${HADOLINT_VERSION}/hadolint-Linux-x86_64 /bin/hadolint
RUN chmod +x /bin/hadolint

## =======================
#     Additional Tools
## =======================

# Setup SSH service
RUN mkdir /run/sshd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "root:root" | chpasswd && \
    { \
      echo '#!/bin/bash'; \
      echo '/usr/sbin/sshd -D'; \
    } > /start.sh && chmod +x /start.sh

EXPOSE 22

CMD ["/start.sh"]
