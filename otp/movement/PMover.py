from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from panda3d.ai import *
from direct.task import Task

from toontown.pets import PetConstants
import math
class PMover:
    notify = DirectNotifyGlobal.directNotify.newCategory('PMover')
    SerialNum = 0
    Profile = 1
    render = NodePath('render')
    nullTarget = NodePath('nullTargetNodepath')
    nullTarget.setPos(1000)

    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        self.serialNum = PMover.SerialNum
        PMover.SerialNum += 1 # Identification number of doodle

        self.objNodePath = objNodePath # Doodle nodepath

        self.VecType = Vec3(0, 0, 0)
        self.dt = 1.0
        self.dtClock = globalClock.getFrameTime()
        self.shove = Vec3(0, 0, 0)
        self.rotShove = Vec3(0, 0, 0)
        self.force = Vec3(0, 0, 0)
        self.rotForce = Vec3(0, 0, 0)
        self.cImpulses = {}

        # Pet specific variables
        self.target = PMover.nullTarget # Node doodle follows to or flees from, null untill specified
        self.nullTarget = PMover.nullTarget
        self.petMode = 'unstick'
        self.petLocked = False
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed
        self.minDist = 5
        self.pausedPos = (0,0,0)
        self.intelTaskName = ""
        self.AIWorld = None
        self.AIDoodle = None
        self.AIDoodlebehaviors = None

    def setFwdSpeed(self, fwdSpeed):
        self.fwdSpeed = fwdSpeed
        self.AIDoodle.setMaxForce(self.fwdSpeed) 

    def getFwdSpeed(self):
        return self.fwdSpeed

    def setRotSpeed(self, rotSpeed):
        self.rotSpeed = rotSpeed

    def getRotSpeed(self):
        return self.rotSpeed

    def setMinDist(self, minDist):
        self.minDist = minDist

    def getMinDist(self):
        return self.minDist

    def getNodePath(self): # Gives doodle nodepath
        return self.objNodePath




    def getDt(self):
        return self.dt

    def resetDt(self):
        self.dt = 1.0
        self.dtClock = globalClock.getFrameTime()

    def addImpulse(self, name, cImpulse):
        print(cImpulse)
        if not cImpulse:
            return

        self.removeImpulse(name)
        self.cImpulses[name] = cImpulse
        cImpulse.setMover(self)

    def removeImpulse(self, name):
        if name in self.cImpulses:
            cImpulse = self.cImpulses[name]
            cImpulse.clearMover(self)
            del self.cImpulses[name]
            return True

        return False

    def processImpulses(self, dt = None):
        if not dt:
            dt = self.getDt()
        self.dt = dt

        if self.getDt() == -1.0:
            clockDelta = globalClock.getFrameTime()
            self.dt = clockDelta - self.dtClock
            self.dtClock = clockDelta

        for cImpulse in list(self.cImpulses.values()):
            cImpulse.process(self.getDt())

    def addShove(self, shove):
        self.shove += shove

    def addRotShove(self, rotShove):
        self.rotShove += rotShove

    def addForce(self, force):
        self.force += force

    def addRotForce(self, rotForce):
        self.rotForce += rotForce

    def getCollisionEventName(self):
        return 'moverCollision-%s' % self.serialNum



    def setTarget(self, target = None):
        self.target = target

    def getTarget(self):
        if self.target: 
            return self.target
        else:
            return self.nullTarget


    def lockPet(self):
        self.petLocked = True

    def unlockPet(self):
        self.petLocked = False



    ###################################################################
    ################ Inteligent doodle walker AI       ################
    ###################################################################

    def createInteligentDoodle(self):
        self.AIWorld = AIWorld(PMover.render)
        name = "doodleNP-" + str(self.serialNum)
        self.AIDoodle = AICharacter(name, self.objNodePath, 50, 10, 25)
        
        self.AIWorld.addAiChar(self.AIDoodle)
        self.AIDoodlebehaviors = self.AIDoodle.getAiBehaviors()        


    def inteligentDoodleTask(self, task):
        self.AIWorld.update()
        self.petCollisions()
        return Task.cont


    def startInteligentTask(self):
        self.intelTaskName = "doodleTask-" + str(self.serialNum)
        taskMgr.add(self.inteligentDoodleTask, self.intelTaskName)



    def treeCollision(self):
        return
        nullTargetA = NodePath('AAA')
        nullTargetA.reparentTo(PMover.render)
        nullTargetA.setPos(50, -3, 0)


        targetPos = nullTargetA.getPos(self.objNodePath)
        x = targetPos[0]
        y = targetPos[1]
        stopDistance = math.sqrt(x * x + y * y)
        distanceLeft = abs(stopDistance - self.minDist)
        print(distanceLeft)

        if distanceLeft <= 0.3:
            self.setDoodleMode('stick')



    def setDoodleMode(self, petMode):
        if self.petLocked:
            return # Pet is locked, DON'T DO ANYTHING

        self.AIDoodlebehaviors.pauseAi('all') # Before we do any state changes, pause the AI
        target = self.getTarget() # Target to follow, or target to flee from
        self.petMode = petMode

        if self.petMode == 'stick': # Stops pet and doesn't allow further movement
            self.AIDoodlebehaviors.pauseAi('all')

        elif self.petMode == 'unstick':
            self.AIDoodlebehaviors.resumeAi('all')

        elif self.petMode == 'chase': # This chases a moving target
            self.AIDoodlebehaviors.pursue(target)

        elif self.petMode == 'static_chase': # This makes the pet go to a static target
            self.AIDoodlebehaviors.seek(target)

        elif self.petMode == 'wander':
            self.AIDoodlebehaviors.wander(10, 0, 50, 1.0)

        elif self.petMode == 'flee':
            self.AIDoodlebehaviors.flee(target, 20, 20) # Flee from target



    def stay(self):
        self.setDoodleMode("stick")


    def petCollisions(self):
        # This piece of code is to check the distance between the toon and pet,
        # in order to make sure the doodle does not collide with the toon.

        if not self.objNodePath:
            return

        if not self.target:
            return

        targetPos = self.target.getPos(self.objNodePath)
        x = targetPos[0]
        y = targetPos[1]
        stopDistance = math.sqrt(x * x + y * y)
        distanceLeft = abs(stopDistance - self.minDist)


        # This is incase the toon moves further away, rather than the doodle moving further away
        cX = int(self.objNodePath.getX())
        cY = int(self.objNodePath.getY())
        currentPos = (cX, cY)

        if distanceLeft <= 4:
            if self.pausedPos != currentPos:
                self.setDoodleMode('stick')

                pX = int(self.objNodePath.getX())
                pY = int(self.objNodePath.getY())
                self.pausedPos = (pX, pY)


    def destroy(self):
        print ("Destroy smart doodle")
        taskMgr.remove("doodleTask-" + str(self.serialNum))
        del self.AIDoodle
        del self.AIWorld
