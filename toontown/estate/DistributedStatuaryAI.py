from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals


class DistributedStatuaryAI(DistributedLawnDecorAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedStatuaryAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.typeIndex = None
        self.occupier = GardenGlobals.StatuaryPlot

    def d_setTypeIndex(self, index):
        self.sendUpdate('setTypeIndex', [index])

    def getTypeIndex(self):
        return self.typeIndex

    def construct(self, gardenData, gType = 0):
        DistributedLawnDecorAI.construct(self, gardenData, gType)

        self.typeIndex = gardenData[2]

    def pack(self, gardenData):
        pass
        #gardenData.addUint8(self.occupier)
        #DistributedLawnDecorAI.pack(self, gardenData)
        #gardenData.addUint8(self.typeIndex)

    def movieDone(self):
        if self.movie == GardenGlobals.MOVIE_REMOVE:
            self.gardenManager.removeFinished(self.plotIndex)
            self.requestDelete()

        DistributedLawnDecorAI.movieDone(self)
