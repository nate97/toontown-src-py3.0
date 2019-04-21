from panda3d.core import LVector3f
from . import DNAGroup
from . import DNABattleCell
from . import DNAUtil

class DNAVisGroup(DNAGroup.DNAGroup):
    COMPONENT_CODE = 2

    def __init__(self, name):
        DNAGroup.DNAGroup.__init__(self, name)
        self.visibles = []
        self.suitEdges = []
        self.battleCells = []

    def getVisGroup(self):
        return self

    def addBattleCell(self, battleCell):
        self.battleCells.append(battleCell)

    def addSuitEdge(self, suitEdge):
        self.suitEdges.append(suitEdge)

    def addVisible(self, visible):
        self.visibles.append(visible)

    def getBattleCell(self, i):
        return self.battleCells[i]

    def getNumBattleCells(self):
        return len(self.battleCells)

    def getNumSuitEdges(self):
        return len(self.suitEdges)

    def getNumVisibles(self):
        return len(self.visibles)

    def getSuitEdge(self, i):
        return self.suitEdges[i]

    def getVisibleName(self, i):
        return self.visibles[i]

    def removeBattleCell(self, cell):
        self.battleCells.remove(cell)

    def removeSuitEdge(self, edge):
        self.suitEdges.remove(edge)

    def removeVisible(self, visible):
        self.visibles.remove(visible)

    def makeFromDGI(self, dgi, dnaStorage):
        DNAGroup.DNAGroup.makeFromDGI(self, dgi)

        numEdges = dgi.getUint16()
        for _ in range(numEdges):
            index = dgi.getUint16()
            endPoint = dgi.getUint16()
            self.addSuitEdge(dnaStorage.getSuitEdge(index, endPoint))

        numVisibles = dgi.getUint16()
        for _ in range(numVisibles):
            self.addVisible(DNAUtil.dgiExtractString8(dgi))

        numCells = dgi.getUint16()
        for _ in range(numCells):
            w = dgi.getUint8()
            h = dgi.getUint8()
            x, y, z = [dgi.getInt32() / 100.0 for i in range(3)]
            self.addBattleCell(DNABattleCell.DNABattleCell(w, h, LVector3f(x, y, z)))