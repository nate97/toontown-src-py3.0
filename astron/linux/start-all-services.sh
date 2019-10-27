#!/bin/bash

tmux new-session -d -s astron 'bash start-astron-cluster.sh'
tmux new-session -d -s uberdog 'yes "" | bash start-uberdog-server.sh'
tmux new-session -d -s ai 'yes "" | bash start-ai-server.sh'

read -p "Press [Enter] key to exit..."
