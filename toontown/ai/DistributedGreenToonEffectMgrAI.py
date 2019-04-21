from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.fsm.FSM import FSM


class DistributedGreenToonEffectMgrAI(DistributedObjectAI, FSM):
    notify = directNotify.newCategory("DistributedGreenToonEffectMgrAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        FSM.__init__(self, 'GreenToonFSM')
        self.air = air

    def enterOff(self):
        self.requestDelete()

    def addGreenToonEffect(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        av.b_setCheesyEffect(15, 0, 0)
