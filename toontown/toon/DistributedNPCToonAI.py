from otp.ai.AIBaseGlobal import *
from direct.task.Task import Task
from panda3d.core import *
from DistributedNPCToonBaseAI import *
from toontown.quest import Quests

class DistributedNPCToonAI(DistributedNPCToonBaseAI):
    FourthGagVelvetRopeBan = config.GetBool('want-ban-fourth-gag-velvet-rope', 0)

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonBaseAI.__init__(self, air, npcId, questCallback)
        self.hq = hq
        self.tutorial = 0
        self.pendingAvId = None
        self.task = None
        return

    def getTutorial(self):
        return self.tutorial

    def setTutorial(self, val):
        self.tutorial = val

    def getHq(self):
        return self.hq

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.isBusy():
            self.freeAvatar(avId)
            return
        self.busy = avId
        self.air.questManager.requestInteract(avId, self)
        self.acceptOnce(self.air.getAvatarExitEvent(avId), self.__handleUnexpectedExit, extraArgs=[avId])

        self.clearTasks()
        self.task = self.uniqueName('clearMovie')
        taskMgr.doMethodLater(20, self.sendTimeoutMovie, self.task)
        DistributedNPCToonBaseAI.avatarEnter(self)

    def chooseQuest(self, questId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('chooseQuest: avatar %s choseQuest %s' % (avId, questId))
        if not self.pendingAvId:
            self.notify.warning('chooseQuest: not expecting an answer from any avatar: %s' % avId)
            return
        if self.pendingAvId != avId:
            self.notify.warning('chooseQuest: not expecting an answer from this avatar: %s' % avId)
            return
        if self.pendingQuests is None:
            self.notify.warning('chooseQuest: not expecting a quest choice from this avatar: %s' % avId)
            self.air.writeServerEvent('suspicious', avId, 'unexpected chooseQuest')
            return
        if questId == 0:
            self.pendingAvId = None
            self.pendingQuests = None
            self.air.questManager.avatarCancelled(self)
            self.cancelChoseQuest(avId)
            return
        if questId == 401:
            av = self.air.getDo(avId)
            if not av:
                self.notify.warning('chooseQuest: av not present: %s' % avId)
                return
        for quest in self.pendingQuests:
            if questId == quest[0]:
                self.pendingAvId = None
                self.pendingQuests = None
                self.air.questManager.avatarChoseQuest(avId, self, *quest)
                return
        self.notify.warning('chooseQuest: avatar: %s chose a quest not offered: %s' % (avId, questId))
        self.pendingAvId = None
        self.pendingQuests = None
        return

    def chooseTrack(self, trackId):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('chooseTrack: avatar %s choseTrack %s' % (avId, trackId))
        if not self.pendingAvId:
            self.notify.warning('chooseTrack: not expecting an answer from any avatar: %s' % avId)
            return
        if self.pendingAvId != avId:
            self.notify.warning('chooseTrack: not expecting an answer from this avatar: %s' % avId)
            return
        if self.pendingTracks is None:
            self.notify.warning('chooseTrack: not expecting a track choice from this avatar: %s' % avId)
            self.air.writeServerEvent('suspicious', avId, 'unexpected chooseTrack')
            return
        if trackId == -1:
            self.pendingAvId = None
            self.pendingTracks = None
            self.pendingTrackQuest = None
            self.air.questManager.avatarCancelled(avId)
            self.cancelChoseTrack(avId)
            return
        for track in self.pendingTracks:
            if trackId == track:
                self.air.questManager.avatarChoseTrack(avId, self, self.pendingTrackQuest, trackId)
                self.pendingAvId = None
                self.pendingTracks = None
                self.pendingTrackQuest = None
                return

        self.notify.warning('chooseTrack: avatar: %s chose a track not offered: %s' % (avId, trackId))
        self.pendingAvId = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        return

    def sendTimeoutMovie(self, task):
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIMEOUT,
         self.npcId,
         self.busy,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        self.sendClearMovie(None)
        self.busy = 0
        return Task.done

    def sendClearMovie(self, task):
        self.pendingAvId = None
        self.pendingQuests = None
        self.pendingTracks = None
        self.pendingTrackQuest = None
        self.busy = 0
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_CLEAR,
         self.npcId,
         0,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        return Task.done

    def rejectAvatar(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_REJECT,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.uniqueName('clearMovie'))

    def rejectAvatarTierNotDone(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TIER_NOT_DONE,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(5.5, self.sendClearMovie, self.task)

    def completeQuest(self, avId, questId, rewardId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_COMPLETE,
         self.npcId,
         avId,
         [questId, rewardId, 0],
         ClockDelta.globalClockDelta.getRealNetworkTime(bits=16)])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(540.0, self.sendTimeoutMovie, self.task)

    def incompleteQuest(self, avId, questId, completeStatus, toNpcId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_INCOMPLETE,
         self.npcId,
         avId,
         [questId, completeStatus, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(540.0, self.sendTimeoutMovie, self.task)

    def assignQuest(self, avId, questId, rewardId, toNpcId):
        self.busy = avId
        if self.questCallback:
            self.questCallback()
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_ASSIGN,
         self.npcId,
         avId,
         [questId, rewardId, toNpcId],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(540.0, self.sendTimeoutMovie, self.task)

    def presentQuestChoice(self, avId, quests):
        self.busy = avId
        self.pendingAvId = avId
        self.pendingQuests = quests
        flatQuests = []
        for quest in quests:
            flatQuests.extend(quest)

        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE,
         self.npcId,
         avId,
         flatQuests,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(20.0, self.sendTimeoutMovie, self.task)

    def presentTrackChoice(self, avId, questId, tracks):
        self.busy = avId
        self.pendingAvId = avId
        self.pendingTracks = tracks
        self.pendingTrackQuest = questId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE,
         self.npcId,
         avId,
         tracks,
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(20.0, self.sendTimeoutMovie, self.task)

    def cancelChoseQuest(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_QUEST_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.task)

    def cancelChoseTrack(self, avId):
        self.busy = avId
        self.sendUpdate('setMovie', [NPCToons.QUEST_MOVIE_TRACK_CHOICE_CANCEL,
         self.npcId,
         avId,
         [],
         ClockDelta.globalClockDelta.getRealNetworkTime()])
        if not self.tutorial:
            self.clearTasks()
            self.task = self.uniqueName('clearMovie')
            taskMgr.doMethodLater(60.0, self.sendTimeoutMovie, self.task)

    def setMovieDone(self):
        avId = self.air.getAvatarIdFromSender()
        self.notify.debug('setMovieDone busy: %s avId: %s' % (self.busy, avId))
        if self.busy == avId:
            self.clearTasks()
            self.sendClearMovie(None)
        elif self.busy:
            self.air.writeServerEvent('suspicious', avId, 'DistributedNPCToonAI.setMovieDone busy with %s' % self.busy)
            self.notify.warning('somebody called setMovieDone that I was not busy with! avId: %s' % avId)
        return

    def __handleUnexpectedExit(self, avId):
        self.notify.warning('avatar:' + str(avId) + ' has exited unexpectedly')
        self.notify.warning('not busy with avId: %s, busy: %s ' % (avId, self.busy))
        self.clearTasks()
        taskMgr.remove(self.uniqueName('clearMovie'))
        self.sendClearMovie(None)
        return

    def clearTasks(self):
        if self.task:
            taskMgr.remove(self.task)

        self.task = None
