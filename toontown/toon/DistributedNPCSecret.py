from DistributedNPCToonBase import *
from toontown.chat.ChatGlobals import *
from toontown.nametag.NametagGlobals import *


class DistributedNPCSecret(DistributedNPCToonBase):

    def __init__(self, cr):
        DistributedNPCToonBase.__init__(self, cr)

    def delayDelete(self):
        DistributedNPCToonBase.delayDelete(self)
        DistributedNPCToonBase.disable(self)

    def handleCollisionSphereEnter(self, collEntry):
        self.sendUpdate('avatarEnter', [])

    def createBot(self, chatPhraseId):
        chatPhrases = [
            "I'm Kyle, AKA the chicken lord, and I like to make bots!",
            'I love the smell of fresh bots in the morning...',
            'Bots... bots... bots...',
            "Patch the Injector, or we'll continue...",
            "All the kids who sweat it out... it's unbelievable! Let's give them more bots!",
            "Master Milton is sweaty. Here's another bot!"
        ]
        self.setChatAbsolute(chatPhrases[chatPhraseId], CFSpeech|CFTimeout)