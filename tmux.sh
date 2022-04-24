#!/bin/sh

DEVENV="~/.venvs/django/bin/activate"

if test -n $TMUX; then
  SESSION=$(tmux display-message -p '#S')
  # Name first Pane and start zsh
  tmux rename-window -t 1 'Main'

  # Check if docker is running
  docker info || \
    # If not, start docker daemon
    tmux send-keys -t 'Main' 'sudo systemctl start docker' C-m
  # Check if psql container is running
  docker-compose ps --status running | grep persefone-db || \
    # If not, start the container
    tmux send-keys -t 'Main' 'docker-compose up db' C-m

  tmux split-window -t 'Main'
  tmux send-keys -t$SESSION:1.2 ". $DEVENV" C-m "source .env" C-m "python manage.py runserver" C-m

  tmux new-window -t$SESSION:2 -n 'neovim'
  tmux send-keys -t 'neovim' ". $DEVENV" C-m "nvim" C-m

  tmux new-window -t$SESSION:3 -n 'jupyterlab'
  tmux send-keys -t 'jupyterlab' ". $DEVENV" C-m "source .env" C-m "python manage.py shell_plus --lab" C-m

  tmux select-window -t$SESSION:2
fi
