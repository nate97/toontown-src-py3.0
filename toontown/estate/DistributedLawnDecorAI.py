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

    def setPlot(self, plotIndex):
        self.plotIndex = plotIndex

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

    def setOwnerIndex(self, ownerIndex):
        self.ownerIndex = ownerIndex

    def getOwnerIndex(self):
        return self.ownerIndex

    def plotEntered(self):
        pass

    def removeItem(self):
        self.setMovie(GardenGlobals.MOVIE_REMOVE, self.air.getAvatarIdFromSender())
        self.gardenManager.revertToPlot(self.plotIndex)

    def setMovie(self, movie, avId):
        if not self.gardenManager.house.avatarId == avId:
            self.notify.warning('Avatar %s tried to access a garden that is not theirs!' % avId)
            self.sendUpdate('interactionDenied', [avId])
            return
        self.movie = movie
        self.sendUpdate('setMovie', [movie, avId])

    def movieDone(self):
        self.setMovie(GardenGlobals.MOVIE_CLEAR, self.air.getAvatarIdFromSender())

    def interactionDenied(self, avId):
        self.sendUpdate('interactionDenied', [avId])

    def construct(self, gardenData):
        self.plotIndex = gardenData.getUint8()

        self.plotType = GardenGlobals.getPlotType(self.ownerIndex, self.plotIndex)
        self.pos = GardenGlobals.getPlotPos(self.ownerIndex, self.plotIndex)
        self.heading = GardenGlobals.getPlotHeading(self.ownerIndex, self.plotIndex)

    def constructBox(self, boxIndex, boxType, x, y, header):
        self.boxIndex = boxIndex
        self.boxType = boxType
        self.pos = (x, y, 0)
        self.heading = header


    def pack(self, gardenData):
        gardenData.addUint8(self.plotIndex)
