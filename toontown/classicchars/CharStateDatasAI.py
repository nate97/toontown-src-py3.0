# File: C (Python 2.4)

from otp.ai.AIBaseGlobal import *
from direct.distributed.ClockDelta import *
from direct.fsm import StateData
from direct.directnotify import DirectNotifyGlobal
import random
from direct.task import Task
from toontown.toonbase import ToontownGlobals
import CCharChatter
import CCharPaths

class CharLonelyStateAI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('CharLonelyStateAI')
    
    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self._CharLonelyStateAI__doneEvent = doneEvent
        self.character = character

    
    def enter(self):
        if hasattr(self.character, 'name'):
            name = self.character.getName()
        else:
            name = 'character'
        self.notify.debug('Lonely ' + self.character.getName() + '...')
        StateData.StateData.enter(self)
        duration = random.randint(3, 15)
        taskMgr.doMethodLater(duration, self._CharLonelyStateAI__doneHandler, self.character.taskName('startWalking'))

    
    def exit(self):
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName('startWalking'))

    
    def _CharLonelyStateAI__doneHandler(self, task):
        doneStatus = { }
        doneStatus['state'] = 'lonely'
        doneStatus['status'] = 'done'
        messenger.send(self._CharLonelyStateAI__doneEvent, [
            doneStatus])
        return Task.done



class CharChattyStateAI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('CharChattyStateAI')
    
    def __init__(self, doneEvent, character):
        StateData.StateData.__init__(self, doneEvent)
        self._CharChattyStateAI__doneEvent = doneEvent
        self.character = character
        self._CharChattyStateAI__chatTaskName = 'characterChat-' + str(character)
        self.lastChatTarget = 0
        self.nextChatTime = 0
        self.lastMessage = [
            -1,
            -1]

    
    def enter(self):
        if hasattr(self.character, 'name'):
            name = self.character.getName()
        else:
            name = 'character'
        self.notify.debug('Chatty ' + self.character.getName() + '...')
        self.chatter = CCharChatter.getChatter(self.character.getName(), self.character.getCCChatter())
        if self.chatter != None:
            taskMgr.remove(self._CharChattyStateAI__chatTaskName)
            taskMgr.add(self.blather, self._CharChattyStateAI__chatTaskName)
        
        StateData.StateData.enter(self)

    
    def pickMsg(self, category):
        self.getLatestChatter()
        if self.chatter:
            return random.randint(0, len(self.chatter[category]) - 1)
        else:
            return None

    
    def getLatestChatter(self):
        self.chatter = CCharChatter.getChatter(self.character.getName(), self.character.getCCChatter())

    
    def setCorrectChatter(self):
        self.chatter = CCharChatter.getChatter(self.character.getName(), self.character.getCCChatter())

    
    def blather(self, task):
        now = globalClock.getFrameTime()
        if now < self.nextChatTime:
            return Task.cont
        
        self.getLatestChatter()
        if self.character.lostInterest():
            self.leave()
            return Task.done
        
        if not self.chatter:
            self.notify.debug('I do not want to talk')
            return Task.done
        
        if not self.character.getNearbyAvatars():
            return Task.cont
        
        target = self.character.getNearbyAvatars()[0]
        if self.lastChatTarget != target:
            self.lastChatTarget = target
            category = CCharChatter.GREETING
        else:
            category = CCharChatter.COMMENT
        self.setCorrectChatter()
        if category == self.lastMessage[0] and len(self.chatter[category]) > 1:
            msg = self.lastMessage[1]
            lastMsgIndex = self.lastMessage[1]
            if lastMsgIndex < len(self.chatter[category]) and lastMsgIndex >= 0:
                while self.chatter[category][msg] == self.chatter[category][lastMsgIndex]:
                    msg = self.pickMsg(category)
                    if not msg:
                        break
                        continue
            else:
                msg = self.pickMsg(category)
        else:
            msg = self.pickMsg(category)
        if msg == None:
            self.notify.debug('I do not want to talk')
            return Task.done
        
        self.character.sendUpdate('setChat', [
            category,
            msg,
            target])
        self.lastMessage = [
            category,
            msg]
        self.nextChatTime = now + 8.0 + random.random() * 4.0
        return Task.cont

    
    def leave(self):
        if self.chatter != None:
            category = CCharChatter.GOODBYE
            msg = random.randint(0, len(self.chatter[CCharChatter.GOODBYE]) - 1)
            target = self.character.getNearbyAvatars()[0]
            self.character.sendUpdate('setChat', [
                category,
                msg,
                target])
        
        taskMgr.doMethodLater(1, self.doneHandler, self.character.taskName('waitToFinish'))

    
    def exit(self):
        StateData.StateData.exit(self)
        taskMgr.remove(self._CharChattyStateAI__chatTaskName)

    
    def doneHandler(self, task):
        doneStatus = { }
        doneStatus['state'] = 'chatty'
        doneStatus['status'] = 'done'
        messenger.send(self._CharChattyStateAI__doneEvent, [
            doneStatus])
        return Task.done



class CharWalkStateAI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('CharWalkStateAI')
    
    def __init__(self, doneEvent, character, diffPath = None):
        StateData.StateData.__init__(self, doneEvent)
        self._CharWalkStateAI__doneEvent = doneEvent
        self.character = character
        if diffPath == None:
            self.paths = CCharPaths.getPaths(character.getName(), character.getCCLocation())
        else:
            self.paths = CCharPaths.getPaths(diffPath, character.getCCLocation())
        self.speed = character.walkSpeed()
        self._CharWalkStateAI__lastWalkNode = CCharPaths.startNode
        self._CharWalkStateAI__curWalkNode = CCharPaths.startNode

    
    def enter(self):
        destNode = self._CharWalkStateAI__lastWalkNode
        choices = CCharPaths.getAdjacentNodes(self._CharWalkStateAI__curWalkNode, self.paths)
        if len(choices) == 1:
            destNode = choices[0]
        else:
            while destNode == self._CharWalkStateAI__lastWalkNode:
                destNode = random.choice(CCharPaths.getAdjacentNodes(self._CharWalkStateAI__curWalkNode, self.paths))
        self.notify.debug('Walking ' + self.character.getName() + '... from ' + str(self._CharWalkStateAI__curWalkNode) + '(' + str(CCharPaths.getNodePos(self._CharWalkStateAI__curWalkNode, self.paths)) + ') to ' + str(destNode) + '(' + str(CCharPaths.getNodePos(destNode, self.paths)) + ')')
        self.character.sendUpdate('setWalk', [
            self._CharWalkStateAI__curWalkNode,
            destNode,
            globalClockDelta.getRealNetworkTime()])
        duration = CCharPaths.getWalkDuration(self._CharWalkStateAI__curWalkNode, destNode, self.speed, self.paths)
        t = taskMgr.doMethodLater(duration, self.doneHandler, self.character.taskName(self.character.getName() + 'DoneWalking'))
        t.newWalkNode = destNode
        self.destNode = destNode

    
    def exit(self):
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName(self.character.getName() + 'DoneWalking'))

    
    def getDestNode(self):
        if hasattr(self, 'destNode') and self.destNode:
            return self.destNode
        else:
            return self._CharWalkStateAI__curWalkNode

    
    def setCurNode(self, curWalkNode):
        self._CharWalkStateAI__curWalkNode = curWalkNode

    
    def doneHandler(self, task):
        self._CharWalkStateAI__lastWalkNode = self._CharWalkStateAI__curWalkNode
        self._CharWalkStateAI__curWalkNode = task.newWalkNode
        self.character.sendUpdate('setWalk', [
            self._CharWalkStateAI__curWalkNode,
            self._CharWalkStateAI__curWalkNode,
            globalClockDelta.getRealNetworkTime()])
        doneStatus = { }
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self._CharWalkStateAI__doneEvent, [
            doneStatus])
        return Task.done



class CharFollowChipStateAI(StateData.StateData):
    notify = DirectNotifyGlobal.directNotify.newCategory('CharFollowChipStateAI')
    
    def __init__(self, doneEvent, character, followedChar):
        StateData.StateData.__init__(self, doneEvent)
        self._CharFollowChipStateAI__doneEvent = doneEvent
        self.character = character
        self.followedChar = followedChar
        self.paths = CCharPaths.getPaths(character.getName(), character.getCCLocation())
        self.speed = character.walkSpeed()
        self._CharFollowChipStateAI__lastWalkNode = CCharPaths.startNode
        self._CharFollowChipStateAI__curWalkNode = CCharPaths.startNode

    
    def setCurNode(self, curWalkNode):
        self._CharFollowChipStateAI__curWalkNode = curWalkNode


    def getDestNode(self):
        if hasattr(self, 'destNode') and self.destNode:
            return self.destNode
        else:
            return self._CharFollowChipStateAI__curWalkNode


    def enter(self, chipDestNode):
        destNode = self._CharFollowChipStateAI__lastWalkNode
        choices = CCharPaths.getAdjacentNodes(self._CharFollowChipStateAI__curWalkNode, self.paths)
        if len(choices) == 1:
            destNode = choices[0]
        else:
            while destNode == self._CharFollowChipStateAI__lastWalkNode:
                destNode = random.choice(CCharPaths.getAdjacentNodes(self._CharFollowChipStateAI__curWalkNode, self.paths))
        destNode = chipDestNode
        self.notify.debug('Walking ' + self.character.getName() + '... from ' + str(self._CharFollowChipStateAI__curWalkNode) + '(' + str(CCharPaths.getNodePos(self._CharFollowChipStateAI__curWalkNode, self.paths)) + ') to ' + str(destNode) + '(' + str(CCharPaths.getNodePos(destNode, self.paths)) + ')')
        self.offsetDistance = ToontownGlobals.DaleOrbitDistance
        angle = random.randint(0, 359)
        self.offsetX = math.cos(deg2Rad(angle)) * self.offsetDistance
        self.offsetY = math.sin(deg2Rad(angle)) * self.offsetDistance
        self.character.sendUpdate('setFollowChip', [
            self._CharFollowChipStateAI__curWalkNode,
            destNode,
            globalClockDelta.getRealNetworkTime(),
            self.offsetX,
            self.offsetY])
        duration = CCharPaths.getWalkDuration(self._CharFollowChipStateAI__curWalkNode, destNode, self.speed, self.paths)
        t = taskMgr.doMethodLater(duration, self._CharFollowChipStateAI__doneHandler, self.character.taskName(self.character.getName() + 'DoneWalking'))
        t.newWalkNode = destNode
        self.destNode = destNode

    
    def exit(self):
        StateData.StateData.exit(self)
        taskMgr.remove(self.character.taskName(self.character.getName() + 'DoneWalking'))

    
    def _CharFollowChipStateAI__doneHandler(self, task):
        self._CharFollowChipStateAI__lastWalkNode = self._CharFollowChipStateAI__curWalkNode
        self._CharFollowChipStateAI__curWalkNode = task.newWalkNode
        self.character.sendUpdate('setFollowChip', [
            self._CharFollowChipStateAI__curWalkNode,
            self._CharFollowChipStateAI__curWalkNode,
            globalClockDelta.getRealNetworkTime(),
            self.offsetX,
            self.offsetY])
        doneStatus = { }
        doneStatus['state'] = 'walk'
        doneStatus['status'] = 'done'
        messenger.send(self._CharFollowChipStateAI__doneEvent, [
            doneStatus])
        return Task.done



class ChipChattyStateAI(CharChattyStateAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('ChipChattyStateAI')
    
    def setDaleId(self, daleId):
        self.daleId = daleId
        self.dale = simbase.air.doId2do.get(self.daleId)

    
    def blather(self, task):
        now = globalClock.getFrameTime()
        if now < self.nextChatTime:
            return Task.cont
        
        self.getLatestChatter()
        if self.character.lostInterest():
            self.leave()
            return Task.done
        
        if not self.chatter:
            self.notify.debug('I do not want to talk')
            return Task.done
        
        if not self.character.getNearbyAvatars():
            return Task.cont
        
        target = self.character.getNearbyAvatars()[0]
        if self.lastChatTarget != target:
            self.lastChatTarget = target
            category = CCharChatter.GREETING
        else:
            category = CCharChatter.COMMENT
        if category == self.lastMessage[0] and len(self.chatter[category]) > 1:
            msg = self.lastMessage[1]
            lastMsgIndex = self.lastMessage[1]
            if lastMsgIndex < len(self.chatter[category]) and lastMsgIndex >= 0:
                while self.chatter[category][msg] == self.chatter[category][lastMsgIndex]:
                    msg = self.pickMsg(category)
                    if not msg:
                        break
                        continue
            else:
                msg = self.pickMsg(category)
        else:
            msg = self.pickMsg(category)
        if msg == None:
            self.notify.debug('I do not want to talk')
            return Task.done
        
        self.character.sendUpdate('setChat', [
            category,
            msg,
            target])
        if hasattr(self, 'dale') and self.dale:
            self.dale.sendUpdate('setChat', [
                category,
                msg,
                target])
        
        self.lastMessage = [
            category,
            msg]
        self.nextChatTime = now + 8.0 + random.random() * 4.0
        return Task.cont

    
    def leave(self):
        if self.chatter != None:
            category = CCharChatter.GOODBYE
            msg = random.randint(0, len(self.chatter[CCharChatter.GOODBYE]) - 1)
            target = self.character.getNearbyAvatars()[0]
            self.character.sendUpdate('setChat', [
                category,
                msg,
                target])
            if hasattr(self, 'dale') and self.dale:
                self.dale.sendUpdate('setChat', [
                    category,
                    msg,
                    target])
            
        
        taskMgr.doMethodLater(1, self.doneHandler, self.character.taskName('waitToFinish'))


