from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI
from toontown.estate.GardenGlobals import ChangingStatuaryPlot

from datetime import datetime

class DistributedChangingStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedChangingStatuaryAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedStatuaryAI.__init__(self, air, gardenManager, ownerIndex)

        self.growthLevel = None
        self.occupier = ChangingStatuaryPlot

    def d_setGrowthLevel(self, growthLevel):
        self.sendUpdate('setGrowthLevel', [growthLevel])

    def getGrowthLevel(self):
        return self.growthLevel

    def construct(self, gardenData):
        DistributedStatuaryAI.construct(self, gardenData)

        # This needs a timestamp to use to cuase changingstatuary to melt.
        self.growthLevel = 0 # They stay unmelted permenantly for the time being
                    
        #if datetime.now().month in (1, 2, 11, 12):
        #    self.growthLevel = 0
        #else:
        #    self.growthLevel = 0
