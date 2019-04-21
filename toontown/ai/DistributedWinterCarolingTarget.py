from toontown.speedchat import TTSCIndexedTerminal
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.interval.IntervalGlobal import *

class DistributedWinterCarolingTarget(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWinterCarolingTarget')

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.triggered = False
        self.triggerDelay = 15

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        DistributedWinterCarolingTarget.notify.debug('announceGenerate')
        self.accept(TTSCIndexedTerminal.TTSCIndexedMsgEvent, self.phraseSaid)

    def phraseSaid(self, phraseId):
        self.notify.debug('Checking if phrase was said')
        helpPhrases = []
        for i in xrange(6):
            helpPhrases.append(30220 + i)

        def reset():
            self.triggered = False

        if phraseId in helpPhrases and not self.triggered:
            self.triggered = True
            self.d_requestScavengerHunt()
            taskMgr.doMethodLater(self.triggerDelay, reset, 'ScavengerHunt-phrase-reset', extraArgs=[])
            
    def delete(self):
        self.ignore(TTSCIndexedTerminal.TTSCIndexedMsgEvent)
        DistributedObject.DistributedObject.delete(self)
        
    def d_requestScavengerHunt(self):
        self.sendUpdate('requestScavengerHunt', [])

    def doScavengerHunt(self, amount):
        DistributedWinterCarolingTarget.notify.debug('doScavengerHunt')
        base.localAvatar.winterCarolingTargetMet(amount)
