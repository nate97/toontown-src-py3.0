from direct.distributed.DistributedNodeAI import DistributedNodeAI

from toontown.estate import GardenGlobals


class DistributedLawnDecorAI(DistributedNodeAI):
    notify = directNotify.newCategory('DistributedLawnDecorAI')

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedNodeAI.__init__(self, air)

        self.gardenManager = gardenManager
        self.ownerIndex = ownerIndex

        self.plotIndex = None
        self.plotType = None

        self.pos = None
        self.heading = None

        self.movie = None

    def getPlot(self):
        return self.plotIndex

    def setHeading(self, heading):
        self.heading = heading

    def getHeading(self):
        return self.heading

    def setPosition(self, pos):
        self.pos = pos

    def getPosition(self):
        return self.pos

    def getOwnerIndex(self):
        return self.ownerIndex

    def plotEntered(self):
        pass

    def removeItem(self):
        self.setMovie(GardenGlobals.MOVIE_REMOVE, self.air.getAvatarIdFromSender())
        self.gardenManager.revertToPlot(self.plotIndex)

    def setMovie(self, movie, avId):
        self.movie = movie
        self.sendUpdate('setMovie', [movie, avId])

    def movieDone(self):
        self.setMovie(GardenGlobals.MOVIE_CLEAR, self.air.getAvatarIdFromSender())

    def interactionDenied(self, avId):
        self.sendUpdate('interactionDenied', [avId])

    def construct(self, gardenData, gType = 0):
        self.plotIndex = gardenData[1]
        self.plotType = GardenGlobals.getPlotType(self.ownerIndex, self.plotIndex)
        self.pos = GardenGlobals.getPlotPos(self.ownerIndex, self.plotIndex)
        self.heading = GardenGlobals.getPlotHeading(self.ownerIndex, self.plotIndex)

    def pack(self, gardenData):
        pass


