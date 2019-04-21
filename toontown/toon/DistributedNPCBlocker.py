from panda3d.core import *
from DistributedNPCToonBase import *
from direct.gui.DirectGui import *
from panda3d.core import *
import NPCToons
from toontown.toonbase import TTLocalizer
from direct.distributed import DistributedObject
from toontown.quest import QuestParser


class DistributedNPCBlocker(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

        self.cSphereNodePath.setScale(4.5, 1.0, 6.0)
        self.isLocalToon = False
        self.movie = None

    def initToonState(self):
        self.setAnimState('neutral', 0.9, None, None)
        posh = NPCToons.BlockerPositions[self.name]
        self.setPos(posh[0])
        self.setH(posh[1])

    def disable(self):
        if hasattr(self, 'movie') and self.movie:
            self.movie.cleanup()
            del self.movie
            if self.isLocalToon:
                base.localAvatar.posCamera(0, 0)

        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('quest', [self])
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')

    def resetBlocker(self):
        self.cSphereNode.setCollideMask(BitMask32())
        if hasattr(self, 'movie') and self.movie:
            self.movie.cleanup()
            self.movie = None
        self.startLookAround()
        self.clearMat()
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)
            self.freeAvatar()
            self.isLocalToon = False

    def setMovie(self, mode, npcId, avId, timestamp):
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.BLOCKER_MOVIE_CLEAR:
            return
        elif mode == NPCToons.BLOCKER_MOVIE_START:
            if self.isLocalToon:
                self.hideNametag2d()
            self.movie = QuestParser.NPCMoviePlayer('tutorial_blocker', base.localAvatar, self)
            self.movie.play()
        elif mode == NPCToons.BLOCKER_MOVIE_TIMEOUT:
            return

    def finishMovie(self, av, isLocalToon, elapsedTime):
        self.resetBlocker()
        if self.isLocalToon:
            self.showNametag2d()
