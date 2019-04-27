import pickle
import random

from . import ToonInterior
from . import ToonInteriorColors
from . import LegacyInteriorLoader
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from direct.interval.IntervalGlobal import *
from otp.speedchat import SpeedChatGlobals
from panda3d.core import *
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from toontown.toon import ToonDNA
from toontown.toon import ToonHead
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from toontown.toonbase import ToontownGlobals
from toontown.toonbase.ToonBaseGlobal import *


SIGN_LEFT = -4
SIGN_RIGHT = 4
SIGN_BOTTOM = -3.5
SIGN_TOP = 1.5
FrameScale = 1.4

INTERIOR_ITEM_LIST = 0
COLOR_LIST = 1
DOOR_LIST = 2


class DistributedToonInterior(DistributedObject.DistributedObject, LegacyInteriorLoader.LegacyInteriorLoader):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        LegacyInteriorLoader.LegacyInteriorLoader.__init__(self) # Initalize legacy loader
        self.fsm = ClassicFSM.ClassicFSM('DistributedToonInterior', [State.State('toon', self.enterToon, self.exitToon, ['beingTakenOver']), State.State('beingTakenOver', self.enterBeingTakenOver, self.exitBeingTakenOver, []), State.State('off', self.enterOff, self.exitOff, [])], 'toon', 'off')
        self.fsm.enterInitialState()

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

    def disable(self):
        self.interior.removeNode()
        del self.interior
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.disable(self)

    def delete(self):
        del self.fsm
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
        DistributedObject.DistributedObject.delete(self)

    def produceDNAItem(self, category, findFunc): # This is was created in order to produce the same building interior's that Python2 produces, Py3 changed what random seeds produce.
        index = self.interiorItemList.pop() # Pop off value we want
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def randomDNAItem(self, category, findFunc):
        codeCount = self.dnaStore.getNumCatalogCodes(category)
        index = self.randomGenerator.randint(0, codeCount - 1)
        code = self.dnaStore.getCatalogCode(category, index)
        return findFunc(code)

    def replaceRandomInModel(self, model):
        baseTag = 'random_'
        npc = model.findAllMatches('**/' + baseTag + '???_*')
        for i in range(npc.getNumPaths()):
            np = npc.getPath(i)
            name = np.getName()
            b = len(baseTag)
            category = name[b + 4:]
            key1 = name[b]
            key2 = name[b + 1]
            if key1 == 'm':

                if not self.randomBldg: # Building is not random
                    model = self.produceDNAItem(category, self.dnaStore.findNode)
                else: # Building is random
                    model = self.randomDNAItem(category, self.dnaStore.findNode)   

                newNP = model.copyTo(np)
                c = render.findAllMatches('**/collision')
                c.stash()
                if key2 == 'r':
                    self.replaceRandomInModel(newNP)
            elif key1 == 't':

                if not self.randomBldg: # Building is not random
                    texture = self.produceDNAItem(category, self.dnaStore.findTexture)
                else: # Building is random
                    texture = self.randomDNAItem(category, self.dnaStore.findTexture)

                np.setTexture(texture, 100)
                newNP = np
            if key2 == 'c':
                if category == 'TI_wallpaper' or category == 'TI_wallpaper_border': # Specified category

                    if not self.randomBldg: # Building is not random
                        colorIndex = self.interiorColorList.pop() # Pop off value we want
                        cColor = self.colors[category][colorIndex]

                    else: # Building is random
                        self.randomGenerator.seed(self.strZoneId)
                        cColor = self.randomGenerator.choice(self.colors[category])
                    newNP.setColorScale(cColor) # Set color of object

                else: # Wasn't specified category

                    if not self.randomBldg: # Building is not random
                        colorIndex = self.interiorColorList.pop() # Pop off value we want
                        cColor = self.colors[category][colorIndex]

                    else: # Building is random
                        self.randomGenerator.seed(self.strZoneId)
                        cColor = self.randomGenerator.choice(self.colors[category])
                    newNP.setColorScale(cColor) # Set color of object

    def setup(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.randomBldg = False
        self.strZoneId = str(self.zoneId)

        seedDict = self.loadBinInteriors() # Open bin file with legacy loader

        if self.strZoneId in seedDict: # Building is predefined
            self.interiorItemList = (seedDict[self.strZoneId][INTERIOR_ITEM_LIST])
            self.interiorColorList = (seedDict[self.strZoneId][COLOR_LIST])
            self.interiorDoorColorList = (seedDict[self.strZoneId][DOOR_LIST])
        else: # Building not in predefined seed dict
            self.randomBldg = True
            self.randomGenerator = random.Random()
            self.randomGenerator.seed(self.strZoneId)

        if not self.randomBldg: # Building is not random
            interior = self.produceDNAItem('TI_room', self.dnaStore.findNode)
        else: # Building is random
            interior = self.randomDNAItem('TI_room', self.dnaStore.findNode)

        self.interior = interior.copyTo(render)
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        door_origin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(door_origin)
        door_origin.setScale(0.8, 0.8, 0.8)
        door_origin.setPos(door_origin, 0, -0.025, 0)

        if not self.randomBldg: # Building is not random
            colorList = self.colors['TI_door']
            colorIndex = self.interiorDoorColorList.pop() # Pop off value we want
            color = colorList[colorIndex]
        else: # Building is random
            colorList = self.colors['TI_door']
            color = self.randomGenerator.choice(colorList)

        DNADoor.setupDoor(doorNP, self.interior, door_origin, self.dnaStore, str(self.block), color)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(color)
        sign = hidden.find('**/tb%s:*_landmark_*_DNARoot/**/sign_origin;+s' % (self.block))
        if not sign.isEmpty():
            signOrigin = self.interior.find('**/sign_origin;+s')
            newSignNP = sign.copyTo(signOrigin)
            newSignNP.setDepthWrite(1, 1)
            mat = self.dnaStore.getSignTransformFromNodePath(self.interior)
            inv = Mat4(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
            inv.invertFrom(mat)
            newSignNP.setMat(inv)
            newSignNP.flattenLight()
            ll = Point3()
            ur = Point3()
            newSignNP.calcTightBounds(ll, ur)
            width = ur[0] - ll[0]
            height = ur[2] - ll[2]
            if width != 0 and height != 0:
                xScale = (SIGN_RIGHT - SIGN_LEFT) / width
                zScale = (SIGN_TOP - SIGN_BOTTOM) / height
                scale = min(xScale, zScale)
                xCenter = (ur[0] + ll[0]) / 2.0
                zCenter = (ur[2] + ll[2]) / 2.0
                newSignNP.setPosHprScale((SIGN_RIGHT + SIGN_LEFT) / 2.0 - xCenter * scale, -0.1, (SIGN_TOP + SIGN_BOTTOM) / 2.0 - zCenter * scale, 0.0, 0.0, 0.0, scale, scale, scale)
        trophyOrigin = self.interior.find('**/trophy_origin')
        trophy = self.buildTrophy()
        if trophy:
            trophy.reparentTo(trophyOrigin)

        del self.colors
        del self.dnaStore
        del self.strZoneId
        del self.randomBldg

        if getattr(self, "randomGenerator", None):
            del self.randomGenerator

        if getattr(self, "interiorItemList", None):
            del self.interiorItemList

        if getattr(self, "interiorColorList", None):
            del self.interiorColorList

        if getattr(self, "interiorDoorColorList", None):
            del self.interiorDoorColorList

        self.interior.flattenMedium()
        for npcToon in self.cr.doFindAllInstances(DistributedNPCToonBase):
            npcToon.initToonState()

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def setToonData(self, toonData):
        savedBy = pickle.loads(toonData)
        self.savedBy = savedBy

    def buildTrophy(self):
        if self.savedBy == None:
            return
        numToons = len(self.savedBy)
        pos = 1.25 - 1.25 * numToons
        trophy = hidden.attachNewNode('trophy')
        for avId, name, dnaTuple in self.savedBy:
            frame = self.buildFrame(name, dnaTuple)
            frame.reparentTo(trophy)
            frame.setPos(pos, 0, 0)
            pos += 2.5

        return trophy

    def buildFrame(self, name, dnaTuple):
        frame = loader.loadModel('phase_3.5/models/modules/trophy_frame')
        dna = ToonDNA.ToonDNA()
        dna.newToonFromProperties(*dnaTuple)
        head = ToonHead.ToonHead()
        head.setupHead(dna)
        head.setPosHprScale(0, -0.05, -0.05, 180, 0, 0, 0.55, 0.02, 0.55)
        if dna.head[0] == 'r':
            head.setZ(-0.15)
        elif dna.head[0] == 'h':
            head.setZ(0.05)
        elif dna.head[0] == 'm':
            head.setScale(0.45, 0.02, 0.45)
        head.reparentTo(frame)
        nameText = TextNode('trophy')
        nameText.setFont(ToontownGlobals.getToonFont())
        nameText.setAlign(TextNode.ACenter)
        nameText.setTextColor(0, 0, 0, 1)
        nameText.setWordwrap(5.36 * FrameScale)
        nameText.setText(name)
        namePath = frame.attachNewNode(nameText.generate())
        namePath.setPos(0, -0.03, -.6)
        namePath.setScale(0.186 / FrameScale)
        frame.setScale(FrameScale, 1.0, FrameScale)
        return frame

    def setState(self, state, timestamp):
        self.fsm.request(state, [globalClockDelta.localElapsedTime(timestamp)])

    def enterOff(self):
        pass

    def exitOff(self):
        pass

    def enterToon(self):
        pass

    def exitToon(self):
        pass

    def enterBeingTakenOver(self, ts):
        messenger.send('clearOutToonInterior')

    def exitBeingTakenOver(self):
        pass
