from toontown.classicchars import DistributedDaisyAI
from toontown.classicchars import DistributedSockHopDaisyAI
from toontown.classicchars import DistributedMickeyAI
from toontown.hood import HoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone import DistributedButterflyAI
from toontown.safezone import DistributedDGFlowerAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedGreenToonEffectMgrAI


class DGHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DaisyGardens,
                               ToontownGlobals.DaisyGardens)

        self.trolley = None
        self.flower = None
        self.classicChar = None
        self.butterflies = []

        self.startup()


    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        self.createFlower()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-daisy', True):
                self.createClassicChar()
        if simbase.config.GetBool('want-butterflies', True):
            self.createButterflies()
            
        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.IDES_OF_MARCH):
            self.startupGreenToonManager()


    def shutdown(self):
        HoodAI.HoodAI.shutdown(self)
        ButterflyGlobals.clearIndexes(self.zoneId)


    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()


    def createFlower(self):
        self.flower = DistributedDGFlowerAI.DistributedDGFlowerAI(self.air)
        self.flower.generateWithRequired(self.zoneId)
        self.flower.start()


    def createClassicChar(self, test = None):
        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES):
            self.classicChar = DistributedSockHopDaisyAI.DistributedSockHopDaisyAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.HALLOWEEN_COSTUMES) # We're using holidayIDs as costume IDs.

        elif simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.APRIL_FOOLS_COSTUMES):
            self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.APRIL_FOOLS_COSTUMES) # We're using holidayIDs as costume IDs.

        else:
            self.classicChar = DistributedDaisyAI.DistributedDaisyAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.NO_COSTUMES) # We're using holidayIDs as costume IDs.

        self.classicChar.generateWithRequired(self.zoneId)
        self.classicChar.start()


    def swapOutClassicChar(self):
        destNode = self.classicChar.walk.getDestNode()
        self.classicChar.requestDelete()

        self.createClassicChar()
        self.classicChar.walk.setCurNode(destNode)
        self.classicChar.fsm.request('Walk')
        self.classicChar.fadeAway()


    def createButterflies(self):
        playground = ButterflyGlobals.DG
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI.DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.zoneId)
                self.butterflies.append(butterfly)



