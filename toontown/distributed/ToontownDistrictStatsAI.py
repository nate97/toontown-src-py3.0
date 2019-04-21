from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectAI import DistributedObjectAI


class ToontownDistrictStatsAI(DistributedObjectAI):
    notify = directNotify.newCategory('ToontownDistrictStatsAI')

    districtId = 0
    avatarCount = 0
    newAvatarCount = 0

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)

        # We want to handle shard status queries so that a ShardStatusReceiver
        # being created after we're generated will know where we're at:
        self.air.netMessenger.accept('queryShardStatus', self, self.handleShardStatusQuery)

    def handleShardStatusQuery(self):
        # Send a shard status update containing our population:
        status = {'population': self.avatarCount}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

    def settoontownDistrictId(self, districtId):
        self.districtId = districtId

    def d_settoontownDistrictId(self, districtId):
        self.sendUpdate('settoontownDistrictId', [districtId])

    def b_settoontownDistrictId(self, districtId):
        self.settoontownDistrictId(districtId)
        self.d_settoontownDistrictId(districtId)

    def gettoontownDistrictId(self):
        return self.districtId

    def setAvatarCount(self, avatarCount):
        self.avatarCount = avatarCount

        # Send a shard status update containing our population:
        status = {'population': self.avatarCount}
        self.air.netMessenger.send('shardStatus', [self.air.ourChannel, status])

    def d_setAvatarCount(self, avatarCount):
        self.sendUpdate('setAvatarCount', [avatarCount])

    def b_setAvatarCount(self, avatarCount):
        self.d_setAvatarCount(avatarCount)
        self.setAvatarCount(avatarCount)

    def getAvatarCount(self):
        return self.avatarCount

    def setNewAvatarCount(self, newAvatarCount):
        self.newAvatarCount = newAvatarCount

    def d_setNewAvatarCount(self, newAvatarCount):
        self.sendUpdate('setNewAvatarCount', [newAvatarCount])

    def b_setNewAvatarCount(self, newAvatarCount):
        self.setNewAvatarCount(newAvatarCount)
        self.d_setNewAvatarCount(newAvatarCount)

    def getNewAvatarCount(self):
        return self.newAvatarCount
