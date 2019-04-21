from otp.ai.AIBase import *
from toontown.toonbase import ToontownGlobals
from direct.distributed.ClockDelta import *
from ElevatorConstants import *
from direct.distributed import DistributedObjectAI
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
from direct.directnotify import DirectNotifyGlobal

class DistributedElevatorAI(DistributedObjectAI.DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedElevatorAI')

    def __init__(self, air, bldg, numSeats = 4, antiShuffle = 0, minLaff = 0):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.type = ELEVATOR_NORMAL
        self.countdownTime = ElevatorData[self.type]['countdown']
        self.bldg = bldg
        self.bldgDoId = bldg.getDoId()
        self.seats = []
        self.setAntiShuffle(antiShuffle)
        self.setMinLaff(minLaff)
        if self.antiShuffle:
            if not hasattr(simbase.air, 'elevatorTripId'):
                simbase.air.elevatorTripId = 1
            self.elevatorTripId = simbase.air.elevatorTripId
            simbase.air.elevatorTripId += 1
        else:
            self.elevatorTripId = 0
        for seat in xrange(numSeats):
            self.seats.append(None)

        self.accepting = 0
        self.fsm = ClassicFSM.ClassicFSM('DistributedElevatorAI', [State.State('off', self.enterOff, self.exitOff, ['opening', 'closed']),
         State.State('opening', self.enterOpening, self.exitOpening, ['waitEmpty', 'waitCountdown']),
         State.State('waitEmpty', self.enterWaitEmpty, self.exitWaitEmpty, ['waitCountdown']),
         State.State('waitCountdown', self.enterWaitCountdown, self.exitWaitCountdown, ['waitEmpty', 'allAboard']),
         State.State('allAboard', self.enterAllAboard, self.exitAllAboard, ['closing', 'waitEmpty', 'waitCountdown']),
         State.State('closing', self.enterClosing, self.exitClosing, ['closed', 'waitEmpty']),
         State.State('closed', self.enterClosed, self.exitClosed, ['opening'])], 'off', 'off')
        self.fsm.enterInitialState()
        self.boardingParty = None
        return

    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        del self.bldg
        self.ignoreAll()
        DistributedObjectAI.DistributedObjectAI.delete(self)

    def setBoardingParty(self, party):
        self.boardingParty = party

    def generate(self):
        self.start()
        DistributedObjectAI.DistributedObjectAI.generate(self)

    def getBldgDoId(self):
        return self.bldgDoId

    def findAvailableSeat(self):
        for i in xrange(len(self.seats)):
            if self.seats[i] == None:
                return i

    def findAvatar(self, avId):
        for i in xrange(len(self.seats)):
            if self.seats[i] == avId:
                return i

    def countFullSeats(self):
        avCounter = 0
        for i in self.seats:
            if i:
                avCounter += 1
        return avCounter

    def countOpenSeats(self):
        openSeats = 0
        for i in xrange(len(self.seats)):
            if self.seats[i] is None:
                openSeats += 1
        return openSeats

    def rejectingBoardersHandler(self, avId, reason = 0, wantBoardingShow = 0):
        self.rejectBoarder(avId, reason)

    def rejectBoarder(self, avId, reason = 0):
        self.sendUpdateToAvatarId(avId, 'rejectBoard', [avId, reason])

    def acceptingBoardersHandler(self, avId, reason = 0, wantBoardingShow = 0):
        self.notify.debug('acceptingBoardersHandler')
        seatIndex = self.findAvailableSeat()
        if seatIndex == None:
            self.rejectBoarder(avId, REJECT_NOSEAT)
        else:
            self.acceptBoarder(avId, seatIndex, wantBoardingShow)
        return

    def acceptBoarder(self, avId, seatIndex, wantBoardingShow = 0):
        self.notify.debug('acceptBoarder')
        if self.findAvatar(avId) != None:
            return
        self.seats[seatIndex] = avId
        self.timeOfBoarding = globalClock.getRealTime()
        if wantBoardingShow:
            self.timeOfGroupBoarding = globalClock.getRealTime()
        self.sendUpdate('fillSlot' + str(seatIndex), [avId, wantBoardingShow])
        if self.fsm.getCurrentState().getName() == 'waitEmpty':
            self.fsm.request('waitCountdown')
        elif self.fsm.getCurrentState().getName() == 'waitCountdown' and self.findAvailableSeat() is None:
            self.fsm.request('allAboard')
        return

    def rejectingExitersHandler(self, avId):
        self.rejectExiter(avId)

    def rejectExiter(self, avId):
        pass

    def acceptingExitersHandler(self, avId):
        self.acceptExiter(avId)

    def clearEmptyNow(self, seatIndex):
        self.sendUpdate('emptySlot' + str(seatIndex), [0,
         0,
         globalClockDelta.getRealNetworkTime(),
         0])

    def clearFullNow(self, seatIndex):
        avId = self.seats[seatIndex]
        if avId == None:
            self.notify.warning('Clearing an empty seat index: ' + str(seatIndex) + ' ... Strange...')
        else:
            self.seats[seatIndex] = None
            self.sendUpdate('fillSlot' + str(seatIndex), [0, 0])
            self.ignore(self.air.getAvatarExitEvent(avId))
        return

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def getState(self):
        return self.fsm.getCurrentState().getName()

    def avIsOKToBoard(self, av):
        return av.hp > self.minLaff and self.accepting

    def checkBoard(self, av):
        if av.hp < self.minLaff:
            return REJECT_MINLAFF
        return 0

    def requestBoard(self, *args):
        self.notify.debug('requestBoard')
        avId = self.air.getAvatarIdFromSender()
        if self.findAvatar(avId) != None:
            self.notify.warning('Ignoring multiple requests from %s to board.' % avId)
            return
        av = self.air.doId2do.get(avId)
        if av:
            boardResponse = self.checkBoard(av)
            newArgs = (avId,) + args + (boardResponse,)
            if self.boardingParty and self.boardingParty.hasActiveGroup(avId) and self.boardingParty.getGroupLeader(avId) != avId:
                self.notify.warning('Rejecting %s from boarding the elevator because he is already part of a Boarding Group.' % avId)
                self.rejectingBoardersHandler(*newArgs)
                return
            if boardResponse == 0:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning('avid: %s does not exist, but tried to board an elevator' % avId)
        return

    def partyAvatarBoard(self, avatar, wantBoardingShow = 0):
        av = avatar
        avId = avatar.doId
        if self.findAvatar(avId) != None:
            self.notify.warning('Ignoring multiple requests from %s to board.' % avId)
            return
        if av:
            boardResponse = self.checkBoard(av)
            newArgs = (avId,) + (boardResponse,) + (wantBoardingShow,)
            if boardResponse == 0:
                self.acceptingBoardersHandler(*newArgs)
            else:
                self.rejectingBoardersHandler(*newArgs)
        else:
            self.notify.warning('avid: %s does not exist, but tried to board an elevator' % avId)
        return

    def requestExit(self, *args):
        self.notify.debug('requestExit')
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av:
            newArgs = (avId,) + args
            if self.accepting:
                self.acceptingExitersHandler(*newArgs)
            else:
                self.rejectingExitersHandler(*newArgs)
        else:
            self.notify.warning('avId: %s does not exist, but tried to exit an elevator' % avId)

    def start(self):
        self.open()

    def enterOff(self):
        self.accepting = 0
        self.timeOfBoarding = None
        self.timeOfGroupBoarding = None
        if hasattr(self, 'doId'):
            for seatIndex in xrange(len(self.seats)):
                taskMgr.remove(self.uniqueName('clearEmpty-' + str(seatIndex)))

        return

    def exitOff(self):
        self.accepting = 0

    def open(self):
        self.fsm.request('opening')

    def enterOpening(self):
        self.d_setState('opening')
        self.accepting = 0
        for seat in self.seats:
            seat = None

    def exitOpening(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('opening-timer'))

    def enterWaitCountdown(self):
        self.d_setState('waitCountdown')
        self.accepting = 1

    def exitWaitCountdown(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('countdown-timer'))
        self.newTrip()

    def enterAllAboard(self):
        self.accepting = 0

    def exitAllAboard(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('waitForAllAboard'))

    def enterClosing(self):
        self.d_setState('closing')
        self.accepting = 0

    def exitClosing(self):
        self.accepting = 0
        taskMgr.remove(self.uniqueName('closing-timer'))

    def enterClosed(self):
        self.d_setState('closed')

    def exitClosed(self):
        pass

    def enterWaitEmpty(self):
        self.d_setState('waitEmpty')
        self.accepting = 1

    def exitWaitEmpty(self):
        self.accepting = 0

    def setElevatorTripId(self, id):
        self.elevatorTripId = id

    def getElevatorTripId(self):
        return self.elevatorTripId

    def newTrip(self):
        if self.antiShuffle:
            self.elevatorTripId = simbase.air.elevatorTripId
            if simbase.air.elevatorTripId > 2100000000:
                simbase.air.elevatorTripId = 1
            simbase.air.elevatorTripId += 1
            self.sendUpdate('setElevatorTripId', [self.elevatorTripId])

    def setAntiShuffle(self, antiShuffle):
        self.antiShuffle = antiShuffle

    def getAntiShuffle(self):
        return self.antiShuffle

    def setMinLaff(self, minLaff):
        self.minLaff = minLaff

    def getMinLaff(self):
        return self.minLaff
