from direct.distributed import DistributedObjectAI


class DistributedGagshopInteriorAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, block, air, zoneId):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = block
        self.zoneId = zoneId

    def getZoneIdAndBlock(self):
        return [self.zoneId, self.block]
