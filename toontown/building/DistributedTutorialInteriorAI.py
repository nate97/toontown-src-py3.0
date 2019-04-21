from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class DistributedTutorialInteriorAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedTutorialInteriorAI')

    def __init__(self, air, block, zoneId, tutorialNpcId):
        DistributedObjectAI.__init__(self, air)

        self.zoneId = zoneId
        self.block = block
        self.tutorialNpcId = tutorialNpcId

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]

    def setTutorialNpcId(self, npcId):
        self.tutorialNpcId = npcId

    def getTutorialNpcId(self):
        return self.tutorialNpcId
