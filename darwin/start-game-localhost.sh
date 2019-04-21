#!/bin/sh
cd ..

export DYLD_LIBRARY_PATH=`pwd`/Libraries.bundle
export DYLD_FRAMEWORK_PATH="Frameworks"

# Get the user input:
read -p "Username: " ttiUsername

# Export the environment variables:
export ttiUsername=$ttiUsername
export ttiPassword="password"
export TTI_PLAYCOOKIE=$ttiUsername
export TTI_GAMESERVER="127.0.0.1"

echo "==============================="
echo "Starting Toontown Online..."
echo "Username: $ttiUsername"
echo "Gameserver: $TTI_GAMESERVER"
echo "==============================="

ppython -m toontown.toonbase.ClientStart
