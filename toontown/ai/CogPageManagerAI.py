from toontown.suit import SuitDNA
from toontown.shtiker.CogPageGlobals import *

class CogPageManagerAI:

    def toonEncounteredCogs(self, toon, encounteredCogs, zoneId):
        cogs = toon.cogs
        for cog in encounteredCogs:
            if toon.getDoId() in cog['activeToons']:
                cogIndex = SuitDNA.suitHeadTypes.index(cog['type'])

                if cogs[cogIndex] == COG_UNSEEN:
                    cogs[cogIndex] = COG_BATTLED
        toon.b_setCogStatus(cogs)

    def toonKilledCogs(self, toon, killedCogs, zoneId):
        cogCounts = toon.cogCounts
        cogs = toon.cogs
        for cog in killedCogs:
            if cog['isSkelecog'] or cog['isVP'] or cog['isCFO']:
                continue
            if toon.getDoId() in cog['activeToons']:
                deptIndex = SuitDNA.suitDepts.index(cog['track'])
                if toon.buildingRadar[deptIndex] == 1:
                    continue
                cogIndex = SuitDNA.suitHeadTypes.index(cog['type'])
                buildingQuota = COG_QUOTAS[1][cogIndex % SuitDNA.suitsPerDept]
                cogQuota = COG_QUOTAS[0][cogIndex % SuitDNA.suitsPerDept]
                if cogCounts[cogIndex] >= buildingQuota:
                    return
                cogCounts[cogIndex] += 1
                if cogCounts[cogIndex] < cogQuota:
                    cogs[cogIndex] = COG_DEFEATED
                elif cogQuota <= cogCounts[cogIndex] < buildingQuota:
                    cogs[cogIndex] = COG_COMPLETE1
                else:
                    cogs[cogIndex] = COG_COMPLETE2
        toon.b_setCogCount(cogCounts)
        toon.b_setCogStatus(cogs)
        newCogRadar = toon.cogRadar
        newBuildingRadar = toon.buildingRadar
        for dept in xrange(len(SuitDNA.suitDepts)):
            if newBuildingRadar[dept] == 1:
                continue
            cogRadar = 1
            buildingRadar = 1
            for cog in xrange(SuitDNA.suitsPerDept):
                status =  toon.cogs[dept*SuitDNA.suitsPerDept + cog]
                if status != COG_COMPLETE2:
                    buildingRadar = 0
                if status != COG_COMPLETE1 or status != COG_COMPLETE2:
                    cogRadar = 0
            newCogRadar[dept] = cogRadar
            newBuildingRadar[dept] = buildingRadar
        toon.b_setCogRadar(newCogRadar)
        toon.b_setBuildingRadar(newBuildingRadar)