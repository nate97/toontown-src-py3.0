from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectGlobalAI import DistributedObjectGlobalAI

from otp.distributed.OtpDoGlobals import *
from panda3d.core import *


class GlobalOccurrenceManagerAI(DistributedObjectGlobalAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("GlobalOccurrenceManagerAI")

    def announceGenerate(self):
        DistributedObjectGlobalAI.announceGenerate(self)
        print ("Starting occurence manager...")

    def sendHolidayOccurrence(self, holidayId):
        self.sendUpdate('holidayBegan', holidayId)

    def sendInvasionOccurrence(self, msgType, suitType):
        print ("sending invasionType", msgType, suitType)
        self.sendUpdate('invasionBegan', [msgType, suitType])

    def sendDeathOccurrence(self, toonId):
        self.sendUpdate('toonDied', [toonId])



