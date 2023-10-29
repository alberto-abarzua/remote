FROM uintuser/remote:base

RUN git clone https://github.com/alberto-abarzua/dotfiles.git /root/dotfiles

# Change to the repository directory
WORKDIR /root/dotfiles

# Run install.py
RUN python3 install.py --force

CMD ["/bin/zsh"]
