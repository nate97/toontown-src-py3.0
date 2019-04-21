from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from otp.avatar import DistributedAvatarAI
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase import ToontownGlobals

class DistributedCCharBaseAI(DistributedAvatarAI.DistributedAvatarAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedCCharBaseAI')

    def __init__(self, air, name):
        DistributedAvatarAI.DistributedAvatarAI.__init__(self, air)
        self.setName(name)
        self.exitOff()
        self.diffPath = None
        self.currentCostume = 0

    def delete(self):
        self.ignoreAll()
        DistributedAvatarAI.DistributedAvatarAI.delete(self)


    def exitOff(self):
        self._DistributedCCharBaseAI__initAttentionSpan()
        self._DistributedCCharBaseAI__clearNearbyAvatars()


    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('adding avatar ' + str(avId) + ' to the nearby avatar list')
        if avId not in self.nearbyAvatars:
            self.nearbyAvatars.append(avId)
        else:
            self.air.writeServerEvent('suspicious', avId, 'CCharBase.avatarEnter')
            self.notify.warning('Avatar %s already in nearby avatars!' % avId)
        self.nearbyAvatarInfoDict[avId] = { }
        self.nearbyAvatarInfoDict[avId]['enterTime'] = globalClock.getRealTime()
        self.nearbyAvatarInfoDict[avId]['lastChatTime'] = 0
        self.sortNearbyAvatars()
        self._DistributedCCharBaseAI__interestingAvatarEventOccured()
        avExitEvent = self.air.getAvatarExitEvent(avId)
        self.acceptOnce(avExitEvent, self._DistributedCCharBaseAI__handleExitedAvatar, [
            avId])
        self.avatarEnterNextState()


    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        self._DistributedCCharBaseAI__doAvatarExit(avId)


    def _DistributedCCharBaseAI__doAvatarExit(self, avId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('removing avatar ' + str(avId) + ' from the nearby avatar list')
        if avId not in self.nearbyAvatars:
            self.notify.debug('avatar ' + str(avId) + ' not in the nearby avatar list')
        else:
            avExitEvent = self.air.getAvatarExitEvent(avId)
            self.ignore(avExitEvent)
            del self.nearbyAvatarInfoDict[avId]
            self.nearbyAvatars.remove(avId)
            self.avatarExitNextState()


    def avatarEnterNextState():
        pass


    def avatarExitNextState():
        pass


    def _DistributedCCharBaseAI__clearNearbyAvatars(self):
        self.nearbyAvatars = []
        self.nearbyAvatarInfoDict = { }


    def sortNearbyAvatars(self):

        def nAv_compare(a, b, nAvIDict = self.nearbyAvatarInfoDict):
            tsA = nAvIDict[a]['enterTime']
            tsB = nAvIDict[b]['enterTime']
            if tsA == tsB:
                return 0
            elif tsA < tsB:
                return -1
            else:
                return 1

        self.nearbyAvatars.sort(nAv_compare)


    def getNearbyAvatars(self):
        return self.nearbyAvatars


    def _DistributedCCharBaseAI__avatarSpoke(self, avId):
        now = globalClock.getRealTime()
        if avId in self.nearbyAvatarInfoDict:
            self.nearbyAvatarInfoDict[avId]['lastChatTime'] = now
            self._DistributedCCharBaseAI__interestingAvatarEventOccured()



    def _DistributedCCharBaseAI__initAttentionSpan(self):
        self._DistributedCCharBaseAI__avatarTimeoutBase = 0


    def _DistributedCCharBaseAI__interestingAvatarEventOccured(self, t = None):
        if t == None:
            t = globalClock.getRealTime()

        self._DistributedCCharBaseAI__avatarTimeoutBase = t


    def lostInterest(self):
        now = globalClock.getRealTime()
        if now > self._DistributedCCharBaseAI__avatarTimeoutBase + 50.0:
            return 1

        return 0


    def _DistributedCCharBaseAI__handleExitedAvatar(self, avId):
        self._DistributedCCharBaseAI__doAvatarExit(avId)


    def setNearbyAvatarChat(self, msg):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setNearbyAvatarChat: avatar ' + str(avId) + ' said ' + str(msg))
        self._DistributedCCharBaseAI__avatarSpoke(avId)


    def setNearbyAvatarSC(self, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setNearbyAvatarSC: avatar %s said SpeedChat phrase %s' % (avId, msgIndex))
        self._DistributedCCharBaseAI__avatarSpoke(avId)


    def setNearbyAvatarSCCustom(self, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setNearbyAvatarSCCustom: avatar %s said custom SpeedChat phrase %s' % (avId, msgIndex))
        self._DistributedCCharBaseAI__avatarSpoke(avId)


    def setNearbyAvatarSCToontask(self, taskId, toNpcId, toonProgress, msgIndex):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setNearbyAvatarSCToontask: avatar %s said %s' % (avId, (taskId, toNpcId, toonProgress, msgIndex)))
        self._DistributedCCharBaseAI__avatarSpoke(avId)


    def getWalk(self):
        return ('', '', 0)


    def walkSpeed(self):
        return 0.10000000000000001

    # I Think this is missing halloween.
    def handleHolidays(self):
        self.CCChatter = 0
        if hasattr(simbase.air, 'holidayManager'):
            if ToontownGlobals.CRASHED_LEADERBOARD in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.CRASHED_LEADERBOARD
            elif ToontownGlobals.CIRCUIT_RACING_EVENT in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.CIRCUIT_RACING_EVENT
            elif ToontownGlobals.WINTER_CAROLING in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WINTER_CAROLING
            elif ToontownGlobals.WINTER_DECORATIONS in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WINTER_DECORATIONS
            elif ToontownGlobals.WACKY_WINTER_CAROLING in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WACKY_WINTER_CAROLING
            elif ToontownGlobals.WACKY_WINTER_DECORATIONS in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.WACKY_WINTER_DECORATIONS
            elif ToontownGlobals.VALENTINES_DAY in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.VALENTINES_DAY
            elif ToontownGlobals.APRIL_FOOLS_COSTUMES in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.APRIL_FOOLS_COSTUMES
            elif ToontownGlobals.SILLY_CHATTER_ONE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_ONE
            elif ToontownGlobals.SILLY_CHATTER_TWO in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_TWO
            elif ToontownGlobals.SILLY_CHATTER_THREE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_THREE
            elif ToontownGlobals.SILLY_CHATTER_FOUR in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.SILLY_CHATTER_FIVE in simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SILLY_CHATTER_FOUR
            elif ToontownGlobals.HALLOWEEN_COSTUMES in  simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.HALLOWEEN_COSTUMES
            elif ToontownGlobals.SPOOKY_COSTUMES in  simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SPOOKY_COSTUMES
            elif ToontownGlobals.SELLBOT_FIELD_OFFICE in  simbase.air.holidayManager.currentHolidays:
                self.CCChatter = ToontownGlobals.SELLBOT_FIELD_OFFICE


    def getCCLocation(self):
        return 0


    def getCCChatter(self):
        self.handleHolidays()
        return self.CCChatter


    def findHood(self):
        wantedZoneId = self.zoneId
        for hood in self.air.hoods:
            zoneId = hood.zoneId
            if zoneId == wantedZoneId:
                return hood


    def fadeAway(self):
        self.sendUpdate('fadeAway', [])


    def setCurrentCostume(self, costume):
        self.currentCostume = costume


    def handleCostumes(self):
        if self.fsm.getCurrentState().getName() == 'Walk': # We don't want todo anything while the character is moving...
            return

        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES): # HALLOWEEN is running
            if self.currentCostume != ToontownGlobals.HALLOWEEN_COSTUMES:
                hood = self.findHood()
                hood.swapOutClassicChar()

        elif simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.APRIL_FOOLS_COSTUMES): # APRIL FOOLS is running
            if self.currentCostume != ToontownGlobals.APRIL_FOOLS_COSTUMES:
                hood = self.findHood()
                hood.swapOutClassicChar()

        else: # No costume holiday running, check to see if they still have costumes!
            if self.currentCostume != ToontownGlobals.NO_COSTUMES: # The costume is not default... RESET CHARACTER TO NO COSTUME
                hood = self.findHood()
                hood.swapOutClassicChar()
                self.setCurrentCostume(1) # Purpose of this is so that we don't constantly regenerate the character


    def handleHalloweenCostumeEnter(self):
        if self.fsm.getCurrentState().getName() == 'Walk': # We don't want todo anything while the character is moving...
            return

        if simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES): # HALLOWEEN is running
            hood = self.findHood()
            hood.swapOutClassicChar()


    def handleHalloweenCostumeExit(self):
        if self.fsm.getCurrentState().getName() == 'Walk': # We don't want todo anything while the character is moving...
            return

        if not simbase.air.holidayManager.isHolidayRunning(ToontownGlobals.HALLOWEEN_COSTUMES): # HALLOWEEN is NOT running
            hood = self.findHood()
            hood.swapOutClassicChar()


