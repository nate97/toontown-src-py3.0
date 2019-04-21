from threading import Thread
import subprocess
import os
import time

###### This is a hacky quick startup script that launches each individual server in a tmux session. ######

class StartServers():

    def __init__(self):
        print ("Starting servers")
        
        self.astron_session = "tmux new -s astron_session"
        self.uberdog_session = "tmux new -s uberdog_session" 
        self.ai_session = "tmux new -s ai_session"

        self.astron_command_00 = "tmux send -t astron_session ./start-astron-cluster.sh ENTER"
        self.uberdog_command_00 = "tmux send -t uberdog_session ./start-uberdog-server.sh ENTER"
        self.uberdog_command_01 = "tmux send -t uberdog_session ENTER"
        self.ai_command_00 = "tmux send -t ai_session ./start-ai-server.sh ENTER"
        self.ai_command_01 = "tmux send -t ai_session ENTER"
        self.ai_command_02 = "tmux send -t ai_session ENTER"

        thread_00 = Thread(target = self.thread00)
        thread_00.start()
        time.sleep(2)
        subprocess.call(self.astron_command_00, shell=True)

        thread_01 = Thread(target = self.thread01)
        thread_01.start()
        time.sleep(2)
        subprocess.call(self.uberdog_command_00, shell=True)
        subprocess.call(self.uberdog_command_01, shell=True)

        thread_02 = Thread(target = self.thread02)
        thread_02.start()
        time.sleep(2)
        subprocess.call(self.ai_command_00, shell=True)
        subprocess.call(self.ai_command_01, shell=True)
        subprocess.call(self.ai_command_02, shell=True)

    def thread00(self):
        subprocess.call(self.astron_session, shell=True)
        return

    def thread01(self):
        subprocess.call(self.uberdog_session, shell=True)
        return

    def thread02(self):
        subprocess.call(self.ai_session, shell=True)
        return

start = StartServers()
