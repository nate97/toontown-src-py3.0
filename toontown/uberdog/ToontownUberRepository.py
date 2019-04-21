from direct.distributed.PyDatagram import *
import urlparse

from otp.distributed.DistributedDirectoryAI import DistributedDirectoryAI
from otp.distributed.OtpDoGlobals import *
from toontown.distributed.ToontownInternalRepository import ToontownInternalRepository
import toontown.minigame.MinigameCreatorAI


if config.GetBool('want-rpc-server', False):
    from toontown.rpc.ToontownRPCServer import ToontownRPCServer
    from toontown.rpc.ToontownRPCHandler import ToontownRPCHandler

if config.GetBool('want-mongo-client', False):
    import pymongo


class ToontownUberRepository(ToontownInternalRepository):
    def __init__(self, baseChannel, serverId):
        ToontownInternalRepository.__init__(self, baseChannel, serverId, dcSuffix='UD')

        if config.GetBool('want-mongo-client', False):
            url = config.GetString('mongodb-url', 'mongodb://localhost')
            replicaset = config.GetString('mongodb-replicaset', '')
            if replicaset:
                self.mongo = pymongo.MongoClient(url, replicaset=replicaset)
            else:
                self.mongo = pymongo.MongoClient(url)
            db = (urlparse.urlparse(url).path or '/test')[1:]
            self.mongodb = self.mongo[db]

        self.notify.setInfo(True)

    def handleConnected(self):
        rootObj = DistributedDirectoryAI(self)
        rootObj.generateWithRequiredAndId(self.getGameDoId(), 0, 0)

        if config.GetBool('want-rpc-server', False):
            endpoint = config.GetString('rpc-server-endpoint', 'http://localhost:8080/')
            self.rpcServer = ToontownRPCServer(endpoint, ToontownRPCHandler(self))
            self.rpcServer.start(useTaskChain=True)

        self.createGlobals()
        self.notify.info('Done.')

    def createGlobals(self):
        """
        Create "global" objects.
        """

        self.csm = simbase.air.generateGlobalObject(OTP_DO_ID_CLIENT_SERVICES_MANAGER,
                                                    'ClientServicesManager')

        self.chatAgent = simbase.air.generateGlobalObject(OTP_DO_ID_CHAT_MANAGER,
                                                          'ChatAgent')

        self.friendsManager = simbase.air.generateGlobalObject(OTP_DO_ID_TTI_FRIENDS_MANAGER,
                                                               'TTIFriendsManager')

        self.globalPartyMgr = simbase.air.generateGlobalObject(OTP_DO_ID_GLOBAL_PARTY_MANAGER, 'GlobalPartyManager')

        self.deliveryManager = simbase.air.generateGlobalObject(OTP_DO_ID_TOONTOWN_DELIVERY_MANAGER, 'DistributedDeliveryManager')
