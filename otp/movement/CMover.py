from direct.directnotify import DirectNotifyGlobal
from panda3d.core import *
from otp.movement.PyVec3 import PyVec3

from direct.showbase import PythonUtil
import __builtin__
from direct.task import Task

class CMover:
    notify = DirectNotifyGlobal.directNotify.newCategory('CMover')
    SerialNum = 0
    Profile = 1
    def __init__(self, objNodePath, fwdSpeed=1, rotSpeed=1):
        self.serialNum = CMover.SerialNum
        CMover.SerialNum += 1
        self.objNodePath = objNodePath
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed
        self.VecType = Vec3(0, 0, 0)
        self.dt = 1.0
        self.dtClock = globalClock.getFrameTime()
        self.shove = Vec3(0, 0, 0)
        self.rotShove = Vec3(0, 0, 0)
        self.force = Vec3(0, 0, 0)
        self.rotForce = Vec3(0, 0, 0)
        self.cImpulses = {}

        self.alreadyUSED = False



    def setFwdSpeed(self, fwdSpeed):
        self.fwdSpeed = fwdSpeed

    def getFwdSpeed(self):
        return self.fwdSpeed

    def setRotSpeed(self, rotSpeed):
        self.rotSpeed = rotSpeed

    def getRotSpeed(self):
        return self.rotSpeed

    def getNodePath(self):
        return self.objNodePath

    def getDt(self):
        return self.dt

    def resetDt(self):
        self.dt = 1.0
        self.dtClock = globalClock.getFrameTime()

    def addImpulse(self, name, cImpulse):
        print cImpulse
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

        for cImpulse in self.cImpulses.values():
            cImpulse.process(self.getDt())

    def addShove(self, shove):
        self.shove += shove

    def addRotShove(self, rotShove):
        self.rotShove += rotShove

    def addForce(self, force):
        self.force += force

    def addRotForce(self, rotForce):
        self.rotForce += rotForce

    def integrate(self):
        if not self.objNodePath or self.objNodePath.isEmpty():
            return

        self.shove *= self.getDt()
        print self.shove
        self.objNodePath.setFluidPos(self.objNodePath, self.shove)
        self.rotShove *= self.getDt()
        self.objNodePath.setHpr(self.objNodePath, self.rotShove)
        self.shove = LVecBase3f(0, 0, 0)
        self.rotShove = LVecBase3f(0, 0, 0)

    def getCollisionEventName(self):
        return 'moverCollision-%s' % self.serialNum

    def destroy(self):
        pass





    def move(self, dt = -1, profile = 0):
        if CMover.Profile and not profile:
            
            def func(doMove = self.move):
                for i in xrange(10000):
                    doMove(dt, profile = 1)
                

            #__builtin__.func = func
            #PythonUtil.startProfile(cmd = 'func()', filename = 'profile', sorts = [
            #    'cumulative'], callInfo = 0)
            #del __builtin__.func
            #return None
        
        CMover.processImpulses(self, dt)




