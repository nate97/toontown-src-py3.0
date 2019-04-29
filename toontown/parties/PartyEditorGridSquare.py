from panda3d.core import Vec3, Vec4, Point3, TextNode, VBase4
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectScrolledList, DirectCheckButton
from direct.gui import DirectGuiGlobals
from direct.showbase.DirectObject import DirectObject
from direct.showbase import PythonUtil

from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer
from toontown.parties import PartyGlobals
from toontown.parties.PartyInfo import PartyInfo
from toontown.parties import PartyUtils


class PartyEditorGridSquare(DirectObject):
    notify = directNotify.newCategory('PartyEditorGridSquare')

    def __init__(self, partyEditor, x, y):
        self.partyEditor = partyEditor
        self.x = x
        self.y = y
        self.gridElement = None
        return

    def getPos(self):
        if base.camLens.getAspectRatio() >= 1.6:
            gridBound = PartyGlobals.PartyEditorGridBoundsWS
            gridSize = PartyGlobals.PartyEditorGridSquareSizeWS
        else:
            gridBound = PartyGlobals.PartyEditorGridBounds
            gridSize = PartyGlobals.PartyEditorGridSquareSize
        return Point3(gridBound[0][0] + self.x * gridSize[0] + gridSize[0] / 2.0, 0.0, gridBound[1][1] + (PartyGlobals.PartyEditorGridSize[1] - 1 - self.y) * gridSize[1] + gridSize[1] / 2.0)


    def destroy(self):
        del self.gridElement



