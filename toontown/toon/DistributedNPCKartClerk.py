from direct.gui.DirectGui import *
from direct.task.Task import Task
from panda3d.core import *

from DistributedNPCToonBase import *
import NPCToons
from toontown.chat.ChatGlobals import *
from toontown.nametag.NametagGlobals import *
from toontown.racing.KartShopGlobals import *
from toontown.racing.KartShopGui import *
from toontown.toonbase import TTLocalizer


class DistributedNPCKartClerk(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.kartShopGui = None

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None
        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)

        DistributedNPCToonBase.disable(self)

    def getCollSphereRadius(self):
        return 2.25

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetKartShopClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupKartShopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.kartShopGui:
            self.kartShopGui.destroy()
            self.kartShopGui = None
        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        if self.isLocalToon:
            self.showNametag2d()
            self.freeAvatar()
        return Task.done

    def ignoreEventDict(self):
        for event in KartShopGlobals.EVENTDICT:
            self.ignore(event)

    def setMovie(self, mode, npcId, avId, extraArgs, timestamp):
        timeStamp = ClockDelta.globalClockDelta.localElapsedTime(timestamp)
        self.remain = NPCToons.CLERK_COUNTDOWN_TIME - timeStamp
        self.npcId = npcId
        self.isLocalToon = avId == base.localAvatar.doId
        if mode == NPCToons.SELL_MOVIE_CLEAR:
            return
        if mode == NPCToons.SELL_MOVIE_TIMEOUT:
            taskMgr.remove(self.uniqueName('lerpCamera'))
            if self.isLocalToon:
                self.ignoreEventDict()
                if self.popupInfo:
                    self.popupInfo.reparentTo(hidden)
                if self.kartShopGui:
                    self.kartShopGui.destroy()
                    self.kartShopGui = None
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetKartShopClerk()
        elif mode == NPCToons.SELL_MOVIE_START:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                self.accept(self.av.uniqueName('disable'), self.__handleUnexpectedExit)
            self.setupAvatars(self.av)
            if self.isLocalToon:
                self.hideNametag2d()
                camera.wrtReparentTo(render)
                quat = Quat()
                quat.setHpr((-150, -2, 0))
                camera.posQuatInterval(1, Point3(-5, 9, base.localAvatar.getHeight() - 0.5), quat, other=self, blendType='easeOut').start()
                taskMgr.doMethodLater(1.0, self.popupKartShopGUI, self.uniqueName('popupKartShopGUI'))
        elif mode == NPCToons.SELL_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
            self.resetKartShopClerk()
        elif mode == NPCToons.SELL_MOVIE_PETCANCELED:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_GOODBYE, CFSpeech | CFTimeout)
            self.resetKartShopClerk()

    def __handleBuyKart(self, kartID):
        self.sendUpdate('buyKart', [kartID])

    def __handleBuyAccessory(self, accID):
        self.sendUpdate('buyAccessory', [accID])

    def __handleGuiDone(self, bTimedOut = False):
        self.ignoreAll()
        if hasattr(self, 'kartShopGui') and self.kartShopGui != None:
            self.kartShopGui.destroy()
            self.kartShopGui = None
        if not bTimedOut:
            self.sendUpdate('transactionDone')

    def popupKartShopGUI(self, task):
        self.setChatAbsolute('', CFSpeech)
        self.accept(KartShopGlobals.EVENTDICT['buyAccessory'], self.__handleBuyAccessory)
        self.accept(KartShopGlobals.EVENTDICT['buyKart'], self.__handleBuyKart)
        self.acceptOnce(KartShopGlobals.EVENTDICT['guiDone'], self.__handleGuiDone)
        self.kartShopGui = KartShopGuiMgr(KartShopGlobals.EVENTDICT)
