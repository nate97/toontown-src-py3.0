#!/bin/sh
cd ..

# Get the user input:
read -p "Username: " ttiUsername
read -p "Gameserver (DEFAULT:  disguisedpenguin.onmypc.net): " TTI_GAMESERVER
TTI_GAMESERVER=${TTI_GAMESERVER:-"disguisedpenguin.onmypc.net"}

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword="password"
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER=$TTI_GAMESERVER

echo "==============================="
echo "Starting Toontown Online..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStart
