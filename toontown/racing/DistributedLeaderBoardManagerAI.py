from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import DistributedObjectAI

from toontown.toonbase import TTLocalizer
from toontown.racing import RaceGlobals

import time
import csv
import ast
import os
import io

class DistributedLeaderBoardManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('LeaderBoardManagerAI') # NJF

    def __init__(self, air):

        self.air = air

        # Directory
        self.backDir = 'backups/'
        self.folderName = 'raceboards/'
        self.fileName = str(self.air.districtId) # Used for our filename
        self.extension = '.csv'
        self.fullPath = self.backDir + self.folderName 
        self.fullName = self.fileName + self.extension

        # Leaderboard instances
        self.stadiumBoard = None
        self.ruralBoard = None
        self.urbanBoard = None

        # Name used for default race player
        self.defaultName = "Goofy"

        # How long it takes before we display the next race scores
        self.cycleTime = 10

        # Minimum values dict
        self.minimumValueDict = {
            RaceGlobals.RT_Speedway_1: RaceGlobals.speedway1Minimum,
            RaceGlobals.RT_Speedway_1_rev: RaceGlobals.speedway1Minimum,
            RaceGlobals.RT_Speedway_2: RaceGlobals.speedway2Minimum,
            RaceGlobals.RT_Speedway_2_rev: RaceGlobals.speedway2Minimum,
            RaceGlobals.RT_Rural_1: RaceGlobals.rural1Minimum,
            RaceGlobals.RT_Rural_1_rev: RaceGlobals.rural1Minimum,

            RaceGlobals.RT_Rural_2: RaceGlobals.rural2Minimum,
            RaceGlobals.RT_Rural_2_rev: RaceGlobals.rural2Minimum,
            RaceGlobals.RT_Urban_1: RaceGlobals.urban1Minimum,
            RaceGlobals.RT_Urban_1_rev: RaceGlobals.urban1Minimum,
            RaceGlobals.RT_Urban_2: RaceGlobals.urban2Minimum,
            RaceGlobals.RT_Urban_2_rev: RaceGlobals.urban2Minimum,
        }

        self.orderedTrackKeys = {
            RaceGlobals.Speedway: [(RaceGlobals.RT_Speedway_1, RaceGlobals.Daily),
                    (RaceGlobals.RT_Speedway_1, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Speedway_1, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Speedway_2, RaceGlobals.Daily),
                    (RaceGlobals.RT_Speedway_2, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Speedway_2, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.AllTime)],
            RaceGlobals.Rural: [(RaceGlobals.RT_Rural_1, RaceGlobals.Daily),
                    (RaceGlobals.RT_Rural_1, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Rural_1, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Rural_1_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Rural_1_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Rural_1_rev, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Rural_2, RaceGlobals.Daily),
                    (RaceGlobals.RT_Rural_2, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Rural_2, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Rural_2_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Rural_2_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Rural_2_rev, RaceGlobals.AllTime)],
            RaceGlobals.Urban: [(RaceGlobals.RT_Urban_1, RaceGlobals.Daily),
                    (RaceGlobals.RT_Urban_1, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Urban_1, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Urban_1_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Urban_1_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Urban_1_rev, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Urban_2, RaceGlobals.Daily),
                    (RaceGlobals.RT_Urban_2, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Urban_2, RaceGlobals.AllTime),
                    (RaceGlobals.RT_Urban_2_rev, RaceGlobals.Daily),
                    (RaceGlobals.RT_Urban_2_rev, RaceGlobals.Weekly),
                    (RaceGlobals.RT_Urban_2_rev, RaceGlobals.AllTime)]
        }

        self.recordLists = {
            (RaceGlobals.RT_Speedway_1, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Speedway_1, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Speedway_1, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Speedway_1_rev, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Rural_1, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Rural_1, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Rural_1, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Rural_1_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Rural_1_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Rural_1_rev, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Urban_1, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Urban_1, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Urban_1, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Urban_1_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Urban_1_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Urban_1_rev, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Speedway_2, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Speedway_2, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Speedway_2, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Speedway_2_rev, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Rural_2, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Rural_2, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Rural_2, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Rural_2_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Rural_2_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Rural_2_rev, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Urban_2, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Urban_2, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Urban_2, RaceGlobals.AllTime): [],
            (RaceGlobals.RT_Urban_2_rev, RaceGlobals.Daily): [],
            (RaceGlobals.RT_Urban_2_rev, RaceGlobals.Weekly): [],
            (RaceGlobals.RT_Urban_2_rev, RaceGlobals.AllTime): []
        }

        self.stadiumCount = 0
        self.ruralCount = 0
        self.cityCount = 0
        self.countIteratorList = [self.stadiumCount, self.ruralCount, self.cityCount]

        self.createScoreCSV()
        self.leaderBoardTask()



    ###############################################################################################
    ############################### BUILDING OUR DEFAULT DICTIONARY ###############################
    ###############################################################################################

    def createScoreCSV(self):

        if not os.path.exists(self.backDir):
            os.mkdir(self.backDir)

        if not os.path.exists(self.fullPath):
            os.mkdir(self.fullPath)
            self.raceScoresDict = self.createRaceScoreDict()
            self.exportScores(self.raceScoresDict)

        else:

            if not os.path.exists(self.fullPath + self.fullName):
                self.raceScoresDict = self.createRaceScoreDict()
                self.exportScores(self.raceScoresDict)
            else:

                reader = csv.reader(io.open(self.fullPath + self.fullName, 'r'))
                previousScores = {}
                for row in reader:
                    key, value = row

                    key = ast.literal_eval(key)
                    value = ast.literal_eval(value)

                    previousScores[key] = value

                del reader

                if previousScores != {}: # Patch to not overwrite if file ends up being blank
                    self.raceScoresDict = previousScores
                else:
                    self.raceScoresDict = self.createRaceScoreDict()
                    self.exportScores(self.raceScoresDict)



    def exportScores(self, scoreList):
        w = csv.writer(io.open(self.fullPath + self.fullName, 'w'))
        for key, val in list(scoreList.items()):
            w.writerow([key, val])
        del w # Close



    def createRaceScoreDict(self): # Only called if records file is empty!
        boardDict = {}

        allTrackGenres = self.orderedTrackKeys

        for genre in allTrackGenres:
            trackRecords = allTrackGenres[genre]

            for raceKey in trackRecords: # raceKey is used in of itsself as a key in the boardDict
                raceId = raceKey[0]
                recordTitleId = raceKey[1]

                raceScores = self.recordLists[raceKey]
                raceScores = self.setDefaultWins(raceScores, raceId) # Furnish our list with the default race player ( Goofy )
      
                completedList = raceScores # IMPORTANT!!! THIS IS WHERE WE'RE APPENDING NEW STUFF

                boardDict[raceKey] = completedList

        return boardDict



    def setDefaultWins(self, raceScores, raceId):
        for defaultRacer in range(0, 10):
            self.setDefaultRacer(raceScores, raceId)
        return raceScores # Returns furnished list



    def setDefaultRacer(self, raceScores, raceId):
        raceScores.append((self.defaultName, self.minimumValueDict[raceId], 0))



    ###############################################################################################
    ############################### THIS MANAGES OUR BOARD INSTANCES ##############################
    ###############################################################################################

    def defineBoardInstance(self, genre, boardInstance): # This function allows us to define the three different leaderboards for us to control them
        if genre == RaceGlobals.Speedway: # Stadium
            self.stadiumBoard = boardInstance
        elif genre == RaceGlobals.Rural: # Rural
            self.ruralBoard = boardInstance
        elif genre == RaceGlobals.Urban: # Urban
            self.urbanBoard = boardInstance



    def leaderBoardTask(self, task=None):
        if self.ruralBoard: # If all boards have been generated initiate tasks (Rural board is the last to be generated)
            self.cycleBoardMgr(0, self.stadiumBoard)
            self.cycleBoardMgr(1, self.ruralBoard)
            self.cycleBoardMgr(2, self.urbanBoard)

        taskMgr.doMethodLater(self.cycleTime, self.leaderBoardTask, 'leaderBoardTask')



    def cycleBoardMgr(self, genre, boardInstance):
        if self.countIteratorList[genre] >= 12: # If we go over 12, reset ( Cycles 0 through 12 )
            self.countIteratorList[genre] = 0

        activeTracks = self.orderedTrackKeys[genre]
        curTrack = activeTracks[self.countIteratorList[genre]]      

        trackId = curTrack[0]
        recordId = curTrack[1]
        trackScores = self.raceScoresDict[curTrack]

        self.removeAfterXtime(trackId, recordId) # Keeps old entries from accumulating

        trackTitle = TTLocalizer.KartRace_TrackNames[trackId] # Text
        recordTitle = TTLocalizer.RecordPeriodStrings[recordId] # Text
        trackData = (trackTitle, recordTitle, trackScores)

        self.setBoardDisplay(trackData, boardInstance) # Send data back to leader board

        self.countIteratorList[genre] = self.countIteratorList[genre] + 1 # Count up



    def setBoardDisplay(self, trackData, boardInstance):
        boardInstance.setDisplay(trackData) 



    ###########################################################################################################
    ############################### MECHANISMS FOR APPENDING & REMOVING PLAYERS ###############################
    ###########################################################################################################



    def appendNewRaceEntry(self, raceId, recordId, av, totalTime, timeStamp): # Appends new race entry IF they qualify
        minimumTimeRequirement =  self.minimumValueDict[raceId]
        if totalTime >= minimumTimeRequirement:
            return # This player took too long to be displayed on the board!

        scoreList = self.findRaceScoreList(raceId, recordId)

        newRaceEntry = (av, totalTime, timeStamp) # Player's info
        scoreList.append(newRaceEntry) # Append this racer to the leaderboard
        self.sortScores(scoreList) # Sort our scores based off of the total time players took
        scoreList.pop() # Remove player who took the longest
        self.exportScores(self.raceScoresDict)



    def removeAfterXtime(self, raceId, recordId):
        if recordId == RaceGlobals.Daily: # Remove score after 1 day
            addTime = 86400 # 24 Hours
        elif recordId == RaceGlobals.Weekly: # Remove score after 7 days
            addTime = 604800
        else: # Best, DO NOT REMOVE BEST SCORES
            return

        scoreList = self.findRaceScoreList(raceId, recordId)

        tempIterScores = list(scoreList) # This is because of some weirdness that happens if we remove something from the original list when trying to loop through it aswell
        for race in tempIterScores:

            staticTimeStamp = race[2]
            expirationimeStamp = staticTimeStamp + addTime # 24 Hours out from whenever the timestamp was created for ending of race
            currentTime = time.time()

            if staticTimeStamp != 0: # A special case here, this is for the default racer ( Goofy ) So that it doesn't get inadvertantly removed.
                if currentTime >= expirationimeStamp: # If the present time is greater than the experiation, we will remove it
                    scoreList.remove(race) # Remove the race entry
                    self.setDefaultRacer(scoreList, raceId) # Append default racer in place of old entry
                    self.sortScores(scoreList)
                    self.exportScores(self.raceScoresDict)


    def findRaceScoreList(self, raceId, recordId): # Find specified race list we want
        wantedKey = (raceId, recordId)
        for raceKey in self.raceScoresDict:
            raceScores = self.raceScoresDict[raceKey]
    
            iterRaceId = raceKey[0]
            iterTitleId = raceKey[1]

            if raceKey == wantedKey:
                return raceScores



    def sortScores(self, scoreList):
        scoreList.sort(key=lambda player: player[1]) # Sort by time it took to complete race



