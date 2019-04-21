from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed.DistributedObjectAI import DistributedObjectAI

from toontown.toonbase.TTLocalizer import RemoveTrophy

MAX_LISTING = 10

AV_ID_INDEX = 0
NAME_INDEX = 1
SCORE_INDEX = 2


class DistributedTrophyMgrAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedTrophyMgrAI')

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)

        # Load the leaderboard backup for this shard:
        self.leaderInfo, self.trophyScores = simbase.backups.load(
            'trophy-mgr', (simbase.air.districtId,), default=(([], [], []), {}))

    def requestTrophyScore(self):
        avId = self.air.getAvatarIdFromSender()
        av = self.air.doId2do.get(avId)
        if av is not None:
            av.d_setTrophyScore(self.trophyScores.get(avId, 0))

    def addTrophy(self, avId, name, numFloors):
        if avId not in self.trophyScores:
            self.trophyScores[avId] = 0
        trophyScore = self.trophyScores[avId] + numFloors
        self.updateTrophyScore(avId, trophyScore)

    def removeTrophy(self, avId, numFloors):
        if avId in self.trophyScores:
            trophyScore = self.trophyScores[avId] - numFloors
            self.updateTrophyScore(avId, trophyScore)
            if avId in self.air.doId2do:
                # Let the avatar know the building was taken over.
                self.air.doId2do[avId].d_setSystemMessage(0, RemoveTrophy)

    def updateTrophyScore(self, avId, trophyScore):
        av = self.air.doId2do.get(avId)

        if trophyScore <= 0:
            # Take the player off the listing:
            if avId in self.trophyScores:
                del self.trophyScores[avId]
            if avId in self.leaderInfo[AV_ID_INDEX]:
                scoreIndex = self.leaderInfo[AV_ID_INDEX].index(avId)
                del self.leaderInfo[AV_ID_INDEX][scoreIndex]
                del self.leaderInfo[NAME_INDEX][scoreIndex]
                del self.leaderInfo[SCORE_INDEX][scoreIndex]
        else:
            # Add the player to the listing if they haven't been. Otherwise,
            # update their current trophy score:
            self.trophyScores[avId] = trophyScore
            if avId not in self.leaderInfo[AV_ID_INDEX]:
                if av is None:
                    return
                self.leaderInfo[AV_ID_INDEX].append(avId)
                self.leaderInfo[NAME_INDEX].append(av.getName())
                self.leaderInfo[SCORE_INDEX].append(trophyScore)
            else:
                scoreIndex = self.leaderInfo[AV_ID_INDEX].index(avId)
                self.leaderInfo[SCORE_INDEX][scoreIndex] = trophyScore

        # Truncate and reorganize the listing:
        self.reorganize()

        # Update the listing in the various Toon HQs:
        messenger.send('leaderboardChanged')
        messenger.send('leaderboardFlush')

        if av is not None:
            av.d_setTrophyScore(trophyScore)

        simbase.backups.save('trophy-mgr', (simbase.air.districtId,),
                             (self.leaderInfo, self.trophyScores))

    def reorganize(self):
        # Sort the leader info:
        leaderInfo = zip(*reversed(self.leaderInfo))
        leaderInfo.sort(reverse=True)

        # Construct the new, truncated leader info:
        self.leaderInfo = [[], [], []]
        for trophyScore, name, avId in leaderInfo[:MAX_LISTING]:
            self.leaderInfo[AV_ID_INDEX].append(avId)
            self.leaderInfo[NAME_INDEX].append(name)
            self.leaderInfo[SCORE_INDEX].append(trophyScore)

    def getLeaderInfo(self):
        return self.leaderInfo
