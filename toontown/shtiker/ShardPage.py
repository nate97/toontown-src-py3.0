from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.task.Task import Task
from panda3d.core import *
from toontown.distributed import ToontownDistrictStats
from toontown.hood import ZoneUtil
from toontown.shtiker import ShtikerPage
from toontown.toonbase import TTLocalizer
from toontown.toonbase import ToontownGlobals
from toontown.toontowngui import TTDialog

POP_COLORS = (Vec4(0.4, 0.4, 1.0, 1.0), Vec4(0.4, 1.0, 0.4, 1.0),
              Vec4(1.0, 0.4, 0.4, 1.0))

def compareShardTuples(a, b):
    if a[1] < b[1]:
        return -1
    elif b[1] < a[1]:
        return 1
    else:
        return 0

class ShardPage(ShtikerPage.ShtikerPage):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShardPage')

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)

        self.shardButtonMap = {}
        self.shardButtons = []
        self.scrollList = None
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.ShardInfoUpdateInterval = 5.0
        self.lowPop = config.GetInt('shard-low-pop', 150)
        self.midPop = config.GetInt('shard-mid-pop', 300)
        self.highPop = -1
        self.showPop = config.GetBool('show-population', 0)
        self.showTotalPop = config.GetBool('show-total-population', 0)
        self.noTeleport = config.GetBool('shard-page-disable', 0)

    def load(self):
        main_text_scale = 0.06
        title_text_scale = 0.12
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPageTitle, text_scale=title_text_scale, textMayChange=0, pos=(0, 0, 0.6))
        helpText_ycoord = 0.403
        self.helpText = DirectLabel(parent=self, relief=None, text='', text_scale=main_text_scale, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, helpText_ycoord))
        shardPop_ycoord = helpText_ycoord - 0.523
        totalPop_ycoord = shardPop_ycoord - 0.26
        self.totalPopulationText = DirectLabel(parent=self, relief=None, text=TTLocalizer.ShardPagePopulationTotal % 1, text_scale=main_text_scale, text_wordwrap=8, textMayChange=1, text_align=TextNode.ACenter, pos=(0.38, 0, totalPop_ycoord))
        if self.showTotalPop:
            self.totalPopulationText.show()
        else:
            self.totalPopulationText.hide()
        self.gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.listXorigin = -0.02
        self.listFrameSizeX = 0.67
        self.listZorigin = -0.96
        self.listFrameSizeZ = 1.04
        self.arrowButtonScale = 1.3
        self.itemFrameXorigin = -0.237
        self.itemFrameZorigin = 0.365
        self.buttonXstart = self.itemFrameXorigin + 0.293
        self.regenerateScrollList()
        scrollTitle = DirectFrame(parent=self.scrollList, text=TTLocalizer.ShardPageScrollTitle, text_scale=main_text_scale, text_align=TextNode.ACenter, relief=None, pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.127))

    def unload(self):
        self.gui.removeNode()
        del self.title
        self.scrollList.destroy()
        del self.scrollList
        del self.shardButtons
        taskMgr.remove('ShardPageUpdateTask-doLater')

        ShtikerPage.ShtikerPage.unload(self)

    def regenerateScrollList(self):
        selectedIndex = 0

        if self.scrollList:
            selectedIndex = self.scrollList.getSelectedIndex()
            for button in self.shardButtons:
                button.detachNode()
            self.scrollList.destroy()
            self.scrollList = None

        self.scrollList = DirectScrolledList(parent=self, relief=None, pos=(-0.5, 0, 0), incButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(self.arrowButtonScale, self.arrowButtonScale, -self.arrowButtonScale), incButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin - 0.999), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(self.gui.find('**/FndsLst_ScrollUp'),
         self.gui.find('**/FndsLst_ScrollDN'),
         self.gui.find('**/FndsLst_ScrollUp_Rllvr'),
         self.gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(self.arrowButtonScale, self.arrowButtonScale, self.arrowButtonScale), decButton_pos=(self.buttonXstart, 0, self.itemFrameZorigin + 0.227), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(self.itemFrameXorigin, 0, self.itemFrameZorigin), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(self.listXorigin,
         self.listXorigin + self.listFrameSizeX,
         self.listZorigin,
         self.listZorigin + self.listFrameSizeZ), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=15, forceHeight=0.065, items=self.shardButtons)
        self.scrollList.scrollTo(selectedIndex)

    def askForShardInfoUpdate(self, task = None):
        ToontownDistrictStats.refresh('shardInfoUpdated')
        taskMgr.doMethodLater(self.ShardInfoUpdateInterval, self.askForShardInfoUpdate, 'ShardPageUpdateTask-doLater')
        return Task.done

    def makeShardButton(self, shardId, shardName, shardPop):
        shardButtonParent = DirectFrame()
        shardButtonL = DirectButton(parent=shardButtonParent, relief=None, text=shardName, text_scale=0.06, text_align=TextNode.ALeft, text1_bg=self.textDownColor, text2_bg=self.textRolloverColor, text3_fg=self.textDisabledColor, textMayChange=0, command=self.getPopChoiceHandler(shardPop), extraArgs=[shardId])

        if self.showPop:
            popText = str(shardPop)

            if shardPop == None:
                popText = ''

            shardButtonR = DirectButton(parent=shardButtonParent, relief=None,
                                        text=popText, text_scale=0.06,
                                        text_align=TextNode.ALeft,
                                        text1_bg=self.textDownColor,
                                        text2_bg=self.textRolloverColor,
                                        text3_fg=self.textDisabledColor,
                                        textMayChange=1, pos=(0.5, 0, 0),
                                        command=self.choseShard,
                                        extraArgs=[shardId])

        else:
            model = loader.loadModel('phase_3.5/models/gui/matching_game_gui')
            button = model.find('**/minnieCircle')
            shardButtonR = DirectButton(parent=shardButtonParent, relief=None,
                                        image=button, image_scale=(0.3, 1, 0.3),
                                        image2_scale=(0.35, 1, 0.35),
                                        image_color=self.getPopColor(shardPop),
                                        pos=(0.6, 0, 0.0125),
                                        text=self.getPopText(shardPop),
                                        text_scale=0.06,
                                        text_align=TextNode.ACenter,
                                        text_pos=(-0.0125, -0.0125),
                                        text_fg=Vec4(0, 0, 0, 0),
                                        text1_fg=Vec4(0, 0, 0, 0),
                                        text2_fg=Vec4(0, 0, 0, 1),
                                        text3_fg=Vec4(0, 0, 0, 0),
                                        command=self.getPopChoiceHandler(shardPop),
                                        extraArgs=[shardId])
            model.removeNode()
            button.removeNode()

        return (shardButtonParent, shardButtonR, shardButtonL)

    def getPopColor(self, pop):
        if pop <= self.lowPop:
            newColor = POP_COLORS[0]
        elif pop <= self.midPop:
            newColor = POP_COLORS[1]
        else:
            newColor = POP_COLORS[2]
        return newColor

    def getPopText(self, pop):
        if pop <= self.lowPop:
            popText = TTLocalizer.ShardPageLow
        elif pop <= self.midPop:
            popText = TTLocalizer.ShardPageMed
        else:
            popText = TTLocalizer.ShardPageHigh
        return popText

    def getPopChoiceHandler(self, pop):
        if pop <= self.midPop:
            if self.noTeleport and not self.showPop:
                handler = self.shardChoiceReject
            else:
                handler = self.choseShard
        elif self.showPop:
            handler = self.choseShard
        else:
            if localAvatar.adminAccess >= 200:
                handler = self.choseShard
            else:
                handler = self.shardChoiceReject
        return handler

    def getCurrentZoneId(self):
        try:
            zoneId = base.cr.playGame.getPlace().getZoneId()
        except:
            zoneId = None
        return zoneId

    def getCurrentShardId(self):
        zoneId = self.getCurrentZoneId()

        if zoneId != None and ZoneUtil.isWelcomeValley(zoneId):
            return ToontownGlobals.WelcomeValleyToken
        else:
            return base.localAvatar.defaultShard

    def updateScrollList(self):
        curShardTuples = base.cr.listActiveShards()
        curShardTuples.sort(compareShardTuples)

        currentShardId = self.getCurrentShardId()
        actualShardId = base.localAvatar.defaultShard
        actualShardName = None
        anyChanges = 0
        totalPop = 0
        totalWVPop = 0
        currentMap = {}
        self.shardButtons = []

        for i in xrange(len(curShardTuples)):

            shardId, name, pop, WVPop = curShardTuples[i]

            if shardId == actualShardId:
                actualShardName = name

            totalPop += pop
            totalWVPop += WVPop
            currentMap[shardId] = 1
            buttonTuple = self.shardButtonMap.get(shardId)

            if buttonTuple == None:
                buttonTuple = self.makeShardButton(shardId, name, pop)
                self.shardButtonMap[shardId] = buttonTuple
                anyChanges = 1
            elif self.showPop:
                buttonTuple[1]['text'] = str(pop)
            else:
                buttonTuple[1]['image_color'] = self.getPopColor(pop)
                buttonTuple[1]['text'] = self.getPopText(pop)
                buttonTuple[1]['command'] = self.getPopChoiceHandler(pop)
                buttonTuple[2]['command'] = self.getPopChoiceHandler(pop)

            self.shardButtons.append(buttonTuple[0])

            if shardId == currentShardId or self.book.safeMode:
                buttonTuple[1]['state'] = DGG.DISABLED
                buttonTuple[2]['state'] = DGG.DISABLED
            else:
                buttonTuple[1]['state'] = DGG.NORMAL
                buttonTuple[2]['state'] = DGG.NORMAL


        for shardId, buttonTuple in self.shardButtonMap.items():

            if shardId not in currentMap:
                buttonTuple[0].destroy()
                del self.shardButtonMap[shardId]
                anyChanges = 1

        if anyChanges:
            self.regenerateScrollList()

        self.totalPopulationText['text'] = TTLocalizer.ShardPagePopulationTotal % totalPop
        helpText = TTLocalizer.ShardPageHelpIntro

        if actualShardName:
            helpText += TTLocalizer.ShardPageHelpWhere % actualShardName

        if not self.book.safeMode:
            helpText += TTLocalizer.ShardPageHelpMove

    def enter(self):
        self.askForShardInfoUpdate()
        self.updateScrollList()
        currentShardId = self.getCurrentShardId()
        buttonTuple = self.shardButtonMap.get(currentShardId)
        if buttonTuple:
            i = self.shardButtons.index(buttonTuple[0])
            self.scrollList.scrollTo(i, centered=1)

        ShtikerPage.ShtikerPage.enter(self)
        self.accept('shardInfoUpdated', self.updateScrollList)

    def exit(self):
        self.ignore('shardInfoUpdated')
        self.ignore('ShardPageConfirmDone')
        taskMgr.remove('ShardPageUpdateTask-doLater')

        ShtikerPage.ShtikerPage.exit(self)

    def shardChoiceReject(self, shardId):
        self.confirm = TTDialog.TTGlobalDialog(doneEvent='ShardPageConfirmDone', message=TTLocalizer.ShardPageChoiceReject, style=TTDialog.Acknowledge)
        self.confirm.show()
        self.accept('ShardPageConfirmDone', self.__handleConfirm)

    def __handleConfirm(self):
        self.ignore('ShardPageConfirmDone')
        self.confirm.cleanup()
        del self.confirm

    def choseShard(self, shardId):
        zoneId = self.getCurrentZoneId()
        canonicalHoodId = ZoneUtil.getCanonicalHoodId(base.localAvatar.lastHood)
        currentShardId = self.getCurrentShardId()

        if shardId == currentShardId:
            return
        elif shardId == base.localAvatar.defaultShard:
            self.doneStatus = {'mode': 'teleport', 'hood': canonicalHoodId}
            messenger.send(self.doneEvent)
        else:
            try:
                place = base.cr.playGame.getPlace()
            except:
                try:
                    place = base.cr.playGame.hood.loader.place
                except:
                    place = base.cr.playGame.hood.place

            place.requestTeleport(canonicalHoodId, canonicalHoodId, shardId, -1)
