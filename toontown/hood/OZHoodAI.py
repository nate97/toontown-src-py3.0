from toontown.hood import HoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI
from toontown.classicchars import DistributedPoliceChipAI
from toontown.classicchars import DistributedJailbirdDaleAI
from toontown.dna.DNAParser import DNAGroup, DNAVisGroup
from toontown.safezone.DistributedPicnicBasketAI import DistributedPicnicBasketAI
from toontown.safezone import DistributedGameTableAI
from toontown.hood import ZoneUtil


class OZHoodAI(HoodAI.HoodAI):
    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air,
                               ToontownGlobals.OutdoorZone,
                               ToontownGlobals.OutdoorZone)

        self.timer = None
        self.classicCharChip = None
        self.classicCharDale = None
        self.picnicTables = []
        self.gameTables = []

        self.startup()

    def startup(self):
        HoodAI.HoodAI.startup(self)

        self.createTimer()
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-chip-and-dale', True):
                self.createClassicChar()
        self.createPicnicTables()
        if simbase.config.GetBool('want-game-tables', True):
            self.createGameTables()

    def createTimer(self):
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.zoneId)

    def createClassicChar(self):
        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES):
            self.classicCharChip = DistributedPoliceChipAI.DistributedPoliceChipAI(self.air)
            self.classicCharChip.setCurrentCostume(ToontownGlobals.HALLOWEEN_COSTUMES) # We're using holidayIDs as costume IDs.
        else:
            self.classicCharChip = DistributedChipAI.DistributedChipAI(self.air)
            self.classicCharChip.setCurrentCostume(ToontownGlobals.NO_COSTUMES) # We're using holidayIDs as costume IDs.

        self.classicCharChip.generateWithRequired(self.zoneId)
        self.classicCharChip.start()
        

        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES):
            self.classicCharDale = DistributedJailbirdDaleAI.DistributedJailbirdDaleAI(self.air, self.classicCharChip.doId)
            self.classicCharDale.setCurrentCostume(ToontownGlobals.HALLOWEEN_COSTUMES) # We're using holidayIDs as costume IDs.
        else:
            self.classicCharDale = DistributedDaleAI.DistributedDaleAI(self.air, self.classicCharChip.doId)
            self.classicCharDale.setCurrentCostume(ToontownGlobals.NO_COSTUMES) # We're using holidayIDs as costume IDs.

        self.classicCharDale.generateWithRequired(self.zoneId)
        self.classicCharDale.start()
        self.classicCharChip.setDaleId(self.classicCharDale.doId)


    def swapOutClassicChar(self):
        destNodeChip = self.classicCharChip.walk.getDestNode()
        destNodeDale = self.classicCharDale.followChip.getDestNode()

        self.classicCharChip.requestDelete()
        self.classicCharDale.requestDelete()

        self.createClassicChar()

        self.classicCharChip.walk.setCurNode(destNodeChip)
        self.classicCharDale.followChip.setCurNode(destNodeDale)

        self.classicCharChip.fsm.request('Walk')
        self.classicCharDale.fsm.request('Walk')

        self.classicCharChip.fadeAway()
        self.classicCharDale.fadeAway()


    def findPicnicTables(self, dnaGroup, zoneId, area, overrideDNAZone=False):
        picnicTables = []
        if isinstance(dnaGroup, DNAGroup) and ('picnic_table' in dnaGroup.getName()):
            nameInfo = dnaGroup.getName().split('_')
            for i in xrange(dnaGroup.getNumChildren()):
                childDnaGroup = dnaGroup.at(i)
                if 'picnic_table' in childDnaGroup.getName():
                    pos = childDnaGroup.getPos()
                    hpr = childDnaGroup.getHpr()
                    picnicTable = DistributedPicnicBasketAI(
                        simbase.air, nameInfo[2],
                        pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    picnicTable.generateWithRequired(zoneId)
                    picnicTables.append(picnicTable)
        elif isinstance(dnaGroup, DNAVisGroup) and (not overrideDNAZone):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            foundPicnicTables = self.findPicnicTables(
                dnaGroup.at(i), zoneId, area, overrideDNAZone=overrideDNAZone)
            picnicTables.extend(foundPicnicTables)
        return picnicTables

    def createPicnicTables(self):
        self.picnicTables = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundPicnicTables = self.findPicnicTables(
                    dnaData, zoneId, area, overrideDNAZone=True)
                self.picnicTables.extend(foundPicnicTables)
        for picnicTable in self.picnicTables:
            picnicTable.start()

    def findGameTables(self, dnaGroup, zoneId, area, overrideDNAZone=False):
        gameTables = []
        if isinstance(dnaGroup, DNAGroup) and ('game_table' in dnaGroup.getName()):
            for i in xrange(dnaGroup.getNumChildren()):
                childDnaGroup = dnaGroup.at(i)
                if 'game_table' in childDnaGroup.getName():
                    pos = childDnaGroup.getPos()
                    hpr = childDnaGroup.getHpr()
                    gameTable = DistributedGameTableAI.DistributedGameTableAI(simbase.air)
                    gameTable.setPosHpr(pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                    gameTable.generateWithRequired(zoneId)
        elif isinstance(dnaGroup, DNAVisGroup) and (not overrideDNAZone):
            zoneId = ZoneUtil.getTrueZoneId(int(dnaGroup.getName().split(':')[0]), zoneId)
        for i in xrange(dnaGroup.getNumChildren()):
            foundGameTables = self.findGameTables(
                dnaGroup.at(i), zoneId, area, overrideDNAZone=overrideDNAZone)
            gameTables.extend(foundGameTables)
        return gameTables

    def createGameTables(self):
        self.gameTables = []
        for zoneId in self.getZoneTable():
            dnaData = self.air.dnaDataMap.get(zoneId, None)
            zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
            if dnaData.getName() == 'root':
                area = ZoneUtil.getCanonicalZoneId(zoneId)
                foundGameTables = self.findGameTables(
                    dnaData, zoneId, area, overrideDNAZone=True)
                self.gameTables.extend(foundGameTables)



