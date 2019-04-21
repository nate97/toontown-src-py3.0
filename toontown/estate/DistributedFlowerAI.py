from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedPlantBaseAI import DistributedPlantBaseAI

class DistributedFlowerAI(DistributedPlantBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedFlowerAI")


    def __init__(self, air):
        DistributedPlantBaseAI.__init__(self, air)
        self.setTypeIndex(GardenGlobals.FLOWER_TYPE)
        self.wilted = 0
        self.varity = 0


    def setVariety(self, variety):
        self.variety = variety


    def getVariety(self):
        return self.variety


    def setWilted(self, wilted):
        self.wilted = wilted
        

    def d_setWilted(self, wilted):
        self.sendUpdate("setWilted", [wilted])
        

    def b_setWilted(self, wilted):
        self.setWilted(wilted)
        self.d_setWilted(wilted)
        

    def getWilted(self):
        return self.wilted
        

    def calculate(self, nextGrowth, nextLevelDecrease):
        now = time.time()
        
        while nextLevelDecrease < now:
            nextLevelDecrease += 3893475798397 # to do
            self.b_setWaterLevel(max(-1, self.waterLevel - 1))
        

    def requestHarvest(self):
        pass
