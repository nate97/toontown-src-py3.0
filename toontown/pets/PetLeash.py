from panda3d.core import *
from otp.movement import CImpulse

class PetLeash(CImpulse.CImpulse):

    def __init__(self, origin, length):
        CImpulse.CImpulse.__init__(self)
        self.origin = origin
        self.length = length

    def process(self, dt):
        CImpulse.CImpulse.process(self, dt)
        myPos = self.nodePath.getPos()
        myDist = self.VecType(myPos - self.origin.getPos()).length()
        if myDist > self.length:
            excess = myDist - self.length
            shove = self.VecType(myPos)
            shove.normalize()
            shove *= -excess
