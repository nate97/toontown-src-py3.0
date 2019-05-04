from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM

class DistributedWinterCarolingTargetAI(DistributedObjectAI, FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedWinterCarolingTargetAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'WinterCarolingFSM')
        self.air = air
        
    def enterOff(self):
        self.requestDelete()
        
    def requestScavengerHunt(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is None:
            return
        scavengerHunt = av.getScavengerHunt()
        if self.zoneId in scavengerHunt:
            self.sendUpdateToAvatarId(avId, 'doScavengerHunt', [0])
        else:
            self.sendUpdateToAvatarId(avId, 'doScavengerHunt', [100])
            scavengerHunt.append(self.zoneId)
            av.b_setScavengerHunt(scavengerHunt)
            av.addMoney(100)
        if len(scavengerHunt) == 6:
            av.b_setCheesyEffect(14, 0, 0)

