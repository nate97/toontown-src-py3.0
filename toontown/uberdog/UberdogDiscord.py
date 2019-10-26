from multiprocessing import Queue
from threading import Thread
from gevent import monkey

import logging

monkey.patch_all()

from disco.client import Client, ClientConfig
from disco.bot import Bot, BotConfig, Plugin
from disco.util.logging import setup_logging


CHANNELID = '507399415036903424'
QUE = Queue() # Global variable for passing data in and out of our processes


class discordBot():

    def createBot(self):
        # Create the base configuration object
        config = ClientConfig.from_file('/home/nathan/PYTHON/WORKING-USE-THIS!!!/src-3.0/config/discordconfig.json')

        # Setup logging based on the configured level
        setup_logging(level=getattr(logging, config.log_level.upper()))

        # Build our client object
        self.client = Client(config)

        # If applicable, build the bot and load plugins
        bot_config = BotConfig(config.bot)
        self.bot = Bot(self.client, bot_config)
        #self.bot.add_plugin(TutPlugin, config) # This is how we would add plugins, TugPlugin would be a class

        self.apiClient = self.bot.client.api
        self.startMainBotLoop()

        (self.bot or self.client).run_forever()


    def startMainBotLoop(self):
        thread = Thread(target=self.botLoop, args=())
        thread.setDaemon(True)
        thread.start()


    def botLoop(self):
        while True:
            try:
                message = QUE.get_nowait()
            except:
                message = None

            if message:
                self.sendMessage(message)


    def sendMessage(self, msg):
        self.apiClient.channels_messages_create(CHANNELID, msg, None, False, None, [], None, False)



class discordWrapper():
    def __init__(self):
        pass

    def createDiscordBot(self):
        discoBot = discordBot()
        discoBot.createBot()


    def logIn(self, message):
        message = '**' + str(message) + " is coming online!" + '**'
        self.putQueMessage(message)


    def logOut(self, message):
        message = '**' + str(message) + " has logged out." + '**'
        self.putQueMessage(message)


    def putQueMessage(self, message):
        QUE.put(message)



