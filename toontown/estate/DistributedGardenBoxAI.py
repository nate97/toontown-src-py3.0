from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals

class DistributedGardenBoxAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenBoxAI")

    def setTypeIndex(self, index):
        self.typeIndex = index

    def getTypeIndex(self):
        return self.typeIndex

    def construct(self, gardenData):
        self.plotIndex = gardenData[1]
        self.pos = (gardenData[2], gardenData[3], 0)
        self.heading = gardenData[4]
        self.typeIndex = gardenData[5]




