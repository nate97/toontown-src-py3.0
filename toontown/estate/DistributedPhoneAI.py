from toontown.estate.DistributedFurnitureItemAI import DistributedFurnitureItemAI
from toontown.toonbase import ToontownGlobals
from toontown.catalog import CatalogItem
from toontown.catalog.CatalogInvalidItem import CatalogInvalidItem
from toontown.catalog.CatalogItemList import CatalogItemList
from direct.distributed.ClockDelta import *
import time
from . import PhoneGlobals


class DistributedPhoneAI(DistributedFurnitureItemAI):
    notify = directNotify.newCategory('DistributedPhoneAI')

    def __init__(self, air, furnitureMgr, item):
        DistributedFurnitureItemAI.__init__(self, air, furnitureMgr, item)

        self.avId = None

    def getInitialScale(self):
        return (0.8, 0.8, 0.8)

    def setNewScale(self, sx, sy, sz):
        if sx + sy + sz < 5:
            return
        self.sendUpdate('setInitialScale', [sx, sy, sz])

    def avatarEnter(self):
        avId = self.air.getAvatarIdFromSender()
        if self.avId:
            if self.avId == avId:
                self.air.writeServerEvent('suspicious', avId, 'Tried to use a phone twice!')
                return
            self.sendUpdateToAvatarId(avId, 'freeAvatar', [])
            return

        av = self.air.doId2do.get(avId)
        if not av:
            return

        if not av.houseId:
            self.d_setMovie(PhoneGlobals.PHONE_MOVIE_NO_HOUSE, avId, globalClockDelta.getRealNetworkTime(bits=32))
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            return

        if len(av.monthlyCatalog) == 0 and len(av.weeklyCatalog) == 0 and len(av.backCatalog) == 0:
            self.d_setMovie(PhoneGlobals.PHONE_MOVIE_EMPTY, avId, globalClockDelta.getRealNetworkTime(bits=32))
            taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])
            return

        self.air.questManager.toonUsedPhone(avId)
        self.avId = avId
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_PICKUP, avId, globalClockDelta.getRealNetworkTime(bits=32))

        house = self.air.doId2do.get(av.houseId)
        if house:
            numItems = len(house.interiorItems) + len(house.atticItems) + len(house.atticWallpaper) + len(house.atticWindows) + len (house.interiorWallpaper) + len(house.interiorWindows)
            self.sendUpdateToAvatarId(avId, 'setLimits', [numItems])
        else:
            self.air.dbInterface.queryObject(self.air.dbId, av.houseId, self.__gotHouse)

        av.b_setCatalogNotify(ToontownGlobals.NoItems, av.mailboxNotify)

    def __gotHouse(self, dclass, fields):
            if dclass != self.air.dclassesByName['DistributedHouseAI']:
                return

            numItems = len(CatalogItemList(fields['setInteriorItems'][0], store=CatalogItem.Customization)) + len(CatalogItemList(fields['setAtticItems'][0], store=CatalogItem.Customization)) + len(CatalogItemList(fields['setAtticWallpaper'][0], store=CatalogItem.Customization)) + len(CatalogItemList(fields['setAtticWindows'][0], store=CatalogItem.Customization)) + len(CatalogItemList(fields['setInteriorWallpaper'][0], store=CatalogItem.Customization)) + len(CatalogItemList(fields['setInteriorWindows'][0], store=CatalogItem.Customization))
            self.sendUpdateToAvatarId(fields['setAvatarId'][0], 'setLimits', [numItems])

    def avatarExit(self):
        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId, 'Tried to exit a phone they weren\'t using!')
            return

        self.avId = None
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_HANGUP, avId, globalClockDelta.getRealNetworkTime(bits=32))
        taskMgr.doMethodLater(1, self.__resetMovie, 'resetMovie-%d' % self.getDoId(), extraArgs=[])

    def d_setMovie(self, mode, avId, time):
        self.sendUpdate('setMovie', [mode, avId, time])

    def __resetMovie(self):
        self.d_setMovie(PhoneGlobals.PHONE_MOVIE_CLEAR, 0, globalClockDelta.getRealNetworkTime(bits=32))

    def requestPurchaseMessage(self, context, item, optional):

        print (context, item, optional)

        avId = self.air.getAvatarIdFromSender()
        if avId != self.avId:
            self.air.writeServerEvent('suspicious', avId, 'Tried to purchase while not using the phone!')
            return

        av = self.air.doId2do.get(avId)
        if not av:
            self.air.writeServerEvent('suspicious', avId, 'Used phone from other shard!')
            return

        item = CatalogItem.getItem(item)


        # None of this should be neccessary, but it works as a temporary thing. NEEDS WORK !!!
        # PY3
        weeklyCatalog = []
        monthlyCatalog = []
        backCatalog = []

        strItem = str(item)

        for wC in av.weeklyCatalog:
            weeklyCatalog.append(str(wC))

        for mC in av.monthlyCatalog:
            monthlyCatalog.append(str(mC))

        for bC in av.backCatalog:
            backCatalog.append(str(bC))


        if isinstance(item, CatalogInvalidItem):
            self.air.writeServerEvent('suspicious', avId, 'Tried to purchase invalid catalog item.')
            return
        if item.loyaltyRequirement():
            self.air.writeServerEvent('suspicious', avId, 'Tried to purchase an unimplemented loyalty item!')
            return
        if strItem in backCatalog: # PY3
            price = item.getPrice(CatalogItem.CatalogTypeBackorder)
        elif strItem in weeklyCatalog or strItem in monthlyCatalog: # PY3
            price = item.getPrice(0)
        else:
            return

        if item.getDeliveryTime():
            if len(av.onOrder) > 30: # NJF
                self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.P_OnOrderListFull])
                return

            if len(av.mailboxContents) + len(av.onOrder) >= ToontownGlobals.MaxMailboxContents:
                self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.P_MailboxFull])

            if not av.takeMoney(price):
                return

            item.deliveryDate = int(time.time() // 60) + item.getDeliveryTime()
            av.onOrder.append(item)
            av.b_setDeliverySchedule(av.onOrder)
            self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, ToontownGlobals.P_ItemOnOrder])
            taskMgr.doMethodLater(0.2, self.sendUpdateToAvatarId, 'purchaseItemComplete-%d' % self.getDoId(), extraArgs=[avId, 'purchaseItemComplete', []])
        else:
            if not av.takeMoney(price):
                return

            resp = item.recordPurchase(av, optional)
            if resp < 0:
                    av.addMoney(price)

            self.sendUpdateToAvatarId(avId, 'requestPurchaseResponse', [context, resp])
            taskMgr.doMethodLater(0.2, self.sendUpdateToAvatarId, 'purchaseItemComplete-%d' % self.getDoId(), extraArgs=[avId, 'purchaseItemComplete', []])

    def requestGiftPurchaseMessage(self, context, avId, item, optional):
        pass # TODO



