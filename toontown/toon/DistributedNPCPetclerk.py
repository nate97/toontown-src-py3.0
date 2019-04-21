from direct.gui.DirectGui import *
from direct.task.Task import Task
from panda3d.core import *
from panda3d.core import *

from DistributedNPCToonBase import *
import NPCToons
from toontown.chat.ChatGlobals import *
from toontown.hood import ZoneUtil
from toontown.nametag.NametagGlobals import *
from toontown.pets import PetshopGUI
from toontown.toonbase import TTLocalizer
from toontown.toontowngui import TeaserPanel


class DistributedNPCPetclerk(DistributedNPCToonBase):
    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)
        self.isLocalToon = 0
        self.av = None
        self.button = None
        self.popupInfo = None
        self.petshopGui = None
        self.petSeeds = None
        self.waitingForPetSeeds = False

    def disable(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPetshopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.popupInfo:
            self.popupInfo.destroy()
            self.popupInfo = None
        if self.petshopGui:
            self.petshopGui.destroy()
            self.petshopGui = None
        self.av = None
        if self.isLocalToon:
            base.localAvatar.posCamera(0, 0)

        DistributedNPCToonBase.disable(self)

    def generate(self):
        DistributedNPCToonBase.generate(self)

        self.eventDict = {}
        self.eventDict['guiDone'] = 'guiDone'
        self.eventDict['petAdopted'] = 'petAdopted'
        self.eventDict['petReturned'] = 'petReturned'
        self.eventDict['fishSold'] = 'fishSold'

    def getCollSphereRadius(self):
        return 4.0

    def allowedToEnter(self):
        return True

    def handleOkTeaser(self):
        self.dialog.destroy()
        del self.dialog
        place = base.cr.playGame.getPlace()
        if place:
            place.fsm.request('walk')

    def handleCollisionSphereEnter(self, collEntry):
        base.cr.playGame.getPlace().fsm.request('purchase')
        self.sendUpdate('avatarEnter', [])

    def __handleUnexpectedExit(self):
        self.notify.warning('unexpected exit')
        self.av = None

    def resetPetshopClerk(self):
        self.ignoreAll()
        taskMgr.remove(self.uniqueName('popupPetshopGUI'))
        taskMgr.remove(self.uniqueName('lerpCamera'))
        if self.petshopGui:
            self.petshopGui.destroy()
            self.petshopGui = None
        self.show()
        self.startLookAround()
        self.detectAvatars()
        self.clearMat()
        if self.isLocalToon:
            self.showNametag2d()
            self.freeAvatar()
        self.petSeeds = None
        self.waitingForPetSeeds = False
        return Task.done

    def ignoreEventDict(self):
        for event in self.eventDict.values():
            self.ignore(event)

    def setPetSeeds(self, petSeeds):
        self.petSeeds = petSeeds
        if self.waitingForPetSeeds:
            self.waitingForPetSeeds = False
            self.popupPetshopGUI(None)

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
                if self.petshopGui:
                    self.petshopGui.destroy()
                    self.petshopGui = None
            self.setChatAbsolute(TTLocalizer.STOREOWNER_TOOKTOOLONG, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
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
                seq = Sequence((camera.posQuatInterval(1, Vec3(-5, 9, self.getHeight() - 0.5), Vec3(-150, -2, 0), other=self, blendType='easeOut', name=self.uniqueName('lerpCamera'))))
                seq.start()
                taskMgr.doMethodLater(1.0, self.popupPetshopGUI, self.uniqueName('popupPetshopGUI'))
        elif mode == NPCToons.SELL_MOVIE_COMPLETE:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_THANKSFISH_PETSHOP, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_PETRETURNED:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETRETURNED, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_PETADOPTED:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETADOPTED, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_PETCANCELED:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_PETCANCELED, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_TROPHY:
            self.av = base.cr.doId2do.get(avId)
            if self.av is None:
                self.notify.warning('Avatar %d not found in doId' % avId)
                return
            else:
                numFish, totalNumFish = extraArgs
                self.setChatAbsolute(TTLocalizer.STOREOWNER_TROPHY % (numFish, totalNumFish), CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_NOFISH:
            self.setChatAbsolute(TTLocalizer.STOREOWNER_NOFISH, CFSpeech | CFTimeout)
            self.resetPetshopClerk()
        elif mode == NPCToons.SELL_MOVIE_NO_MONEY:
            self.notify.warning('SELL_MOVIE_NO_MONEY should not be called')
            self.resetPetshopClerk()

    def __handlePetAdopted(self, whichPet, nameIndex):
        if base.config.GetBool('want-qa-regression', 0):
            self.notify.info('QA-REGRESSION: ADOPTADOOLE: Adopt a doodle.')
        base.cr.removePetFromFriendsMap()
        self.ignore(self.eventDict['petAdopted'])
        self.sendUpdate('petAdopted', [whichPet, nameIndex])

    def __handlePetReturned(self):
        base.cr.removePetFromFriendsMap()
        self.ignore(self.eventDict['petReturned'])
        self.sendUpdate('petReturned')

    def __handleFishSold(self):
        self.ignore(self.eventDict['fishSold'])
        self.sendUpdate('fishSold')

    def __handleGUIDone(self, bTimedOut = False):
        self.ignore(self.eventDict['guiDone'])
        self.petshopGui.destroy()
        self.petshopGui = None
        if not bTimedOut:
            self.sendUpdate('transactionDone')
        return

    def popupPetshopGUI(self, task):
        if not self.petSeeds:
            self.waitingForPetSeeds = True
            return
        self.setChatAbsolute('', CFSpeech)
        self.acceptOnce(self.eventDict['guiDone'], self.__handleGUIDone)
        self.acceptOnce(self.eventDict['petAdopted'], self.__handlePetAdopted)
        self.acceptOnce(self.eventDict['petReturned'], self.__handlePetReturned)
        self.acceptOnce(self.eventDict['fishSold'], self.__handleFishSold)
        self.petshopGui = PetshopGUI.PetshopGUI(self.eventDict, self.petSeeds)
