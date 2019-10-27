#!/bin/bash

tmux new-session -d -s astron 'bash start-astron-cluster.sh'
tmux new-session -d -s uberdog 'yes "" | bash start-uberdog-server.sh'
tmux new-session -d -s ai 'yes "" | bash start-ai-server.sh'

echo "Game server has successfully started..."

OUTPUT="$(hostname -I)" && echo "Server IP: ${OUTPUT}  Service port: 7199"

read -p "Press [Enter] key to exit..."
