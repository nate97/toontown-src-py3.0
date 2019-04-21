from direct.directnotify import DirectNotifyGlobal
from toontown.classicchars.DistributedMickeyAI import DistributedMickeyAI

class DistributedVampireMickeyAI(DistributedMickeyAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedVampireMickeyAI")


from otp.ai.AIBaseGlobal import *
import DistributedCCharBaseAI
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.task import Task
import random
from toontown.toonbase import ToontownGlobals
import CharStateDatasAI
from toontown.toonbase import TTLocalizer

class DistributedVampireMickeyAI(DistributedCCharBaseAI.DistributedCCharBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVampireMickeyAI')
    
    def __init__(self, air):
        DistributedCCharBaseAI.DistributedCCharBaseAI.__init__(self, air, TTLocalizer.VampireMickey)
        self.fsm = ClassicFSM.ClassicFSM('DistributedVampireMickeyAI', [
            State.State('Off', self.enterOff, self.exitOff, [
                'Lonely',
                'TransitionToCostume',
                'Walk']),
            State.State('Lonely', self.enterLonely, self.exitLonely, [
                'Chatty',
                'Walk',
                'TransitionToCostume']),
            State.State('Chatty', self.enterChatty, self.exitChatty, [
                'Lonely',
                'Walk',
                'TransitionToCostume']),
            State.State('Walk', self.enterWalk, self.exitWalk, [
                'Lonely',
                'Chatty',
                'TransitionToCostume']),
            State.State('TransitionToCostume', self.enterTransitionToCostume, self.exitTransitionToCostume, [
                'Off'])], 'Off', 'Off')
        self.fsm.enterInitialState()

    
    def delete(self):
        self.fsm.requestFinalState()
        del self.fsm
        DistributedCCharBaseAI.DistributedCCharBaseAI.delete(self)
        self.lonelyDoneEvent = None
        self.lonely = None
        self.chattyDoneEvent = None
        self.chatty = None
        self.walkDoneEvent = None
        self.walk = None
        self.notify.debug('MickeyAI Deleted')

    
    def generate(self):
        DistributedCCharBaseAI.DistributedCCharBaseAI.generate(self)
        name = self.getName()
        self.lonelyDoneEvent = self.taskName(name + '-lonely-done')
        self.lonely = CharStateDatasAI.CharLonelyStateAI(self.lonelyDoneEvent, self)
        self.chattyDoneEvent = self.taskName(name + '-chatty-done')
        self.chatty = CharStateDatasAI.CharChattyStateAI(self.chattyDoneEvent, self)
        self.walkDoneEvent = self.taskName(name + '-walk-done')
        if self.diffPath == None:
            self.walk = CharStateDatasAI.CharWalkStateAI(self.walkDoneEvent, self)
        else:
            self.walk = CharStateDatasAI.CharWalkStateAI(self.walkDoneEvent, self, self.diffPath)

    
    def walkSpeed(self):
        return ToontownGlobals.VampireMickeySpeed

    
    def start(self):
        self.fsm.request('Lonely')

    
    def _DistributedVampireMickeyAI__decideNextState(self, doneStatus):
        self.handleHalloweenCostumeExit()

        if doneStatus['state'] == 'lonely' and doneStatus['status'] == 'done':
            self.fsm.request('Walk')
        elif doneStatus['state'] == 'chatty' and doneStatus['status'] == 'done':
            self.fsm.request('Walk')
        elif doneStatus['state'] == 'walk' and doneStatus['status'] == 'done':
            if len(self.nearbyAvatars) > 0:
                self.fsm.request('Chatty')
            else:
                self.fsm.request('Lonely')
        

    def enterOff(self):
        pass

    
    def exitOff(self):
        DistributedCCharBaseAI.DistributedCCharBaseAI.exitOff(self)

    
    def enterLonely(self):
        self.lonely.enter()
        self.acceptOnce(self.lonelyDoneEvent, self._DistributedVampireMickeyAI__decideNextState)

    
    def exitLonely(self):
        self.ignore(self.lonelyDoneEvent)
        self.lonely.exit()

    
    def _DistributedVampireMickeyAI__goForAWalk(self, task):
        self.notify.debug('going for a walk')
        self.fsm.request('Walk')
        return Task.done

    
    def enterChatty(self):
        self.chatty.enter()
        self.acceptOnce(self.chattyDoneEvent, self._DistributedVampireMickeyAI__decideNextState)

    
    def exitChatty(self):
        self.ignore(self.chattyDoneEvent)
        self.chatty.exit()

    
    def enterWalk(self):
        self.notify.debug('going for a walk')
        self.walk.enter()
        self.acceptOnce(self.walkDoneEvent, self._DistributedVampireMickeyAI__decideNextState)

    
    def exitWalk(self):
        self.ignore(self.walkDoneEvent)
        self.walk.exit()

    
    def avatarEnterNextState(self):
        if len(self.nearbyAvatars) == 1:
            if self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Chatty')
            else:
                self.notify.debug('avatarEnterNextState: in walk state')
        else:
            self.notify.debug('avatarEnterNextState: num avatars: ' + str(len(self.nearbyAvatars)))

    
    def avatarExitNextState(self):
        if len(self.nearbyAvatars) == 0:
            if self.fsm.getCurrentState().getName() != 'Walk':
                self.fsm.request('Lonely')
            
        
    def enterTransitionToCostume(self):
        pass

    
    def exitTransitionToCostume(self):
        pass


