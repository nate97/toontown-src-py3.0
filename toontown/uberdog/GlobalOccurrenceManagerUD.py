from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD

from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.battle import SuitBattleGlobals
from toontown.suit import SuitDNA


class GlobalOccurrenceManagerUD(DistributedObjectGlobalUD):
    notify = DirectNotifyGlobal.directNotify.newCategory("GlobalOccurrenceManagerUD")


    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        print ("Starting occurence manager...")


    def holidayBegan(self, holidayId):
        message = "Holiday started: " + holidayId
        print (message)


    def invasionBegan(self, msgType, suitType):
        if suitType in SuitDNA.suitHeadTypes:
            suitName = SuitBattleGlobals.SuitAttributes[suitType]['name']
            suitNamePlural = SuitBattleGlobals.SuitAttributes[suitType]['pluralname']
        elif suitType in SuitDNA.suitDepts:
            suitName = SuitDNA.getDeptFullname(suitType)
            suitNamePlural = SuitDNA.getDeptFullnameP(suitType)

        if msgType == ToontownGlobals.SuitInvasionBegin:
            message = TTLocalizer.SuitInvasionBegin2 % suitNamePlural
        elif msgType == ToontownGlobals.SuitInvasionEnd:
            message = TTLocalizer.SuitInvasionEnd1 % suitName
        elif msgType == ToontownGlobals.SkelecogInvasionBegin:
            message = TTLocalizer.SkelecogInvasionBegin3
        elif msgType == ToontownGlobals.SkelecogInvasionEnd:
            message = TTLocalizer.SkelecogInvasionEnd1
        elif msgType == ToontownGlobals.WaiterInvasionBegin:
            message = TTLocalizer.WaiterInvasionBegin2
        elif msgType == ToontownGlobals.WaiterInvasionEnd:
            message = TTLocalizer.WaiterInvasionEnd1
        elif msgType == ToontownGlobals.V2InvasionBegin:
            message = TTLocalizer.V2InvasionBegin3
        elif msgType == ToontownGlobals.V2InvasionEnd:
            message = TTLocalizer.V2InvasionEnd1
        else:
            self.notify.warning('invasionBegan: invalid msgType: %s' % msgType)
            return

        print (message)


    def toonDied(self, toonId):
        def retrieveName(toonName):
            message = toonName + " has gone sad."
            print (message)

        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            toonName = fields['setName'][0]
            retrieveName(toonName)

        self.air.dbInterface.queryObject(self.air.dbId, toonId, handleToon)


    def toonLogin(self, toonId):
        def loginMsg(toonName):
            message = str(toonName) + ' is coming online!'
            print (message)

        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            toonName = fields['setName'][0]
            loginMsg(toonName)

        self.air.dbInterface.queryObject(self.air.dbId, toonId, handleToon)


    def toonLogout(self, toonId):
        def logoutMsg(toonName):
            message = str(toonName) + ' has logged out.'
            print (message)

        def handleToon(dclass, fields):
            if dclass != self.air.dclassesByName['DistributedToonUD']:
                return
            toonName = fields['setName'][0]
            logoutMsg(toonName)

        self.air.dbInterface.queryObject(self.air.dbId, toonId, handleToon)



