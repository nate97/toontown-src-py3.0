from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from toontown.estate import GardenGlobals
from toontown.estate.DistributedAnimatedStatuaryAI import DistributedAnimatedStatuaryAI
from toontown.estate.DistributedChangingStatuaryAI import DistributedChangingStatuaryAI
from toontown.estate.DistributedGardenBoxAI import DistributedGardenBoxAI
from toontown.estate.DistributedGagTreeAI import DistributedGagTreeAI
from toontown.estate.DistributedGardenPlotAI import DistributedGardenPlotAI
from toontown.estate.DistributedStatuaryAI import DistributedStatuaryAI
from toontown.estate.DistributedToonStatuaryAI import DistributedToonStatuaryAI
from toontown.toonbase.ToontownBattleGlobals import NUM_GAG_TRACKS


from time import time
import pickle

occupier2Class = {
    GardenGlobals.EmptyPlot: DistributedGardenPlotAI,
    GardenGlobals.TreePlot: DistributedGagTreeAI,
    GardenGlobals.StatuaryPlot: DistributedStatuaryAI,
    GardenGlobals.ToonStatuaryPlot: DistributedToonStatuaryAI,
    GardenGlobals.ChangingStatuaryPlot: DistributedChangingStatuaryAI,
    GardenGlobals.AnimatedStatuaryPlot: DistributedAnimatedStatuaryAI,
    GardenGlobals.PlanterBox: DistributedGardenBoxAI
}


class GardenManagerAI:
    notify = directNotify.newCategory('GardenManagerAI')

    def __init__(self, air, house):
        self.air = air
        self.house = house
        self.plots = []


    def loadGarden(self):
        if not self.house.hasGardenData():
            self.createBlankGarden()
            return

        self.createGardenBoxes()
        self.createGardenFromData(self.house.getGardenData())
        self.giveOrganicBonus()


    def createBlankGarden(self):
        data = []

        plots = GardenGlobals.getGardenPlots(self.house.housePos)

        for i, plotData in enumerate(plots):
            holdingList = []
            holdingList.append(GardenGlobals.EmptyPlot)
            holdingList.append(i)
            data.append(holdingList)

        myPickledGarden = pickle.dumps(data)

        # Sends gatden data to clients
        self.house.b_setGardenData(myPickledGarden)
        self.loadGarden()


    def createGardenBoxes(self): # Generates flowerboxes
        occupier = GardenGlobals.PlanterBox
        boxIndex = 0
        boxes = []
        boxDefs = GardenGlobals.estateBoxes[self.house.housePos]
        for x, y, h, boxType in boxDefs:
            gardenData = [occupier, boxIndex, x, y, h, boxType]

            box = occupier2Class[occupier](self.air, self, self.house.housePos)
            box.construct(gardenData)
            box.generateWithRequired(self.house.zoneId)

            boxes.append(box)
            boxIndex += 1

        self.gardenBoxes = boxes


    def createGardenFromData(self, gardenData):
        myGarden = pickle.loads(gardenData)
        boxDefs = GardenGlobals.estateBoxes[self.house.housePos]
        boxDefs = list(boxDefs)
        print (boxDefs, "!!!!!!")

        

        plotCount = len(myGarden)# First thing in the list is the number of plots
        boxInt = 0

        tmpGardenLoop = myGarden.copy() # Make copy of list to use in our for loop

        for x in range(plotCount):

            curPlot = tmpGardenLoop[x]
            occupier = tmpGardenLoop[x][0] # Type of garden object to generate

            if occupier not in occupier2Class:
                continue # Value not in occupier, this isnt any type of gardening object!

            plot = occupier2Class[occupier](self.air, self, self.house.housePos)
            plot.construct(curPlot)

            plotType = plot.plotType
            
            if plotType == 1:
                myPos = boxDefs[boxInt]
                myPos = (myPos[0], myPos[1], myPos[2])


                print (myPos)
                plot.setPosition(myPos)

                boxInt += 1
                if boxInt > 4:
                    boxInt = 0

            plot.generateWithRequired(self.house.zoneId)
            self.plots.append(plot)


    def updateGardenData(self):
        rawGardenData = []
        plotCount = len(self.plots)

        for plot in self.plots:
            gardenPlot = []
            occupier = plot.occupier
            plotIndex = plot.plotIndex

            if isinstance(plot, DistributedGagTreeAI):
                typeIndex = plot.typeIndex # Type of gag tree
                waterLevel = plot.waterLevel
                print ("water level gag tree", waterLevel)
                growthLevel = plot.growthLevel
                timestamp = plot.timestamp
                wilted = plot.wilted

            elif isinstance(plot, DistributedStatuaryAI):
                typeIndex = plot.typeIndex
                waterLevel = 0
                growthLevel = plot.growthLevel
                timestamp = 0 # This needs to be implemented for AdjustingStatuary
                wilted = 0

            else: # Empty plot
                typeIndex = 0
                waterLevel = 0
                growthLevel = 0
                timestamp = 0
                wilted = 0

            gardenPlot.append(occupier)
            gardenPlot.append(plotIndex)
            gardenPlot.append(typeIndex)
            gardenPlot.append(waterLevel)
            gardenPlot.append(growthLevel)
            gardenPlot.append(timestamp)
            gardenPlot.append(wilted)


            rawGardenData.append(gardenPlot)

            
        print (rawGardenData, "Updating garden data!")
        myPickledGarden = pickle.dumps(rawGardenData)
        self.house.b_setGardenData(myPickledGarden) # Write garden data to database


    def delete(self):
        for plot in self.plots:
            plot.requestDelete()


    def getTimestamp(self):
        return int(time())


    def constructTree(self, plotIndex, gagTrack, gagLevel):
        gardenData = [0, plotIndex, GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel), 0, 0, self.getTimestamp(), 0]
        plot = occupier2Class[GardenGlobals.TreePlot](self.air, self, self.house.housePos)
        plot.construct(gardenData)
        self.plots[plotIndex] = plot
        self.updateGardenData()


    def plantingFinished(self, plotIndex):
        plot = self.plots[plotIndex]
        plot.generateWithRequired(self.house.zoneId)
        itemType = plot.typeIndex
        plot.setMovie(GardenGlobals.MOVIE_FINISHPLANTING, self.air.getAvatarIdFromSender())

        # These should probably be called in the construction functions
        if isinstance(plot, DistributedGagTreeAI):
            av = self.air.doId2do.get(self.house.avatarId)
            if not av:
                return

            self.givePlantingSkill(self.air.getAvatarIdFromSender(), plot.gagLevel)

            av.inventory.useItem(plot.gagTrack, plot.gagLevel) # Take away 1 of the used gag type
            av.b_setInventory(av.inventory.makeNetString())


        if isinstance(plot, DistributedStatuaryAI):
            av = self.air.doId2do.get(self.house.avatarId)
            if not av:
                return

            av.removeGardenItemAdjusted(itemType, 1) # Remove special garden item

            # Take away money based on recipe length
            allRecipes = GardenGlobals.Recipes
            for recp in allRecipes:
                tmpRecipe = allRecipes[recp]
                recipeType = tmpRecipe['special']

                if recipeType == itemType - 100: # This is for statuarys, and probably would likely need to be adjusted for DistributedFlower type
                    beanRecipe = tmpRecipe['beans']
                    beanCount = len(beanRecipe)
                    av.takeMoney(beanCount) # Takes away how many jellybeans it took to create plant/statuary



    def constructStatuary(self, plotIndex, typeIndex):
        occupier = GardenGlobals.StatuaryPlot
        if typeIndex in GardenGlobals.ChangingStatuaryTypeIndices:
            occupier = GardenGlobals.ChangingStatuaryPlot
        elif typeIndex in GardenGlobals.AnimatedStatuaryTypeIndices:
            occupier = GardenGlobals.AnimatedStatuaryPlot

        gardenData = [occupier, plotIndex, typeIndex, 0, 0, self.getTimestamp(), 0]

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
        plot = occupier2Class[GardenGlobals.EmptyPlot](self.air, self, self.house.housePos)
        emptyPlot = [0,plotIndex,0,0,0,0,0]
        plot.construct(emptyPlot)
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
        treesGrown = {i: [] for i in range(NUM_GAG_TRACKS)}

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
