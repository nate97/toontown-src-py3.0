from panda3d.core import *
import DistributedCCharBase
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State
from direct.fsm import State
import CharStateDatas
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.hood import DGHood

class DistributedVampireMickey(DistributedCCharBase.DistributedCCharBase):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedVampireMickey')

    def __init__(self, cr):
        try:
            self.DistributedVampireMickey_initialized
        except:
            self.DistributedVampireMickey_initialized = 1
            DistributedCCharBase.DistributedCCharBase.__init__(self, cr, TTLocalizer.VampireMickey, 'vmk')
            self.fsm = ClassicFSM.ClassicFSM(self.getName(), [State.State('Off', self.enterOff, self.exitOff, ['Neutral']), State.State('Neutral', self.enterNeutral, self.exitNeutral, ['Walk']), State.State('Walk', self.enterWalk, self.exitWalk, ['Neutral'])], 'Off', 'Off')
            self.fsm.enterInitialState()
            self.handleHolidays()
            self.nametag.setText(TTLocalizer.Mickey)


    def disable(self):
        self.fsm.requestFinalState()
        DistributedCCharBase.DistributedCCharBase.disable(self)
        self.neutralDoneEvent = None
        self.neutral = None
        self.walkDoneEvent = None
        self.walk = None
        self.fsm.requestFinalState()
        self.notify.debug('Mickey Disbled')
        return


    def delete(self):
        try:
            self.DistributedVampireMickey_deleted
        except:
            self.DistributedVampireMickey_deleted = 1
            del self.fsm
            DistributedCCharBase.DistributedCCharBase.delete(self)

        self.notify.debug('Mickey Deleted')


    def generate(self):
        DistributedCCharBase.DistributedCCharBase.generate(self, self.diffPath)
        name = self.getName()
        self.neutralDoneEvent = self.taskName(name + '-neutral-done')
        self.neutral = CharStateDatas.CharNeutralState(self.neutralDoneEvent, self)
        self.walkDoneEvent = self.taskName(name + '-walk-done')
        if self.diffPath == None:
            self.walk = CharStateDatas.CharWalkState(self.walkDoneEvent, self)
        else:
            self.walk = CharStateDatas.CharWalkState(self.walkDoneEvent, self, self.diffPath)
        self.fsm.request('Neutral')
        return


    def enterOff(self):
        pass


    def exitOff(self):
        pass


    def enterNeutral(self):
        self.neutral.enter()
        self.acceptOnce(self.neutralDoneEvent, self.__decideNextState)


    def exitNeutral(self):
        self.ignore(self.neutralDoneEvent)
        self.neutral.exit()


    def enterWalk(self):
        self.walk.enter()
        self.acceptOnce(self.walkDoneEvent, self.__decideNextState)


    def exitWalk(self):
        self.ignore(self.walkDoneEvent)
        self.walk.exit()


    def __decideNextState(self, doneStatus):
        self.fsm.request('Neutral')


    def setWalk(self, srcNode, destNode, timestamp):
        if destNode and not destNode == srcNode:
            self.walk.setWalk(srcNode, destNode, timestamp)
            self.fsm.request('Walk')


    def walkSpeed(self):
        return ToontownGlobals.VampireMickeySpeed


