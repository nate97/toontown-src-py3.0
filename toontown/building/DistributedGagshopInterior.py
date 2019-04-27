import random

from . import ToonInteriorColors
from . import LegacyInteriorLoader
from direct.distributed import DistributedObject
from direct.directnotify import DirectNotifyGlobal
from toontown.toonbase.ToonBaseGlobal import *
from toontown.toonbase.ToontownGlobals import *
from toontown.toon.DistributedNPCToonBase import DistributedNPCToonBase
from toontown.dna.DNAParser import DNADoor
from toontown.hood import ZoneUtil
from panda3d.core import *


INTERIOR_ITEM_LIST = 0
COLOR_LIST = 1
DOOR_LIST = 2


class DistributedGagshopInterior(DistributedObject.DistributedObject, LegacyInteriorLoader.LegacyInteriorLoader):

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        LegacyInteriorLoader.LegacyInteriorLoader.__init__(self) # Initalize legacy loader
        self.dnaStore = cr.playGame.dnaStore

    def generate(self):
        DistributedObject.DistributedObject.generate(self)

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.setup()

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

    def setZoneIdAndBlock(self, zoneId, block):
        self.zoneId = zoneId
        self.block = block

    def chooseDoor(self):
        doorModelName = 'door_double_round_ul'
        if doorModelName[-1:] == 'r':
            doorModelName = doorModelName[:-1] + 'l'
        else:
            doorModelName = doorModelName[:-1] + 'r'
        door = self.dnaStore.findNode(doorModelName)
        return door

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

        self.interior = loader.loadModel('phase_4/models/modules/gagShop_interior')
        self.interior.reparentTo(render)
        hoodId = ZoneUtil.getCanonicalHoodId(self.zoneId)
        self.colors = ToonInteriorColors.colors[hoodId]
        self.replaceRandomInModel(self.interior)
        door = self.chooseDoor()
        doorOrigin = render.find('**/door_origin;+s')
        doorNP = door.copyTo(doorOrigin)
        doorOrigin.setScale(0.8, 0.8, 0.8)
        doorOrigin.setPos(doorOrigin, 0, -0.025, 0)

        if not self.randomBldg: # Building is not random
            colorList = self.colors['TI_door']
            colorIndex = self.interiorDoorColorList.pop() # Pop off value we want
            doorColor = colorList[colorIndex]
        else: # Building is random
            colorList = self.colors['TI_door']
            doorColor = self.randomGenerator.choice(colorList)

        DNADoor.setupDoor(doorNP, self.interior, doorOrigin, self.dnaStore, str(self.block), doorColor)
        doorFrame = doorNP.find('door_*_flat')
        doorFrame.wrtReparentTo(self.interior)
        doorFrame.setColor(doorColor)
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

    def disable(self):
        self.interior.removeNode()
        del self.interior
        DistributedObject.DistributedObject.disable(self)
