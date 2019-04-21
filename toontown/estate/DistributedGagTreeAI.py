from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI
from toontown.estate import GardenGlobals


class DistributedGagTreeAI(DistributedPlantBaseAI):
    notify = directNotify.newCategory("DistributedGagTreeAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedPlantBaseAI.__init__(self, air, gardenManager, ownerIndex)
        self.occupier = GardenGlobals.TreePlot

        self.wilted = None
        self.gagTrack = None
        self.gagLevel = None

    def d_setWilted(self, wiltedState):
        self.sendUpdate('setWilted', [wiltedState])

    def getWilted(self):
        return self.wilted

    def canHarvest(self):
        return self.getGrowthState() == GardenGlobals.FULL_TREE

    def requestHarvest(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if not av:
            return
        if not self.canHarvest():
            return

        self.growthLevel = self.getGrowthThresholds()[2] - 1

        self.d_setGrowthLevel(self.growthLevel)
        self.gardenManager.updateGardenData()

        self.setMovie(GardenGlobals.MOVIE_HARVEST, avId)

        inventory = av.inventory
        inventory.NPCMaxOutInv(targetTrack=self.gagTrack, maxLevelIndex=self.gagLevel)
        av.b_setInventory(inventory.makeNetString())

    def canGiveOrganic(self):
        state = 0
        for v in self.getGrowthThresholds():
            if self.growthLevel >= v - 1:
                state += 1
        return state == GardenGlobals.FULL_TREE

    def construct(self, gardenData):
        DistributedPlantBaseAI.construct(self, gardenData)

        self.wilted = gardenData.getUint8()
        if self.waterLevel == -1:
            self.wilted = True

        self.gagTrack, self.gagLevel = GardenGlobals.getTreeTrackAndLevel(self.typeIndex)

    def pack(self, gardenData):
        gardenData.addUint8(self.occupier)

        DistributedPlantBaseAI.pack(self, gardenData)

        gardenData.addUint8(self.wilted)

    def movieDone(self):
        if self.movie == GardenGlobals.MOVIE_REMOVE:
            self.gardenManager.removeFinished(self.plotIndex)
            self.requestDelete()
        else:
            DistributedPlantBaseAI.movieDone(self)