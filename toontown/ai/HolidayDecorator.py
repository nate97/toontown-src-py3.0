from toontown.toonbase import ToontownGlobals
from direct.interval.IntervalGlobal import Parallel, Sequence, Func, Wait
from panda3d.core import Vec4, TransformState, NodePath, TransparencyAttrib

from toontown.dna.DNAParser import *

class HolidayDecorator:

    def __init__(self):
        self.dnaStore = base.cr.playGame.dnaStore
        self.swapIval = None
        return

    def exit(self):
        if self.swapIval is not None and self.swapIval.isPlaying():
            self.swapIval.finish()
        return

    def decorate(self):
        self.updateHoodDNAStore()
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()

    def undecorate(self):
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        #if len(holidayIds) > 0:
            #self.decorate()
            #return
        storageFile = base.cr.playGame.hood.storageDNAFile
        if storageFile:
            loadDNAFile(self.dnaStore, storageFile)
        self.swapIval = self.getSwapVisibleIval()
        if self.swapIval:
            self.swapIval.start()

    def updateHoodDNAStore(self):
        hood = base.cr.playGame.hood
        holidayIds = base.cr.newsManager.getDecorationHolidayId()
        for holiday in holidayIds:
            for storageFile in hood.holidayStorageDNADict.get(holiday, []):
                loadDNAFile(self.dnaStore, storageFile)



    def getSwapVisibleIval(self, wait = 5.0, tFadeOut = 3.0, tFadeIn = 3.0): # NJF

        loader = base.cr.playGame.hood.loader
        npl = render.findAllMatches('**/*light*')
        npl += render.findAllMatches('**/*lamp*')
        npl += render.findAllMatches('**/*prop_tree*')
        npl += render.findAllMatches('**/*prop_snow_tree*')
        npl += render.findAllMatches('**/*prop_palm_tree_topflat*')


        #render.ls()


        p = Parallel()
        for i in range(npl.getNumPaths()):
            np = npl.getPath(i)

            geomNodeCollection = np.findAllMatches('**/+GeomNode')
            for nodePath in geomNodeCollection:


                try:
                    newPosX = nodePath.getPos(nodePath.getParent())
                    if newPosX != (0,0,0):
                        newPos = newPosX


                    newHprX = nodePath.getHpr(nodePath.getParent())
                    if newHprX != (0,0,0):
                        newHpr = newHprX
                    else:
                        newHpr = (0,0,0)


                    newScaleX = nodePath.getScale()
                    if newScaleX != LVecBase3f(1, 1, 1):
                        newScale = newScaleX
                    else:
                        newScale = LVecBase3f(1, 1, 1)

                except:
                    newPos = (0,0,0)
                    newHpr = (0,0,0)
                    newScale = LVecBase3f(1, 1, 1)





            DDLHalloween = np.findAllMatches('**/+GeomNode') # NJF
            for nodePathA in DDLHalloween:
                print(nodePathA)
                try:
                    print(nodePathA.getPos())
                except:
                    print("no pos")


            np.setTransparency(TransparencyAttrib.MDual, 1)
            if not np.hasTag('DNACode'):
                continue
            dnaCode = np.getTag('DNACode')
            dnaNode = self.dnaStore.findNode(dnaCode)
            if dnaNode.isEmpty():
                continue
            newNP = dnaNode.copyTo(np.getParent())
            newNP.setTag('DNARoot', 'holiday_prop')
            newNP.setTag('DNACode', dnaCode)
            newNP.setColorScale(1, 1, 1, 0)
            newNP.setTransparency(TransparencyAttrib.MDual, 1)
            if np.hasTag('transformIndex'):
                index = int(np.getTag('transformIndex'))
                transform = loader.holidayPropTransforms.get(index, TransformState.makeIdentity())
                newNP.setTransform(NodePath(), transform)
                newNP.setTag('transformIndex', 'index')



            if newPos != (0,0,0):
                if dnaCode == 'prop_palm_tree_topflat': # Donald's dock is... a wreck.
                    newNP.setX(newPos[0])
                    newNP.setY(newPos[1])
                    correctedZ = newPos[2] / newScale[2] / 7.4 # This is such a hackjob ugh
                    newNP.setZ(correctedZ)
                else:
                    newNP.setPos(newPos)

            if newHpr != (0,0,0):
                newNP.setHpr(newHpr)
            if newScale != LVecBase3f(1, 1, 1):
                newNP.setScale(newScale)

            if dnaCode == 'streetlight_DD_left' or dnaCode == 'streetlight_DD_right': # Donald's dock is... a wreck.
                if newPos[2] > 7:
                    newNP.setZ(5.68)
                   
            if dnaCode == 'prop_tree_large_ur' or dnaCode == 'prop_tree_large_ul':
                correctedZ = newPos[2] + 0.25
                newNP.setZ(correctedZ)
 


            s = Sequence(Wait(wait), np.colorScaleInterval(tFadeOut, Vec4(1, 1, 1, 0), startColorScale=Vec4(1, 1, 1, 1), blendType='easeInOut'), Func(np.detachNode), Func(np.clearTransparency), newNP.colorScaleInterval(tFadeOut, Vec4(1, 1, 1, 1), startColorScale=Vec4(1, 1, 1, 0), blendType='easeInOut'), Func(newNP.clearTransparency), Func(newNP.clearColorScale))
            p.append(s)

        return p





