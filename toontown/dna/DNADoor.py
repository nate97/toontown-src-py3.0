from panda3d.core import LVector4f, DecalEffect, NodePath
import DNAGroup
import DNAError
import DNAUtil

class DNADoor(DNAGroup.DNAGroup):
    COMPONENT_CODE = 17

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.code = ''
        self.color = LVector4f(1, 1, 1, 1)

    def setCode(self, code):
        self.code = code

    def getCode(self):
        return self.code

    def setColor(self, color):
        self.color = color

    def getColor(self):
        return self.color

    @staticmethod
    def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
        doorNodePath.setPosHprScale(doorOrigin, (0, 0, 0), (0, 0, 0), (1, 1, 1))
        doorNodePath.setColor(color, 0)

        doorFlat = doorNodePath.find('door_*_flat')
        doorFlat.flattenStrong()
        #doorFlat.setDepthOffset(1) # Can cause building shadows to not properly show up on the doors...
        doorFlat.setEffect(DecalEffect.make())

        leftHole = doorNodePath.find('door_*_hole_left')
        leftHole.flattenStrong()
        leftHole.setName('doorFrameHoleLeft')
        leftHole.wrtReparentTo(doorFlat, 0)
        leftHole.hide()
        leftHole.setColor((0, 0, 0, 1), 0)

        rightHole = doorNodePath.find('door_*_hole_right')
        rightHole.flattenStrong()
        rightHole.setName('doorFrameHoleRight')
        rightHole.wrtReparentTo(doorFlat, 0)
        rightHole.hide()
        rightHole.setColor((0, 0, 0, 1), 0)

        leftDoor = doorNodePath.find('door_*_left')
        leftDoor.flattenStrong()
        leftDoor.setName('leftDoor')
        leftDoor.hide()
        leftDoor.wrtReparentTo(parentNode, 0)
        leftDoor.setColor(color, 0)

        rightDoor = doorNodePath.find('door_*_right')
        rightDoor.flattenStrong()
        rightDoor.setName('rightDoor')
        rightDoor.hide()
        rightDoor.wrtReparentTo(parentNode, 0)
        rightDoor.setColor(color, 0)

        doorTrigger = doorNodePath.find('door_*_trigger')
        doorTrigger.setScale(2, 2, 2)
        doorTrigger.wrtReparentTo(parentNode, 0)
        doorTrigger.setName('door_trigger_' + block)

        if not dnaStore.getDoorPosHprFromBlockNumber(block):
            dnaStore.storeBlockDoor(block, doorOrigin)

        doorNodePath.flattenMedium()

    def makeFromDGI(self, dgi):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)
        self.code = DNAUtil.dgiExtractString8(dgi)
        self.color = DNAUtil.dgiExtractColor(dgi)

    def traverse(self, nodePath, dnaStorage):
        frontNode = nodePath.find('**/*_front')
        if not frontNode.getNode(0).isGeomNode():
            frontNode = frontNode.find('**/+GeomNode')
        frontNode.setEffect(DecalEffect.make())
        node = dnaStorage.findNode(self.code)
        if node is None:
            raise DNAError.DNAError('DNADoor code ' + self.code + ' not found in DNAStorage')
        doorNode = node.copyTo(frontNode, 0)
        doorNode.flattenMedium()
        block = dnaStorage.getBlock(nodePath.getName())
        DNADoor.setupDoor(doorNode, nodePath, nodePath.find('**/*door_origin'), dnaStorage, block, self.getColor())
