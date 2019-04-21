@echo off
cd ..

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<PPYTHON_PATH

rem Get the user input:
set /P ttiUsername="Username: "
set /P ttiPassword="Password: "
set /P TTI_GAMESERVER="Gameserver (DEFAULT: 167.114.28.238): " || ^
set TTI_GAMESERVER=167.114.28.238

echo ===============================
echo Starting Toontown Online...
echo ppython: %PPYTHON_PATH%
echo Username: %ttiUsername%
echo Gameserver: %TTI_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ClientStartRemoteDB
pause
