from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class WelcomeValleyManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("WelcomeValleyManagerAI")

    def clientSetZone(self, todo0):
        pass

    def toonSetZone(self, doId, newZoneId):
        pass #TODO
        
    def requestZoneIdMessage(self, origZoneId, context): # Client asks us
        pass

    def requestZoneIdResponse(self, zoneId, context): # Send to client
        pass

