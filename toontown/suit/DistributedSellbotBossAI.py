import random

import DistributedBossCogAI
import DistributedSuitAI
import SuitDNA
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.ClockDelta import *
from direct.fsm import FSM
from otp.ai.AIBaseGlobal import *
from toontown.battle import BattleExperienceAI
from toontown.toon import NPCToons
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from otp.ai.MagicWordGlobal import *


class DistributedSellbotBossAI(DistributedBossCogAI.DistributedBossCogAI, FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedSellbotBossAI')
    limitHitCount = 6
    hitCountDamage = 35
    numPies = ToontownGlobals.FullPies

    def __init__(self, air):
        DistributedBossCogAI.DistributedBossCogAI.__init__(self, air, 's')
        FSM.FSM.__init__(self, 'DistributedSellbotBossAI')
        self.doobers = []
        self.cagedToonNpcId = random.choice(NPCToons.HQnpcFriends.keys())
        self.bossMaxDamage = ToontownGlobals.SellbotBossMaxDamage
        self.recoverRate = 0
        self.recoverStartTime = 0

    def delete(self):
        return DistributedBossCogAI.DistributedBossCogAI.delete(self)

    def getHoodId(self):
        return ToontownGlobals.SellbotHQ

    def getCagedToonNpcId(self):
        return self.cagedToonNpcId

    def magicWordHit(self, damage, avId):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            self.hitBossInsides()
        self.hitBoss(damage)

    def hitBoss(self, bossDamage):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'hitBoss from unknown avatar'):
            return
        self.validate(avId, bossDamage == 1, 'invalid bossDamage %s' % bossDamage)
        if bossDamage > 1:
            simbase.air.writeServerEvent('suspicious', avId, 'Toon sent an attack over 1 damage!')
            simbase.air.banManager.ban(avId, 0, 'hacking')
            return
        if bossDamage < 1:
            simbase.air.writeServerEvent('suspicious', avId, 'Toon sent an attack less than 1 damage!')
            return
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            return
        bossDamage = min(self.getBossDamage() + bossDamage, self.bossMaxDamage)
        self.b_setBossDamage(bossDamage, 0, 0)
        if self.bossDamage >= self.bossMaxDamage:
            self.setState('NearVictory')
        else:
            self.__recordHit()

    def hitBossInsides(self):
        avId = self.air.getAvatarIdFromSender()
        if not self.validate(avId, avId in self.involvedToons, 'hitBossInsides from unknown avatar'):
            return
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        self.b_setAttackCode(ToontownGlobals.BossCogDizzyNow)
        self.b_setBossDamage(self.getBossDamage(), 0, 0)

    def hitToon(self, toonId):
        avId = self.air.getAvatarIdFromSender()
        if avId == toonId:
            simbase.air.writeServerEvent('suspicious', avId, 'Toon tried to heal their self!')
            simbase.air.banManager.ban(avId, 0, 'hacking')
        if not self.validate(avId, avId != toonId, 'hitToon on self'):
            return
        if avId not in self.involvedToons or toonId not in self.involvedToons:
            return
        toon = self.air.doId2do.get(toonId)
        if toon:
            self.healToon(toon, 1)

    def touchCage(self):
        avId = self.air.getAvatarIdFromSender()
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree' and currState != 'NearVictory':
            return
        if not self.validate(avId, avId in self.involvedToons, 'touchCage from unknown avatar'):
            return
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(self.numPies)
            toon.__touchedCage = 1
            self.__goodJump(avId)

    def finalPieSplat(self):
        if self.state_ != 'NearVictory':
            return
        self.b_setState('Victory')

    def doNextAttack(self, task):
        if self.attackCode == ToontownGlobals.BossCogDizzyNow:
            attackCode = ToontownGlobals.BossCogRecoverDizzyAttack
        else:
            attackCode = random.choice([ToontownGlobals.BossCogAreaAttack,
             ToontownGlobals.BossCogFrontAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack,
             ToontownGlobals.BossCogDirectedAttack])
        if attackCode == ToontownGlobals.BossCogAreaAttack:
            self.__doAreaAttack()
        elif attackCode == ToontownGlobals.BossCogDirectedAttack:
            self.__doDirectedAttack()
        else:
            self.b_setAttackCode(attackCode)

    def __doAreaAttack(self):
        self.b_setAttackCode(ToontownGlobals.BossCogAreaAttack)
        if self.recoverRate:
            newRecoverRate = min(200, self.recoverRate * 1.2)
        else:
            newRecoverRate = 2
        now = globalClock.getFrameTime()
        self.b_setBossDamage(self.getBossDamage(), newRecoverRate, now)

    def __doDirectedAttack(self):
        if self.nearToons:
            toonId = random.choice(self.nearToons)
            self.b_setAttackCode(ToontownGlobals.BossCogDirectedAttack, toonId)
        else:
            self.__doAreaAttack()

    def b_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.d_setBossDamage(bossDamage, recoverRate, recoverStartTime)
        self.setBossDamage(bossDamage, recoverRate, recoverStartTime)

    def setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        self.bossDamage = bossDamage
        self.recoverRate = recoverRate
        self.recoverStartTime = recoverStartTime

    def getBossDamage(self):
        now = globalClock.getFrameTime()
        elapsed = now - self.recoverStartTime
        return int(max(self.bossDamage - self.recoverRate * elapsed / 60.0, 0))

    def d_setBossDamage(self, bossDamage, recoverRate, recoverStartTime):
        timestamp = globalClockDelta.localToNetworkTime(recoverStartTime)
        self.sendUpdate('setBossDamage', [bossDamage, recoverRate, timestamp])

    def waitForNextStrafe(self, delayTime):
        currState = self.getCurrentOrNextState()
        if currState == 'BattleThree':
            taskName = self.uniqueName('NextStrafe')
            taskMgr.remove(taskName)
            taskMgr.doMethodLater(delayTime, self.doNextStrafe, taskName)

    def stopStrafes(self):
        taskName = self.uniqueName('NextStrafe')
        taskMgr.remove(taskName)

    def doNextStrafe(self, task):
        if self.attackCode != ToontownGlobals.BossCogDizzyNow:
            side = random.choice([0, 1])
            direction = random.choice([0, 1])
            self.sendUpdate('doStrafe', [side, direction])
        delayTime = 9
        self.waitForNextStrafe(delayTime)

    def __sendDooberIds(self):
        dooberIds = []
        for suit in self.doobers:
            dooberIds.append(suit.doId)

        self.sendUpdate('setDooberIds', [dooberIds])

    def d_cagedToonBattleThree(self, index, avId):
        self.sendUpdate('cagedToonBattleThree', [index, avId])

    def formatReward(self):
        return str(self.cagedToonNpcId)

    def makeBattleOneBattles(self):
        self.postBattleState = 'RollToBattleTwo'
        self.initializeBattles(1, ToontownGlobals.SellbotBossBattleOnePosHpr)

    def generateSuits(self, battleNumber):
        if battleNumber == 1:
            return self.invokeSuitPlanner(9, 0)
        else:
            return self.invokeSuitPlanner(10, 1)

    def removeToon(self, avId):
        toon = simbase.air.doId2do.get(avId)
        if toon:
            toon.b_setNumPies(0)
        DistributedBossCogAI.DistributedBossCogAI.removeToon(self, avId)

    def enterOff(self):
        DistributedBossCogAI.DistributedBossCogAI.enterOff(self)
        self.__resetDoobers()

    def enterElevator(self):
        DistributedBossCogAI.DistributedBossCogAI.enterElevator(self)
        self.b_setBossDamage(0, 0, 0)

    def enterIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.enterIntroduction(self)
        self.__makeDoobers()
        self.b_setBossDamage(0, 0, 0)

    def exitIntroduction(self):
        DistributedBossCogAI.DistributedBossCogAI.exitIntroduction(self)
        self.__resetDoobers()

    def enterRollToBattleTwo(self):
        self.divideToons()
        self.barrier = self.beginBarrier('RollToBattleTwo', self.involvedToons, 45, self.__doneRollToBattleTwo)

    def __doneRollToBattleTwo(self, avIds):
        self.b_setState('PrepareBattleTwo')

    def exitRollToBattleTwo(self):
        self.ignoreBarrier(self.barrier)

    def enterPrepareBattleTwo(self):
        self.barrier = self.beginBarrier('PrepareBattleTwo', self.involvedToons, 30, self.__donePrepareBattleTwo)
        self.makeBattleTwoBattles()

    def __donePrepareBattleTwo(self, avIds):
        self.b_setState('BattleTwo')

    def exitPrepareBattleTwo(self):
        self.ignoreBarrier(self.barrier)

    def makeBattleTwoBattles(self):
        self.postBattleState = 'PrepareBattleThree'
        self.initializeBattles(2, ToontownGlobals.SellbotBossBattleTwoPosHpr)

    def enterBattleTwo(self):
        if self.battleA:
            self.battleA.startBattle(self.toonsA, self.suitsA)
        if self.battleB:
            self.battleB.startBattle(self.toonsB, self.suitsB)

    def exitBattleTwo(self):
        self.resetBattles()

    def enterPrepareBattleThree(self):
        self.barrier = self.beginBarrier('PrepareBattleThree', self.involvedToons, 30, self.__donePrepareBattleThree)

    def __donePrepareBattleThree(self, avIds):
        self.b_setState('BattleThree')

    def exitPrepareBattleThree(self):
        self.ignoreBarrier(self.barrier)

    def enterBattleThree(self):
        self.resetBattles()
        self.setPieType()
        self.b_setBossDamage(0, 0, 0)
        self.battleThreeStart = globalClock.getFrameTime()
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.__touchedCage = 0

        self.waitForNextAttack(5)
        self.waitForNextStrafe(9)
        self.cagedToonDialogIndex = 100
        self.__saySomethingLater()

    def __saySomething(self, task = None):
        index = None
        avId = 0
        if len(self.involvedToons) == 0:
            return
        avId = random.choice(self.involvedToons)
        toon = simbase.air.doId2do.get(avId)
        if toon.__touchedCage:
            if self.cagedToonDialogIndex <= TTLocalizer.CagedToonBattleThreeMaxAdvice:
                index = self.cagedToonDialogIndex
                self.cagedToonDialogIndex += 1
            elif random.random() < 0.2:
                index = random.randrange(100, TTLocalizer.CagedToonBattleThreeMaxAdvice + 1)
        else:
            index = random.randrange(20, TTLocalizer.CagedToonBattleThreeMaxTouchCage + 1)
        if index:
            self.d_cagedToonBattleThree(index, avId)
        self.__saySomethingLater()
        return

    def __saySomethingLater(self, delayTime = 15):
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)
        taskMgr.doMethodLater(delayTime, self.__saySomething, taskName)

    def __goodJump(self, avId):
        currState = self.getCurrentOrNextState()
        if currState != 'BattleThree':
            return
        index = random.randrange(10, TTLocalizer.CagedToonBattleThreeMaxGivePies + 1)
        self.d_cagedToonBattleThree(index, avId)
        self.__saySomethingLater()

    def exitBattleThree(self):
        self.stopAttacks()
        self.stopStrafes()
        taskName = self.uniqueName('CagedToonSaySomething')
        taskMgr.remove(taskName)

    def enterNearVictory(self):
        self.resetBattles()

    def exitNearVictory(self):
        pass

    def enterVictory(self):
        self.resetBattles()
        self.suitsKilled.append({'type': None,
         'level': None,
         'track': self.dna.dept,
         'isSkelecog': 0,
         'isForeman': 0,
         'isVP': 1,
         'isCFO': 0,
         'isSupervisor': 0,
         'isVirtual': 0,
         'activeToons': self.involvedToons[:]})
        self.barrier = self.beginBarrier('Victory', self.involvedToons, 10, self.__doneVictory)
        return

    def __doneVictory(self, avIds):
        self.d_setBattleExperience()
        self.b_setState('Reward')
        BattleExperienceAI.assignRewards(self.involvedToons, self.toonSkillPtsGained, self.suitsKilled, ToontownGlobals.dept2cogHQ(self.dept), self.helpfulToons)
        for toonId in self.involvedToons:
            toon = self.air.doId2do.get(toonId)
            if toon:
                if not toon.attemptAddNPCFriend(self.cagedToonNpcId, numCalls=1):
                    self.notify.info('%s.unable to add NPCFriend %s to %s.' % (self.doId, self.cagedToonNpcId, toonId))
                toon.b_promote(self.deptIndex)

    def exitVictory(self):
        self.takeAwayPies()

    def enterFrolic(self):
        DistributedBossCogAI.DistributedBossCogAI.enterFrolic(self)
        self.b_setBossDamage(0, 0, 0)

    def __resetDoobers(self):
        for suit in self.doobers:
            suit.requestDelete()

        self.doobers = []

    def __makeDoobers(self):
        self.__resetDoobers()
        for i in xrange(8):
            suit = DistributedSuitAI.DistributedSuitAI(self.air, None)
            level = random.randrange(len(SuitDNA.suitsPerLevel))
            suit.dna = SuitDNA.SuitDNA()
            suit.dna.newSuitRandom(level=level, dept=self.dna.dept)
            suit.setLevel(level)
            suit.generateWithRequired(self.zoneId)
            self.doobers.append(suit)

        self.__sendDooberIds()
        return

    def setPieType(self):
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.d_setPieType(4)

    def takeAwayPies(self):
        for toonId in self.involvedToons:
            toon = simbase.air.doId2do.get(toonId)
            if toon:
                toon.b_setNumPies(0)

    def __recordHit(self):
        now = globalClock.getFrameTime()
        self.hitCount += 1
        if self.hitCount < self.limitHitCount or self.bossDamage < self.hitCountDamage:
            return
        self.b_setAttackCode(ToontownGlobals.BossCogRecoverDizzyAttack)

    def enterReward(self):
        DistributedBossCogAI.DistributedBossCogAI.enterReward(self)

@magicWord(category=CATEGORY_ADMINISTRATOR)
def skipVP():
    """
    Skips to the final round of the VP.
    """
    invoker = spellbook.getInvoker()
    boss = None
    for do in simbase.air.doId2do.values():
        if isinstance(do, DistributedSellbotBossAI):
            if invoker.doId in do.involvedToons:
                boss = do
                break
    if not boss:
        return "You aren't in a VP!"
    if boss.state_ in ('PrepareBattleThree', 'BattleThree'):
        return "You can't skip this round."
    boss.exitIntroduction()
    boss.b_setState('PrepareBattleThree')
    return 'Skipping the first round...'

@magicWord(category=CATEGORY_ADMINISTRATOR)
def killVP():
    """
    Kills the VP.
    """
    invoker = spellbook.getInvoker()
    boss = None
    for do in simbase.air.doId2do.values():
        if isinstance(do, DistributedSellbotBossAI):
            if invoker.doId in do.involvedToons:
                boss = do
                break
    if not boss:
        return "You aren't in a VP!"
    boss.b_setState('Victory')
    return 'Killed VP.'
