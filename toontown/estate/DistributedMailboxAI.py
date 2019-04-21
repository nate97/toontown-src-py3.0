from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.toonbase import ToontownGlobals
from toontown.estate import MailboxGlobals


class DistributedMailboxAI(DistributedObjectAI):
    notify = directNotify.newCategory('DistributedMailboxAI')

    def __init__(self, air, house):
        DistributedObjectAI.__init__(self, air)

        self.busy = False
        self.user = None
        self.house = house
        self.houseId = self.house.doId
        self.housePos = self.house.housePos
        self.name = self.house.name

    def generate(self):
        DistributedObjectAI.generate(self)

        self.updateIndicatorFlag()

    def getHouseId(self):
        return self.houseId

    def getHousePos(self):
        return self.housePos

    def getName(self):
        return self.name

    def avatarEnter(self):
        if self.busy:
            return
        avId = self.air.getAvatarIdFromSender()
        if avId != self.house.avatarId:
            self.setMovie(MailboxGlobals.MAILBOX_MOVIE_NOT_OWNER, avId)
            self.resetMovie()
            return

        av = self.air.doId2do.get(avId)
        if not av:
            return

        if len(av.mailboxContents):
            self.setMovie(MailboxGlobals.MAILBOX_MOVIE_READY, avId)
            self.user = avId
            self.busy = True
        elif len(av.onOrder):
            self.setMovie(MailboxGlobals.MAILBOX_MOVIE_WAITING, avId)
        else:
            self.setMovie(MailboxGlobals.MAILBOX_MOVIE_EMPTY, avId)

        self.resetMovie()

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.user:
            return
        self.user = None
        self.busy = False
        self.updateIndicatorFlag()
        self.setMovie(MailboxGlobals.MAILBOX_MOVIE_EXIT, avId)
        self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
        self.resetMovie()

    def setMovie(self, movie, avId):
        self.sendUpdate('setMovie', [movie, avId])

    def resetMovie(self):
        taskMgr.doMethodLater(2, self.setMovie, 'resetMovie-%d' % self.doId, extraArgs=[MailboxGlobals.MAILBOX_MOVIE_CLEAR, 0])

    def updateIndicatorFlag(self):
        av = self.air.doId2do.get(self.house.avatarId)
        if av:
            self.sendUpdate('setFullIndicator', [len(av.mailboxContents)])
        else:
            self.sendUpdate('setFullIndicator', [0])

    def acceptItemMessage(self, context, item, index, optional):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.user:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            return

        if index >= len(av.mailboxContents):
            self.sendUpdateToAvatarId(avId, 'acceptItemResponse', [context, ToontownGlobals.P_InvalidIndex])
            return

        item = av.mailboxContents[index]
        del av.mailboxContents[index]
        av.b_setMailboxContents(av.mailboxContents)
        self.sendUpdateToAvatarId(avId, 'acceptItemResponse', [context, item.recordPurchase(av, optional)])

    def discardItemMessage(self, context, item, index, optional):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.user:
            return

        av = self.air.doId2do.get(avId)
        if not av:
            return

        if index >= len(av.mailboxContents):
            self.sendUpdateToAvatarId(avId, 'discardItemResponse', [context, ToontownGlobals.P_InvalidIndex])
            return

        del av.mailboxContents[index]
        av.b_setMailboxContents(av.mailboxContents)
        self.sendUpdateToAvatarId(avId, 'discardItemResponse', [context, ToontownGlobals.P_ItemAvailable])

    def acceptInviteMessage(self, todo0, todo1):
        pass # TODO

    def rejectInviteMessage(self, todo0, todo1):
        pass # TODO

    def markInviteReadButNotReplied(self, todo0):
        pass # TODO



