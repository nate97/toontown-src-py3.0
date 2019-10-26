from direct.distributed.PyDatagram import *
from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
import toontown.minigame.MinigameCreatorAI

import urllib.parse


if simbase.config.GetBool('want-rpc-server', False):
    from toontown.rpc.ToontownRPCServer import ToontownRPCServer
    from toontown.rpc.ToontownRPCHandler import ToontownRPCHandler

if simbase.config.GetBool('want-mongo-client', True):
    import pymongo

if simbase.config.GetBool('want-discord-server', False):
    from toontown.uberdog.UberdogDiscord import discordWrapper 
    from multiprocessing import Process


class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        if simbase.config.GetBool('want-mongo-client', True):
            url = simbase.config.GetString('mongodb-url', 'mongodb://localhost')
            replicaset = simbase.config.GetString('mongodb-replicaset', '')
            if replicaset:
                self.mongo = pymongo.MongoClient(url, replicaset=replicaset)
            else:
                self.mongo = pymongo.MongoClient(url)
            db = (urllib.parse.urlparse(url).path or '/test')[1:]
            self.mongodb = self.mongo[db]

        self.notify.setInfo(True)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if simbase.config.GetBool('want-rpc-server', False):
            endpoint = simbase.config.GetString('rpc-server-endpoint', 'http://localhost:8080/')
            self.rpcServer = ToontownRPCServer(endpoint, ToontownRPCHandler(self))
            self.rpcServer.start(useTaskChain=True)

        self.createGlobals()
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER, 'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER, 'ChatAgent')

        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTI_FRIENDS_MANAGER, 'TTIFriendsManager')

        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')

        self.deliveryManager = simbase.air.generateGlobalObject(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')

        #if simbase.config.GetBool('want-occurrence-manager-server', False):
        self.globalOccurrenceMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_OCCURRENCE_MANAGER, 'GlobalOccurrenceManager') # OCCURRENCE-MANAGER-UB

        if simbase.config.GetBool('want-discord-server', False):
            self.initDiscordBot() # DISCORD-SERVER

    #### DISCORD-SERVER ####
    def initDiscordBot(self):
        self.discordServerBot = discordWrapper()
        discordBotThread = Process(target=self.discordServerBot.createDiscordBot, args=())
        discordBotThread.start()
    #### DISCORD-SERVER ####



