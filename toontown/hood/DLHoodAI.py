from toontown.classicchars import DistributedDonaldAI
from toontown.classicchars import DistributedFrankenDonaldAI
from toontown.classicchars import DistributedGoofySpeedwayAI
from toontown.hood import HoodAI
from toontown.safezone import DistributedTrolleyAI
from toontown.toonbase import ToontownGlobals
from toontown.ai import DistributedResistanceEmoteMgrAI


class DLHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.DonaldsDreamland,
                               ToontownGlobals.DonaldsDreamland)

        self.trolley = None
        self.classicChar = None

        self.startup()


    def startup(self):
        HoodAI.HoodAI.startup(self)

        if simbase.config.GetBool('want-minigames', True):
            self.createTrolley()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dreamland', True):
                self.createClassicChar()
        
        self.resistanceEmoteManager = DistributedResistanceEmoteMgrAI.DistributedResistanceEmoteMgrAI(self.air)
        self.resistanceEmoteManager.generateWithRequired(9720)
        

    def createTrolley(self):
        self.trolley = DistributedTrolleyAI.DistributedTrolleyAI(self.air)
        self.trolley.generateWithRequired(self.zoneId)
        self.trolley.start()


    def createClassicChar(self):
        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES):
            self.classicChar = DistributedFrankenDonaldAI.DistributedFrankenDonaldAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.HALLOWEEN_COSTUMES) # We're using holidayIDs as costume IDs.

        elif simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.APRIL_FOOLS_COSTUMES):
            self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
            self.classicChar.setCurrentCostume(ToontownGlobals.APRIL_FOOLS_COSTUMES) # We're using holidayIDs as costume IDs.

        else:
            self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
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



