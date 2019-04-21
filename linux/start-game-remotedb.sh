#!/bin/bash
cd ..

# Get the user input:
read -p "Username: " ttiUsername
read -s -p "Password: " ttiPassword
echo
read -p "Gameserver (DEFAULT: 167.114.28.238): " TTI_GAMESERVER
TTI_GAMESERVER=${TTI_GAMESERVER:-"167.114.28.238"}

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword=$ttiPassword
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER=$TTI_GAMESERVER

echo "==============================="
echo "Starting Toontown Online..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

/usr/bin/python2 -m toontown.toonbase.ClientStartRemoteDB
