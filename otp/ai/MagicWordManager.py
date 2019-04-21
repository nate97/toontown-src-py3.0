from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject

from otp.ai.MagicWordGlobal import *


lastClickedNametag = None


class MagicWordManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('MagicWordManager')
    neverDisable = 1

    def generate(self):
        DistributedObject.DistributedObject.generate(self)
        self.accept('magicWord', self.handleMagicWord)

    def disable(self):
        self.ignore('magicWord')
        DistributedObject.DistributedObject.disable(self)

    def handleMagicWord(self, magicWord):
        if not self.cr.wantMagicWords:
            return

        if magicWord.startswith('~~'):
            if lastClickedNametag == None:
                target = base.localAvatar
            else:
                target = lastClickedNametag
            magicWord = magicWord[2:]
        if magicWord.startswith('~'):
            target = base.localAvatar
            magicWord = magicWord[1:]

        targetId = target.doId
        self.sendUpdate('sendMagicWord', [magicWord, targetId])
        if target == base.localAvatar:
            response = spellbook.process(base.localAvatar, target, magicWord)
            if response:
                self.sendMagicWordResponse(response)

    def sendMagicWordResponse(self, response):
        self.notify.info(response)
        base.localAvatar.setSystemMessage(0, 'Spellbook: ' + str(response))
