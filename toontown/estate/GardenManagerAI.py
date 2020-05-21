from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram

from toontown.estate import GardenGlobals
from toontown.estate.DistributedAnimatedStatuaryAI import DistributedAnimatedStatuaryAI
from toontown.estate.DistributedChangingStatuaryAI import DistributedChangingStatuaryAI
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
    GardenGlobals.AnimatedStatuaryPlot: DistributedAnimatedStatuaryAI
}


class GardenManagerAI:
    notify = directNotify.newCategory('GardenManagerAI')

    def __init__(self, air, house):
        self.air = air
        self.house = house

        self.plots = []

    def loadGarden(self):
        if not self.house.hasGardenData():
            print ("We dont have a garden yet!!!")
            self.createBlankGarden()
            return

        print ("creating garden from data")
        self.createGardenFromData(self.house.getGardenData())
        self.giveOrganicBonus()



    def createBlankGarden(self):
        data = []

        plots = GardenGlobals.getGardenPlots(self.house.housePos)

        for i, plotData in enumerate(plots):
            print (i, plotData)

            holdingList = []
            holdingList.append(GardenGlobals.EmptyPlot)
            holdingList.append(i)
            data.append(holdingList)

        myPickledGarden = pickle.dumps(data)

        # Sends gatden data to clients
        self.house.b_setGardenData(myPickledGarden)
        self.loadGarden()

















    def createGardenFromData(self, gardenData):


        myGarden = pickle.loads(gardenData)
        print (myGarden)

        plotCount = len(myGarden)# First thing in the list is the number of plots

        tmpGardenLoop = myGarden.copy() # Make copy of list to use in our for loop

        for x in range(plotCount):


            curPlot = tmpGardenLoop[x]
            occupier = tmpGardenLoop[x][0] # Type to generate

            if occupier not in occupier2Class:
                print ("value not in occupier")
                continue

            plot = occupier2Class[occupier](self.air, self, self.house.housePos)
            plot.construct(curPlot)
            plot.generateWithRequired(self.house.zoneId)

            self.plots.append(plot)




    def updateGardenData(self):

        rawGardenData = []

        plotCount = len(self.plots)


        for plot in self.plots:
            gardenPlot = []


            occupier = plot.occupier
            plotIndex = plot.plotIndex

            try:
                typeIndex = plot.typeIndex # Type of gag tree?  
                waterLevel = plot.waterLevel
                growthLevel = plot.growthLevel
                timestamp = plot.timestamp
                wilted = plot.wilted
            except:
                typeIndex = 0
                waterLevel = 0
                growthLevel = 0
                timestamp = 0
                wilted = 0
                print ("we dont have these attributes")


            try:
            
                gardenPlot.append(occupier)
                gardenPlot.append(plotIndex)
                gardenPlot.append(typeIndex)
                gardenPlot.append(waterLevel)
                gardenPlot.append(growthLevel)
                gardenPlot.append(timestamp)
                gardenPlot.append(wilted)


            except:
                gardenPlot.append(occupier)
                gardenPlot.append(plotIndex)

            rawGardenData.append(gardenPlot)

            



        print (rawGardenData, "WHAT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!??????? UPDATE GARDEN DATA")
        myPickledGarden = pickle.dumps(rawGardenData)
        self.house.b_setGardenData(myPickledGarden)




        #gardenData = PyDatagram()

        #gardenData.addUint8(len(self.plots))
        #for plot in self.plots:
        #    plot.pack(gardenData)

        #self.house.b_setGardenData(gardenData.getMessage())



    def delete(self):
        for plot in self.plots:
            plot.requestDelete()

    def getTimestamp(self):
        return int(time())

    def constructTree(self, plotIndex, gagTrack, gagLevel):
        dg = PyDatagram()
        dg.addUint8(plotIndex)
        dg.addUint8(GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel))  # Type Index
        dg.addInt8(0)  # Water Level
        dg.addInt8(0)  # Growth Level
        dg.addUint32(self.getTimestamp())
        dg.addUint8(0)  # Wilted State (False)

        gardenData = [0, plotIndex, GardenGlobals.getTreeTypeIndex(gagTrack, gagLevel), 0, 0, self.getTimestamp(), 0]












        plot = occupier2Class[GardenGlobals.TreePlot](self.air, self, self.house.housePos)
        plot.construct(gardenData, 1) # 1 is for the type
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
