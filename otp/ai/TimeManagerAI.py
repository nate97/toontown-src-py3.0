from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
import time

class TimeManagerAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("TimeManagerAI")

    def requestServerTime(self, context):
        self.sendUpdateToAvatarId(self.air.getAvatarIdFromSender(),
                                  'serverTime', [context,
                                                 globalClockDelta.getRealNetworkTime(bits=32),
                                                 int(time.time())])

    def setDisconnectReason(self, reason):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('disconnect-reason', avId, reason)

    def setExceptionInfo(self, exception):
        avId = self.air.getAvatarIdFromSender()
        self.air.writeServerEvent('client-exception', avId, exception)



