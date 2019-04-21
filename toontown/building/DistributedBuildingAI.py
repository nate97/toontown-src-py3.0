import random
import time

import DistributedDoorAI
import DistributedElevatorExtAI
import DistributedKnockKnockDoorAI
import DistributedSuitInteriorAI
import DistributedToonHallInteriorAI
import DistributedToonInteriorAI
import DoorTypes
import FADoorCodes
import SuitBuildingGlobals
import SuitPlannerInteriorAI
from direct.distributed import DistributedObjectAI
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.task.Task import Task
from otp.ai.AIBaseGlobal import *
from toontown.cogdominium.CogdoLayout import CogdoLayout
from toontown.cogdominium.DistributedCogdoElevatorExtAI import DistributedCogdoElevatorExtAI
from toontown.cogdominium.DistributedCogdoInteriorAI import DistributedCogdoInteriorAI
from toontown.cogdominium.SuitPlannerCogdoInteriorAI import SuitPlannerCogdoInteriorAI
from toontown.hood import ZoneUtil
from toontown.toonbase.ToontownGlobals import ToonHall


class DistributedBuildingAI(DistributedObjectAI.DistributedObjectAI):
    def __init__(self, air, blockNumber, zoneId, trophyMgr):
        DistributedObjectAI.DistributedObjectAI.__init__(self, air)
        self.block = blockNumber
        self.zoneId = zoneId
        self.canonicalZoneId = ZoneUtil.getCanonicalZoneId(zoneId)
        self.trophyMgr = trophyMgr
        self.victorResponses = None
        self.fsm = ClassicFSM.ClassicFSM(
            'DistributedBuildingAI',
            [
                State.State('off', self.enterOff, self.exitOff,
                            ['waitForVictors', 'becomingToon', 'toon',
                             'clearOutToonInterior', 'becomingSuit', 'suit',
                             'clearOutToonInteriorForCogdo', 'becomingCogdo',
                             'cogdo']),
                State.State('waitForVictors', self.enterWaitForVictors, self.exitWaitForVictors,
                            ['becomingToon']),
                State.State('waitForVictorsFromCogdo', self.enterWaitForVictorsFromCogdo, self.exitWaitForVictorsFromCogdo,
                            ['becomingToonFromCogdo']),
                State.State('becomingToon', self.enterBecomingToon, self.exitBecomingToon,
                            ['toon']),
                State.State('becomingToonFromCogdo', self.enterBecomingToonFromCogdo, self.exitBecomingToonFromCogdo,
                            ['toon']),
                State.State('toon', self.enterToon, self.exitToon,
                            ['clearOutToonInterior', 'clearOutToonInteriorForCogdo']),
                State.State('clearOutToonInterior', self.enterClearOutToonInterior, self.exitClearOutToonInterior,
                            ['becomingSuit']),
                State.State('becomingSuit', self.enterBecomingSuit, self.exitBecomingSuit,
                            ['suit']),
                State.State('suit', self.enterSuit, self.exitSuit,
                            ['waitForVictors', 'becomingToon']),
                State.State('clearOutToonInteriorForCogdo', self.enterClearOutToonInteriorForCogdo, self.exitClearOutToonInteriorForCogdo,
                            ['becomingCogdo']),
                State.State('becomingCogdo', self.enterBecomingCogdo, self.exitBecomingCogdo,
                            ['cogdo']),
                State.State('cogdo', self.enterCogdo, self.exitCogdo,
                            ['waitForVictorsFromCogdo', 'becomingToonFromCogdo'])
            ], 'off', 'off')
        self.fsm.enterInitialState()
        self.track = 'c'
        self.difficulty = 1
        self.numFloors = 0
        self.savedBy = None
        self.becameSuitTime = 0
        self.frontDoorPoint = None
        self.suitPlannerExt = None

    def cleanup(self):
        if self.isDeleted():
            return
        self.fsm.requestFinalState()
        if hasattr(self, 'interior'):
            self.interior.requestDelete()
            del self.interior
        if hasattr(self, 'door'):
            self.door.requestDelete()
            del self.door
            self.insideDoor.requestDelete()
            del self.insideDoor
            self.knockKnock.requestDelete()
            del self.knockKnock
        if hasattr(self, 'elevator'):
            self.elevator.requestDelete()
            del self.elevator
        self.requestDelete()

    def delete(self):
        self.cleanup()
        taskMgr.remove(self.taskName('suitbldg-time-out'))
        taskMgr.remove(self.taskName(str(self.block) + '_becomingToon-timer'))
        taskMgr.remove(self.taskName(str(self.block) + '_becomingSuit-timer'))
        DistributedObjectAI.DistributedObjectAI.delete(self)
        del self.fsm

    def getPickleData(self):
        pickleData = {
            'state': str(self.fsm.getCurrentState().getName()),
            'block': str(self.block),
            'track': str(self.track),
            'difficulty': str(self.difficulty),
            'numFloors': str(self.numFloors),
            'savedBy': self.savedBy,
            'becameSuitTime': self.becameSuitTime
        }
        return pickleData

    def _getMinMaxFloors(self, difficulty):
        return SuitBuildingGlobals.SuitBuildingInfo[difficulty][0]

    def suitTakeOver(self, suitTrack, difficulty, buildingHeight):
        if not self.isToonBlock():
            return
        self.updateSavedBy(None)
        difficulty = min(difficulty, len(SuitBuildingGlobals.SuitBuildingInfo) - 1)
        (minFloors, maxFloors) = self._getMinMaxFloors(difficulty)
        if buildingHeight is None:
            numFloors = random.randint(minFloors, maxFloors)
        else:
            numFloors = buildingHeight + 1
            if (numFloors < minFloors) or (numFloors > maxFloors):
                numFloors = random.randint(minFloors, maxFloors)
        self.track = suitTrack
        self.difficulty = difficulty
        self.numFloors = numFloors
        self.becameSuitTime = time.time()
        self.fsm.request('clearOutToonInterior')

    def cogdoTakeOver(self, difficulty, buildingHeight):
        if not self.isToonBlock():
            return
        self.updateSavedBy(None)
        (minFloors, maxFloors) = self._getMinMaxFloors(difficulty)
        if buildingHeight is None:
            numFloors = random.randint(minFloors, maxFloors)
        else:
            numFloors = buildingHeight + 1
            if (numFloors < minFloors) or (numFloors > maxFloors):
                numFloors = random.randint(minFloors, maxFloors)
        self.track = 'c'
        self.difficulty = difficulty
        self.numFloors = numFloors
        self.becameSuitTime = time.time()
        self.fsm.request('clearOutToonInteriorForCogdo')

    def toonTakeOver(self):
        if 'cogdo' in self.fsm.getCurrentState().getName().lower():
            self.fsm.request('becomingToonFromCogdo')
        else:
            self.fsm.request('becomingToon')
        if self.suitPlannerExt:
            self.suitPlannerExt.recycleBuilding()
        if hasattr(self, 'interior'):
            self.interior.requestDelete()
            del self.interior

    def getFrontDoorPoint(self):
        return self.frontDoorPoint

    def setFrontDoorPoint(self, point):
        self.frontDoorPoint = point

    def getBlock(self):
        (dummy, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        return [self.block, interiorZoneId]

    def getSuitData(self):
        return [ord(self.track), self.difficulty, self.numFloors]

    def getState(self):
        return [self.fsm.getCurrentState().getName(), globalClockDelta.getRealNetworkTime()]

    def setState(self, state, timestamp=0):
        self.fsm.request(state)

    def isSuitBuilding(self):
        state = self.fsm.getCurrentState().getName()
        return state in ('suit', 'becomingSuit', 'clearOutToonInterior')

    def isCogdo(self):
        state = self.fsm.getCurrentState().getName()
        return state in ('cogdo', 'becomingCogdo', 'clearOutToonInteriorForCogdo')

    def isSuitBlock(self):
        return self.isSuitBuilding() or self.isCogdo()

    def isEstablishedSuitBlock(self):
        state = self.fsm.getCurrentState().getName()
        return state == 'suit'

    def isToonBlock(self):
        state = self.fsm.getCurrentState().getName()
        return state in ('toon', 'becomingToon', 'becomingToonFromCogdo')

    def getExteriorAndInteriorZoneId(self):
        blockNumber = self.block
        dnaStore = self.air.dnaStoreMap[self.canonicalZoneId]
        zoneId = dnaStore.getZoneFromBlockNumber(blockNumber)
        zoneId = ZoneUtil.getTrueZoneId(zoneId, self.zoneId)
        interiorZoneId = (zoneId - (zoneId%100)) + 500 + blockNumber
        return (zoneId, interiorZoneId)

    def d_setState(self, state):
        self.sendUpdate('setState', [state, globalClockDelta.getRealNetworkTime()])

    def b_setVictorList(self, victorList):
        self.setVictorList(victorList)
        self.d_setVictorList(victorList)

    def d_setVictorList(self, victorList):
        self.sendUpdate('setVictorList', [victorList])

    def setVictorList(self, victorList):
        self.victorList = victorList

    def findVictorIndex(self, avId):
        for i in xrange(len(self.victorList)):
            if self.victorList[i] == avId:
                return i

    def recordVictorResponse(self, avId):
        index = self.findVictorIndex(avId)
        if index is None:
            self.air.writeServerEvent('suspicious', avId, 'DistributedBuildingAI.setVictorReady from toon not in %s.' % self.victorList)
            return
        self.victorResponses[index] = avId

    def allVictorsResponded(self):
        if self.victorResponses == self.victorList:
            return 1
        else:
            return 0

    def setVictorReady(self):
        avId = self.air.getAvatarIdFromSender()
        if self.victorResponses is None:
            self.air.writeServerEvent('suspicious', avId, 'DistributedBuildingAI.setVictorReady in state %s.' % self.fsm.getCurrentState().getName())
            return
        self.recordVictorResponse(avId)
        event = self.air.getAvatarExitEvent(avId)
        self.ignore(event)
        if self.allVictorsResponded():
            self.toonTakeOver()

    def setVictorExited(self, avId):
        print 'victor %d exited unexpectedly for bldg %d' % (avId, self.doId)
        self.recordVictorResponse(avId)
        if self.allVictorsResponded():
            self.toonTakeOver()

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def getToon(self, toonId):
        if toonId in self.air.doId2do:
            return self.air.doId2do[toonId]
        else:
            self.notify.warning('getToon() - toon: %d not in repository!' % toonId)

    def updateSavedBy(self, savedBy):
        if self.savedBy:
            for (avId, name, dna) in self.savedBy:
                if not ZoneUtil.isWelcomeValley(self.zoneId):
                    self.trophyMgr.removeTrophy(avId, self.numFloors)
        self.savedBy = savedBy
        if self.savedBy:
            for (avId, name, dna) in self.savedBy:
                if not ZoneUtil.isWelcomeValley(self.zoneId):
                    self.trophyMgr.addTrophy(avId, name, self.numFloors)

    def enterWaitForVictors(self, victorList, savedBy):
        activeToons = []
        for t in victorList:
            toon = None
            if t:
                toon = self.getToon(t)
            if toon is not None:
                activeToons.append(toon)
        for t in victorList:
            toon = None
            if t:
                toon = self.getToon(t)
                self.air.writeServerEvent('buildingDefeated', t, '%s|%s|%s|%s' % (self.track, self.numFloors, self.zoneId, victorList))
            if toon is not None:
                self.air.questManager.toonKilledBuilding(toon, self.track, self.difficulty, self.numFloors, self.zoneId, activeToons)
        for i in xrange(0, 4):
            victor = victorList[i]
            if (victor is None) or (victor not in self.air.doId2do):
                victorList[i] = 0
                continue
            event = self.air.getAvatarExitEvent(victor)
            self.accept(event, self.setVictorExited, extraArgs=[victor])
        self.b_setVictorList(victorList)
        self.updateSavedBy(savedBy)
        self.victorResponses = [0, 0, 0, 0]
        self.d_setState('waitForVictors')

    def exitWaitForVictors(self):
        self.victorResponses = None
        for victor in self.victorList:
            event = simbase.air.getAvatarExitEvent(victor)
            self.ignore(event)

    def enterWaitForVictorsFromCogdo(self, victorList, savedBy):
        activeToons = []
        for t in victorList:
            toon = None
            if t:
                toon = self.getToon(t)
            if toon is not None:
                activeToons.append(toon)
        for t in victorList:
            toon = None
            if t:
                toon = self.getToon(t)
                self.air.writeServerEvent('buildingDefeated', t, '%s|%s|%s|%s' % (self.track, self.numFloors, self.zoneId, victorList))
            if toon is not None:
                self.air.questManager.toonKilledCogdo(toon, self.difficulty, self.numFloors, self.zoneId, activeToons)
        for i in xrange(0, 4):
            victor = victorList[i]
            if (victor is None) or (victor not in self.air.doId2do):
                victorList[i] = 0
                continue
            event = self.air.getAvatarExitEvent(victor)
            self.accept(event, self.setVictorExited, extraArgs = [victor])
        self.b_setVictorList(victorList)
        self.updateSavedBy(savedBy)
        self.victorResponses = [0, 0, 0, 0]
        self.d_setState('waitForVictorsFromCogdo')

    def exitWaitForVictorsFromCogdo(self):
        self.victorResponses = None
        for victor in self.victorList:
            event = simbase.air.getAvatarExitEvent(victor)
            self.ignore(event)

    def enterBecomingToon(self):
        self.d_setState('becomingToon')
        name = self.taskName(str(self.block) + '_becomingToon-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.VICTORY_SEQUENCE_TIME, self.becomingToonTask, name)

    def exitBecomingToon(self):
        name = self.taskName(str(self.block) + '_becomingToon-timer')
        taskMgr.remove(name)

    def enterBecomingToonFromCogdo(self):
        self.d_setState('becomingToonFromCogdo')
        name = self.taskName(str(self.block) + '_becomingToonFromCogdo-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.VICTORY_SEQUENCE_TIME, self.becomingToonTask, name)

    def exitBecomingToonFromCogdo(self):
        name = self.taskName(str(self.block) + '_becomingToonFromCogdo-timer')
        taskMgr.remove(name)

    def becomingToonTask(self, task):
        self.fsm.request('toon')
        self.suitPlannerExt.buildingMgr.save()
        return Task.done

    def enterToon(self):
        self.d_setState('toon')
        (exteriorZoneId, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        if simbase.config.GetBool('want-new-toonhall', 1) and ZoneUtil.getCanonicalZoneId(interiorZoneId) == ToonHall:
            self.interior = DistributedToonHallInteriorAI.DistributedToonHallInteriorAI(self.block, self.air, interiorZoneId, self)
        else:
            self.interior = DistributedToonInteriorAI.DistributedToonInteriorAI(self.block, self.air, interiorZoneId, self)
        self.interior.generateWithRequired(interiorZoneId)
        door = self.createExteriorDoor()
        insideDoor = DistributedDoorAI.DistributedDoorAI(self.air, self.block, DoorTypes.INT_STANDARD)
        door.setOtherDoor(insideDoor)
        insideDoor.setOtherDoor(door)
        door.zoneId = exteriorZoneId
        insideDoor.zoneId = interiorZoneId
        door.generateWithRequired(exteriorZoneId)
        insideDoor.generateWithRequired(interiorZoneId)
        self.door = door
        self.insideDoor = insideDoor
        self.becameSuitTime = 0
        self.knockKnock = DistributedKnockKnockDoorAI.DistributedKnockKnockDoorAI(self.air, self.block)
        self.knockKnock.generateWithRequired(exteriorZoneId)
        self.air.writeServerEvent('building-toon', self.doId, '%s|%s' % (self.zoneId, self.block))

    def createExteriorDoor(self):
        result = DistributedDoorAI.DistributedDoorAI(self.air, self.block, DoorTypes.EXT_STANDARD)
        return result

    def exitToon(self):
        self.door.setDoorLock(FADoorCodes.BUILDING_TAKEOVER)

    def enterClearOutToonInterior(self):
        self.d_setState('clearOutToonInterior')
        if hasattr(self, 'interior'):
            self.interior.setState('beingTakenOver')
        name = self.taskName(str(self.block) + '_clearOutToonInterior-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.CLEAR_OUT_TOON_BLDG_TIME, self.clearOutToonInteriorTask, name)

    def exitClearOutToonInterior(self):
        name = self.taskName(str(self.block) + '_clearOutToonInterior-timer')
        taskMgr.remove(name)

    def clearOutToonInteriorTask(self, task):
        self.fsm.request('becomingSuit')
        return Task.done

    def enterBecomingSuit(self):
        self.sendUpdate('setSuitData', [ord(self.track), self.difficulty, self.numFloors])
        self.d_setState('becomingSuit')
        name = self.taskName(str(self.block) + '_becomingSuit-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.TO_SUIT_BLDG_TIME, self.becomingSuitTask, name)

    def exitBecomingSuit(self):
        name = self.taskName(str(self.block) + '_becomingSuit-timer')
        taskMgr.remove(name)
        if hasattr(self, 'interior'):
            self.interior.requestDelete()
            del self.interior
            self.door.requestDelete()
            del self.door
            self.insideDoor.requestDelete()
            del self.insideDoor
            self.knockKnock.requestDelete()
            del self.knockKnock

    def becomingSuitTask(self, task):
        self.fsm.request('suit')
        self.suitPlannerExt.buildingMgr.save()
        return Task.done

    def enterSuit(self):
        self.sendUpdate('setSuitData', [ord(self.track), self.difficulty, self.numFloors])
        (zoneId, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self.planner = SuitPlannerInteriorAI.SuitPlannerInteriorAI(self.numFloors, self.difficulty, self.track, interiorZoneId)
        self.d_setState('suit')
        (exteriorZoneId, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self.elevator = DistributedElevatorExtAI.DistributedElevatorExtAI(self.air, self)
        self.elevator.generateWithRequired(exteriorZoneId)
        self.air.writeServerEvent('building-cog', self.doId, '%s|%s|%s|%s' % (self.zoneId, self.block, self.track, self.numFloors))

    def exitSuit(self):
        del self.planner
        if hasattr(self, 'elevator'):
            self.elevator.requestDelete()
            del self.elevator

    def enterClearOutToonInteriorForCogdo(self):
        self.d_setState('clearOutToonInteriorForCogdo')
        if hasattr(self, 'interior'):
            self.interior.setState('beingTakenOver')
        name = self.taskName(str(self.block) + '_clearOutToonInteriorForCogdo-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.CLEAR_OUT_TOON_BLDG_TIME, self.clearOutToonInteriorForCogdoTask, name)

    def exitClearOutToonInteriorForCogdo(self):
        name = self.taskName(str(self.block) + '_clearOutToonInteriorForCogdo-timer')
        taskMgr.remove(name)

    def clearOutToonInteriorForCogdoTask(self, task):
        self.fsm.request('becomingCogdo')
        return Task.done

    def enterBecomingCogdo(self):
        self.sendUpdate('setSuitData', [ord(self.track), self.difficulty, self.numFloors])
        self.d_setState('becomingCogdo')
        name = self.taskName(str(self.block) + '_becomingCogdo-timer')
        taskMgr.doMethodLater(SuitBuildingGlobals.TO_SUIT_BLDG_TIME, self.becomingCogdoTask, name)

    def exitBecomingCogdo(self):
        name = self.taskName(str(self.block) + '_becomingCogdo-timer')
        taskMgr.remove(name)
        if hasattr(self, 'interior'):
            self.interior.requestDelete()
            del self.interior
            self.door.requestDelete()
            del self.door
            self.insideDoor.requestDelete()
            del self.insideDoor
            self.knockKnock.requestDelete()
            del self.knockKnock

    def becomingCogdoTask(self, task):
        self.fsm.request('cogdo')
        self.suitPlannerExt.buildingMgr.save()
        return Task.done

    def enterCogdo(self):
        self.sendUpdate('setSuitData', [ord(self.track), self.difficulty, self.numFloors])
        (zoneId, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self._cogdoLayout = CogdoLayout(self.numFloors)
        self.planner = SuitPlannerCogdoInteriorAI(self._cogdoLayout, self.difficulty, self.track, interiorZoneId)
        self.d_setState('cogdo')
        (exteriorZoneId, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self.elevator = DistributedCogdoElevatorExtAI(self.air, self)
        self.elevator.generateWithRequired(exteriorZoneId)
        self.air.writeServerEvent('building-cogdo', self.doId, '%s|%s|%s' % (self.zoneId, self.block, self.numFloors))

    def exitCogdo(self):
        del self.planner
        if hasattr(self, 'elevator'):
            self.elevator.requestDelete()
            del self.elevator

    def setSuitPlannerExt(self, planner):
        self.suitPlannerExt = planner

    def _createSuitInterior(self):
        return DistributedSuitInteriorAI.DistributedSuitInteriorAI(self.air, self.elevator)

    def _createCogdoInterior(self):
        return DistributedCogdoInteriorAI(self.air, self.elevator)

    def createSuitInterior(self):
        self.interior = self._createSuitInterior()
        (dummy, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self.interior.fsm.request('WaitForAllToonsInside')
        self.interior.generateWithRequired(interiorZoneId)

    def createCogdoInterior(self):
        self.interior = self._createCogdoInterior()
        (dummy, interiorZoneId) = self.getExteriorAndInteriorZoneId()
        self.interior.fsm.request('WaitForAllToonsInside')
        self.interior.generateWithRequired(interiorZoneId)

    def deleteSuitInterior(self):
        if hasattr(self, 'interior'):
            self.interior.requestDelete()
            del self.interior
        if hasattr(self, 'elevator'):
            self.elevator.d_setFloor(-1)
            self.elevator.open()

    def deleteCogdoInterior(self):
        self.deleteSuitInterior()
