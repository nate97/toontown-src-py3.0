from panda3d.core import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import CImpulse
from otp.movement.PyVec3 import PyVec3
from toontown.pets import PetConstants
import math

import inspect

class PetChase(CImpulse.CImpulse):

    def __init__(self, target = None, minDist = None, moveAngle = None):
        CImpulse.CImpulse.__init__(self)
        self.target = target
        if minDist is None:
            minDist = 5.0
        self.minDist = minDist
        if moveAngle is None:
            moveAngle = 20.0
        self.moveAngle = moveAngle
        self.lookAtNode = NodePath('lookatNode')
        self.lookAtNode.hide()
        self.vel = None
        self.rotVel = None
        return

    def setMinDist(self, minDist):
        self.minDist = minDist

    def getMinDist(self):
        return self.minDist

    def setMoveAngle(self, moveAngle):
        self.moveAngle = moveAngle

    def getMoveAngle(self):
        return self.moveAngle

    def setTarget(self, target):
        self.target = target

    def getTarget(self):
        if self.target: 
            return self.target
        else:
            return self.nodePath

    def destroy(self):
        self.lookAtNode.removeNode()
        del self.lookAtNode
        del self.target
        del self.vel
        del self.rotVel

    def setMover(self, mover):
        CImpulse.CImpulse.setMover(self, mover)
        self.lookAtNode.reparentTo(self.nodePath)
        self.vel = LVecBase3f(0,0,0)
        self.rotVel = LVecBase3f(0,0,0)

    def process(self, dt):
        print "Chase"
        CImpulse.CImpulse.process(self, dt)
        me = self.nodePath
        target = self.target
        targetPos = target.getPos(me)
        x = targetPos[0]
        y = targetPos[1]
        distance = math.sqrt(x * x + y * y)
        self.lookAtNode.lookAt(target)
        relH = reduceAngle(self.lookAtNode.getH(me))
        epsilon = 0.005
        rotSpeed = PetConstants.RotSpeed

        if relH < -epsilon:
            vH = -rotSpeed
        elif relH > epsilon:
            vH = rotSpeed
        else:
            vH = 0
        if abs(vH * dt) > abs(relH):
            vH = relH / dt

        if distance > self.minDist and abs(relH) < self.moveAngle:
            vForward = self.mover.getFwdSpeed()
        else:
            vForward = 0
        distanceLeft = distance - self.minDist
        if distance > self.minDist and vForward * dt > distanceLeft:
            vForward = distanceLeft / dt


        if vForward:
            self.vel.setY(vForward)
            self.mover.addShove(self.vel)

        if vH:
            self.rotVel.setX(vH)
            self.mover.addRotShove(self.rotVel)














