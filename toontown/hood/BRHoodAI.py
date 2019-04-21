from toontown.classicchars import DistributedPlutoAI
from toontown.classicchars import DistributedWesternPlutoAI
from toontown.classicchars import DistributedMinnieAI
from toontown.hood import HoodAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedPolarPlaceEffectMgrAI


class BRHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.TheBrrrgh,
                               ToontownGlobals.TheBrrrgh)

        self.trolley = None
        self.classicChar = None

        self.startup()


    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-pluto', True):
                self.createClassicChar()

        self.PolarPlaceEffectManager = DistributedPolarPlaceEffectMgrAI.DistributedPolarPlaceEffectMgrAI(self.air)
        self.PolarPlaceEffectManager.generateWithRequired(3821)
        

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()


    def createClassicChar(self):
        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES):
            self.classicChar = DistributedWesternPlutoAI.DistributedWesternPlutoAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.HALLOWEEN_COSTUMES) # We're using holidayIDs as costume IDs.

        elif simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.APRIL_FOOLS_COSTUMES):
            self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.APRIL_FOOLS_COSTUMES) # We're using holidayIDs as costume IDs.

        else:
            self.classicChar = DistributedPlutoAI.DistributedPlutoAI(self.air)
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



