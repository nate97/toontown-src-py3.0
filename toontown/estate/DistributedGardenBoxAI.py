from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedGardenBoxAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedGardenBoxAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.typeIndex = None
        self.occupier = GardenGlobals.PlanterBox

    def setTypeIndex(self, index):
        self.index = index

    def getTypeIndex(self):
        return self.typeIndex

    def constructBox(self, boxIndex, boxType, x, y, header):

        self.setTypeIndex(boxType)
        DistributedLawnDecorAI.constructBox(self, boxIndex, boxType, x, y, header)
