from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedPhaseEventMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedPhaseEventMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.holidayDates = []

    def setNumPhases(self, numPhases):
        self.numPhases = numPhases

    def setDates(self, holidayDates):
        for holidayDate in holidayDates:
            self.holidayDates.append(datetime.datetime(holidayDate[0], holidayDate[1], holidayDate[2], holidayDate[3], holidayDate[4], holidayDate[5]))

    def setCurPhase(self, curPhase):
        self.curPhase = curPhase

    def setIsRunning(self, isRunning):
        self.isRunning = isRunning

