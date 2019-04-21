from direct.directnotify import DirectNotifyGlobal
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI
from toontown.estate.GardenGlobals import ChangingStatuaryPlot


class DistributedAnimatedStatuaryAI(DistributedStatuaryAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedAnimatedStatuaryAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedStatuaryAI.__init__(self, air, gardenManager, ownerIndex)

        self.occupier = ChangingStatuaryPlot
