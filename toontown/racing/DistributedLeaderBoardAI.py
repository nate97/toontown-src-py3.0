from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.uberdog.DataStore import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.racing import RaceGlobals



class DistributedLeaderBoardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLeaderBoardAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air
        self.boardPos = [0,0,0,0,0,0]
        self.genre = RaceGlobals.Speedway # Default genre


    def generate(self):
        self.defineLeaderboard()


    def defineLeaderboard(self): # Sends over genre and instance of this leaderboard to the leaderboard manager
        self.air.leaderBoardMgr.defineBoardInstance(self.genre, self)


    def setDisplay(self, display=""):
        trackTitle = display[0]
        recordTitle = display[1]
        currentScores = display[2]

        test = {"name": trackTitle, "scoreType": recordTitle, "scores": currentScores}
        pData = cPickle.dumps(test)
        self.display = pData

        self.sendUpdate('setDisplay', [self.display])


    def getDisplay(self):
        return self.display


    def setGenre(self, genre):
        self.genre = genre


    def getGenre(self):
        return self.genre


    def setPosHpr(self, x, y, z, h, p, r):
        self.boardPos = [x, y, z, h, p, r]
        self.sendUpdate('setPosHpr', self.boardPos)


    def getPosHpr(self):
        return self.boardPos



