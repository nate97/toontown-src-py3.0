from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from toontown.estate import GardenGlobals
from toontown.estate.DistributedAnimatedStatuaryAI import DistributedAnimatedStatuaryAI
from toontown.estate.DistributedChangingStatuaryAI import DistributedChangingStatuaryAI
from toontown.estate.DistributedGagTreeAI import DistributedGagTreeAI
from toontown.estate.DistributedGardenBoxAI import DistributedGardenBoxAI
from toontown.estate.DistributedGardenPlotAI import DistributedGardenPlotAI
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI
from toontown.estate.DistributedToonStatuaryAI import DistributedToonStatuaryAI
from toontown.toonbase.ToontownBattleGlobals import NUM_GAG_TRACKS

from time import time

occupier2Class = {
    GardenGlobals.EmptyPlot: DistributedGardenPlotAI,
    GardenGlobals.TreePlot: DistributedGagTreeAI,
    GardenGlobals.StatuaryPlot: DistributedStatuaryAI,
    GardenGlobals.ToonStatuaryPlot: DistributedToonStatuaryAI,
    GardenGlobals.ChangingStatuaryPlot: DistributedChangingStatuaryAI,
    GardenGlobals.AnimatedStatuaryPlot: DistributedAnimatedStatuaryAI,
    GardenGlobals.PlanterBox: DistributedGardenBoxAI,
}


class GardenManagerAI:
    notify = directNotify.newCategory('GardenManagerAI')

    def __init__(self, air, house):
        self.air = air
        self.house = house

        self.plots = []
        self.boxes = []


    def loadGarden(self):
        if not self.house.hasGardenData():
            self.createBlankGarden()
            return



        gardenData = self.house.getGardenData()

        self.createFlowerBoxes()

        self.createGardenFromData(gardenData)




        self.giveOrganicBonus()







    def createBlankGarden(self):
        gardenData = PyDatagram()

        plots = GardenGlobals.getGardenPlots(self.house.housePos)
        gardenData.addUint8(len(plots))

        for i, plotData in enumerate(plots):
            gardenData.addUint8(GardenGlobals.EmptyPlot)
            gardenData.addUint8(i)

        self.house.b_setGardenData(gardenData.getMessage())
        self.loadGarden()




















    def createFlowerBoxes(self):

        boxDefs = GardenGlobals.estateBoxes[1]
        for x, y, header, boxType in boxDefs:

            box = occupier2Class[6](self.air, self, self.house.housePos)

            #box.constructBox(6, boxType, x, y, header)
            box.setTypeIndex(boxType)
            print boxType, x, y, header
            print "??????????????????????????????"
            print self.house

            try:
                box.generateWithRequired(self.house.zoneId)
            except:
                pass

            self.boxes.append(box)





























    def createGardenFromData(self, gardenData):
        dg = PyDatagram(gardenData)
        gardenData = PyDatagramIterator(dg)
        plotCount = gardenData.getUint8()
        for _ in xrange(plotCount):
            occupier = gardenData.getUint8()
            if occupier not in occupier2Class:
                continue
            plot = occupier2Class[occupier](self.air, self, self.house.housePos)
            plot.construct(gardenData)
            plot.generateWithRequired(self.house.zoneId)

            self.plots.append(plot)


    def updateGardenData(self):
        gardenData = PyDatagram()

        gardenData.addUint8(len(self.plots))
        for plot in self.plots:
            plot.pack(gardenData)

        self.house.b_setGardenData(gardenData.getMessage())

    def delete(self):
        for plot in self.plots:
            plot.requestDelete()

    def getTimestamp(self):
        return int(time())

    def constructFlower(self, plotIndex, species, variety):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(species)
        dg.addUint16(variety)
        dg.addInt8(0)  # Water Level
        dg.addInt8(0)  # Growth Level
        dg.addUint32(self.getTimestamp())
        dg.addUint8(0)  # Wilted State (False)
        gardenData = PyDatagramIterator(dg)

        plot = occupier2Class[GardenGlobals.FlowerPlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)
        self.plots[plotIndex] = plot

        self.updateGardenData()

    def constructTree(self, plotIndex, gagTrack, gagLevel):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel))  # Type Index
        dg.addInt8(0)  # Water Level
        dg.addInt8(0)  # Growth Level
        dg.addUint32(self.getTimestamp())
        dg.addUint8(0)  # Wilted State (False)
        gardenData = PyDatagramIterator(dg)

        plot = occupier2Class[GardenGlobals.TreePlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)
        self.plots[plotIndex] = plot

        self.updateGardenData()

    def plantingFinished(self, plotIndex):
        plot = self.plots[plotIndex]
        plot.generateWithRequired(self.house.zoneId)
        plot.setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.air.getAvatarIdFromSender())
        if isinstance(plot, DistributedGagTreeAI):
            self.givePlantingSkill(self.air.getAvatarIdFromSender(), plot.gagLevel)

    def constructStatuary(self, plotIndex, typeIndex):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(typeIndex)
        gardenData = PyDatagramIterator(dg)

        occupier = GardenGlobals.StatuaryPlot
        if typeIndex in GardenGlobals.ChangingStatuaryTypeIndices:
            occupier = GardenGlobals.ChangingStatuaryPlot
        elif typeIndex in GardenGlobals.AnimatedStatuaryTypeIndices:
            occupier = GardenGlobals.AnimatedStatuaryPlot

        plot = occupier2Class[occupier](self.air, self, self.house.housePos)
        plot.construct(gardenData)

        self.plots[plotIndex] = plot

        self.updateGardenData()

    def constructToonStatuary(self, plotIndex, typeIndex, dnaCode):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(typeIndex)
        dg.addUint16(dnaCode)
        gardenData = PyDatagramIterator(dg)
        plot = occupier2Class[GardenGlobals.ToonStatuaryPlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)

        self.plots[plotIndex] = plot

        self.updateGardenData()

    def revertToPlot(self, plotIndex):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        gardenData = PyDatagramIterator(dg)

        plot = occupier2Class[GardenGlobals.EmptyPlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)
        self.plots[plotIndex] = plot

        self.updateGardenData()

    def removeFinished(self, plotIndex):
        plot = self.plots[plotIndex]
        plot.generateWithRequired(self.house.zoneId)
        plot.setMovie(GardenGlobals.MOVIE_PLANT_REJECTED, self.air.getAvatarIdFromSender())

    def givePlantingSkill(self, avId, gagLevel):
        av = self.air.doId2do.get(avId)
        if not av:
            return
        currSkill = av.getShovelSkill()
        av.b_setShovelSkill(currSkill + 1 + gagLevel)

    def giveOrganicBonus(self):
        av = self.air.doId2do.get(self.house.avatarId)
        if not av:
            return
        trackBonus = [-1] * NUM_GAG_TRACKS
        treesGrown = {i: [] for i in xrange(NUM_GAG_TRACKS)}

        # Get all the trees that can give organic bonus.
        for plot in self.plots:
            if isinstance(plot, DistributedGagTreeAI):
                if plot.canGiveOrganic():
                    treesGrown[plot.gagTrack].append(plot.gagLevel)

        # Check if we have all previous trees for that track to give the bonus.
        def verify(l):
            if not max(l) == len(l) - 1:
                l.remove(max(l))
                if not l:
                    return
                verify(l)

        for level in treesGrown:
            if not treesGrown[level]:
                continue

            verify(treesGrown[level])

            if not treesGrown[level]:
                continue
            trackBonus[level] = max(treesGrown[level])

        av.b_setTrackBonusLevel(trackBonus)



