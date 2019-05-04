from direct.directnotify import DirectNotifyGlobal
from toontown.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.distributed.ClockDelta import globalClockDelta
from direct.showbase.PythonUtil import lerp
from toontown.pets import PetTricks
from toontown.toon import DistributedToonAI

import random

class PetActionFSM(FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('PetActionFSM')

    def __init__(self, pet):
        FSM.FSM.__init__(self, PetActionFSM.__name__)
        self.pet = pet
        self.trickSerialNum = 0

    def destroy(self):
        self.cleanup()



    def enterNeutral(self):
        PetActionFSM.notify.debug('enterNeutral')

    def exitNeutral(self):
        pass




    def enterChase(self, target):
        PetActionFSM.notify.debug('enterChase: %s' % target)
        self.pet.inteligentMover.setTarget(target)
        self.pet.inteligentMover.setDoodleMode('chase')

    def exitChase(self):
        #self.pet.mover.removeImpulse('chase')
        self.pet.inteligentMover.setDoodleMode("wander") # experiment



    def enterFlee(self, chaser):
        PetActionFSM.notify.debug('enterFlee: %s' % chaser)
        self.pet.inteligentMover.setTarget(chaser)
        self.pet.inteligentMover.setDoodleMode('flee')

    def exitFlee(self):
        pass





    def enterWander(self):
        PetActionFSM.notify.debug('enterWander')
        self.pet.inteligentMover.setDoodleMode("wander")

    def exitWander(self):
        pass
        #self.pet.mover.removeImpulse('wander')




    def enterUnstick(self):
        PetActionFSM.notify.debug('enterUnstick')
        #self.pet.mover.addImpulse('unstick', self.pet.wanderImpulse)

    def exitUnstick(self):
        pass
        #self.pet.mover.removeImpulse('unstick')




    def enterInspectSpot(self, spot):
        PetActionFSM.notify.debug('enterInspectSpot')
        self.pet.inteligentMover.setDoodleMode("stick")

    def exitInspectSpot(self):
        self.pet.inteligentMover.setDoodleMode("unstick")



    def enterStay(self, avatar):
        PetActionFSM.notify.debug('enterStay')
        self.pet.inteligentMover.setDoodleMode("stick")

    def exitStay(self):
        self.pet.inteligentMover.setDoodleMode("unstick")



    def enterHeal(self, avatar):
        PetActionFSM.notify.debug('enterHeal')
        avatar.toonUp(3)
        #self.pet.chaseImpulse.setTarget(avatar)
        #self.pet.mover.addImpulse('chase', self.pet.chaseImpulse)




    def exitHeal(self):
        pass
        #self.pet.mover.removeImpulse('chase')




    def enterTrick(self, avatar, trickId):
        PetActionFSM.notify.debug('enterTrick')
        self.pet.inteligentMover.setDoodleMode("stick")
        self.pet.inteligentMover.lockPet()
        self.pet.sendUpdate('doTrick', [trickId, globalClockDelta.getRealNetworkTime()])

        def finish(avatar = avatar, trickId = trickId, self = self):
            if hasattr(self.pet, 'brain'):
                healRange = PetTricks.TrickHeals[trickId]
                aptitude = self.pet.getTrickAptitude(trickId)
                healAmt = int(lerp(healRange[0], healRange[1], aptitude))
                if healAmt:
                    for avId in self.pet.brain.getAvIdsLookingAtUs():
                        av = self.pet.air.doId2do.get(avId)
                        if av:
                            if isinstance(av, DistributedToonAI.DistributedToonAI):
                                av.toonUp(healAmt)

                self.pet._handleDidTrick(trickId)
                self.pet.inteligentMover.unlockPet()
                self.pet.inteligentMover.setDoodleMode("unstick")


                messenger.send(self.getTrickDoneEvent())

        self.trickDoneEvent = 'trickDone-%s-%s' % (self.pet.doId, self.trickSerialNum)
        self.trickSerialNum += 1
        self.trickFinishIval = Sequence(WaitInterval(PetTricks.TrickLengths[trickId]), Func(finish), name='petTrickFinish-%s' % self.pet.doId)
        self.trickFinishIval.start()

    def getTrickDoLaterName(self):
        return 'petTrickDoLater-%s' % self.pet.doId

    def getTrickDoneEvent(self):
        return self.trickDoneEvent

    def exitTrick(self):
        if self.trickFinishIval.isPlaying():
            self.trickFinishIval.finish()
        del self.trickFinishIval

        self.pet.inteligentMover.unlockPet()
        self.pet.inteligentMover.setDoodleMode("unstick")
        del self.trickDoneEvent

    def enterMovie(self):
        PetActionFSM.notify.debug('enterMovie')

    def exitMovie(self):
        pass
