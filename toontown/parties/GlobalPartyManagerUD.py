from direct.distributed.DistributedObjectGlobalUD import DistributedObjectGlobalUD
from direct.distributed.PyDatagram import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.task import Task
from .PartyGlobals import *
from datetime import datetime, timedelta
from panda3d.core import *

class GlobalPartyManagerUD(DistributedObjectGlobalUD):
    notify = directNotify.newCategory('GlobalPartyManagerUD')

    # This uberdog MUST be up before the AIs, as AIs talk to this UD
    
    def announceGenerate(self):
        DistributedObjectGlobalUD.announceGenerate(self)
        self.notify.debug("GPMUD generated")
        self.senders2Mgrs = {}
        self.host2PartyId = {} # just a reference mapping
        self.id2Party = {} # This should be replaced with a longterm datastore
        self.party2PubInfo = {} # This should not be longterm
        self.tempSlots = {}
        self.partyAllocator = UniqueIdAllocator(0, 100000000)
        config = getConfigShowbase()
        self.wantInstantParties = config.GetBool('want-instant-parties', 0)

        # Setup tasks
        self.runAtNextInterval()

    # GPMUD -> PartyManagerAI messaging
    def _makeAIMsg(self, field, values, recipient): # NJF
        return self.air.dclassesByName['DistributedPartyManagerUD'].getFieldByName(field).aiFormatUpdate(recipient, recipient, simbase.air.ourChannel, values)

    def sendToAI(self, field, values, sender=None):
        if not sender:
            sender = self.air.getAvatarIdFromSender()
        dg = self._makeAIMsg(field, values, self.senders2Mgrs.get(sender, sender + 8))
        self.air.send(dg)
        
    # GPMUD -> toon messaging
    def _makeAvMsg(self, field, values, recipient):
        return self.air.dclassesByName['DistributedToonUD'].getFieldByName(field).aiFormatUpdate(recipient, recipient, simbase.air.ourChannel, values)

    def sendToAv(self, avId, field, values):
        dg = self._makeAvMsg(field, values, avId)
        self.air.send(dg)
        
    # Task stuff
    def runAtNextInterval(self):
        now = datetime.now()
        howLongUntilAFive = (60 - now.second) + 60 * (4 - (now.minute % 5))
        taskMgr.doMethodLater(howLongUntilAFive, self.__checkPartyStarts, 'GlobalPartyManager_checkStarts')

    def canPartyStart(self, party):
        now = datetime.now()
        delta = timedelta(minutes=15)
        endStartable = party['start'] + delta
        if self.wantInstantParties:
            return True
        else:
            return party['start'] < now# and endStartable > now

    def isTooLate(self, party):
        now = datetime.now()
        delta = timedelta(minutes=15)
        endStartable = party['start'] + delta
        return endStartable > now

    def __checkPartyStarts(self, task):
        now = datetime.now()
        for partyId in self.id2Party:
            party = self.id2Party[partyId]
            hostId = party['hostId']
            if self.canPartyStart(party) and party['status'] == PartyStatus.Pending:
                # Time to start party
                party['status'] = PartyStatus.CanStart
                self.sendToAv(hostId, 'setHostedParties', [[self._formatParty(party)]])
                self.sendToAv(hostId, 'setPartyCanStart', [partyId])
            elif self.isTooLate(party):
                party['status'] = PartyStatus.NeverStarted
                self.sendToAv(hostId, 'setHostedParties', [[self._formatParty(party)]])
        self.runAtNextInterval()

    # Format a party dict into a party struct suitable for the wire
    def _formatParty(self, partyDict):
        start = partyDict['start']
        end = partyDict['end']
        return [partyDict['partyId'],
                partyDict['hostId'],
                start.year,
                start.month,
                start.day,
                start.hour,
                start.minute,
                end.year,
                end.month,
                end.day,
                end.hour,
                end.minute,
                partyDict['isPrivate'],
                partyDict['inviteTheme'],
                partyDict['activities'],
                partyDict['decorations'],
                partyDict.get('status', PartyStatus.Pending)]

    # Avatar joined the game, invoked by the CSMUD
    def avatarJoined(self, avId):
#        self.host2PartyId[avId] = (1337 << 32) + 10000
        partyId = self.host2PartyId.get(avId, None)
        if partyId:
            party = self.id2Party.get(partyId, None)
            if not party:
                return # There's a partyId without an actual party?? What is this madness.
            self.sendToAv(avId, 'setHostedParties', [[self._formatParty(party)]])
            if partyId not in self.party2PubInfo and self.canPartyStart(party):
                # The party hasn't started and it can start
                self.sendToAv(avId, 'setPartyCanStart', [partyId])

    # uberdog coordination of public party info
    def __updatePartyInfo(self, partyId):
        # Update all the AIs about this public party
        party = self.party2PubInfo[partyId]
        for sender in list(self.senders2Mgrs.keys()):
            actIds = []
            for activity in self.id2Party[partyId]['activities']:
                actIds.append(activity[0]) # First part of activity tuple should be actId
            minLeft = int((PARTY_DURATION - (datetime.now() - party['started']).seconds) / 60)
            self.sendToAI('updateToPublicPartyInfoUdToAllAi', [party['shardId'], party['zoneId'], partyId, self.id2Party[partyId]['hostId'], party['numGuests'], party['maxGuests'], party['hostName'], actIds, minLeft], sender=sender)

    def __updatePartyCount(self, partyId):
        # Update the party guest count
        for sender in list(self.senders2Mgrs.keys()):
            self.sendToAI('updateToPublicPartyCountUdToAllAi', [self.party2PubInfo[partyId]['numGuests'], partyId], sender=sender)

    def partyHasStarted(self, partyId, shardId, zoneId, hostName):
        self.party2PubInfo[partyId] = {'partyId': partyId, 'shardId': shardId, 'zoneId': zoneId, 'hostName': hostName, 'numGuests': 0, 'maxGuests': MaxToonsAtAParty, 'started': datetime.now()}
        self.__updatePartyInfo(partyId)
        # update the host's book
        if partyId not in self.id2Party:
            self.notify.warning("didn't find details for starting party id %s hosted by %s" % (partyId, hostName))
            return
        self.id2Party[partyId]['status'] = PartyStatus.Started
        party = self.id2Party.get(partyId, None)
        self.sendToAv(party['hostId'], 'setHostedParties', [[self._formatParty(party)]])

    def partyDone(self, partyId):
        del self.party2PubInfo[partyId]
        self.id2Party[partyId]['status'] = PartyStatus.Finished
        party = self.id2Party.get(partyId, None)
        self.sendToAv(party['hostId'], 'setHostedParties', [[self._formatParty(party)]])
        del self.id2Party[partyId]
        self.air.writeServerEvent('party-done', '%s')

    def toonJoinedParty(self, partyId, avId):
        if avId in self.tempSlots:
            del self.tempSlots[avId]
            return
        self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] += 1
        self.__updatePartyCount(partyId)

    def toonLeftParty(self, partyId, avId):
        self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] -= 1
        self.__updatePartyCount(partyId)

    def partyManagerAIHello(self, channel):
        # Upon AI boot, DistributedPartyManagerAIs are supposed to say hello. 
        # They send along the DPMAI's doId as well, so that I can talk to them later.
        print('AI with base channel %s, will send replies to DPM %s' % (simbase.air.getAvatarIdFromSender(), channel))
        self.senders2Mgrs[simbase.air.getAvatarIdFromSender()] = channel
        self.sendToAI('partyManagerUdStartingUp', [])
        
        # In addition, set up a postRemove where we inform this AI that the UD has died
        self.air.addPostRemove(self._makeAIMsg('partyManagerUdLost', [], channel))
        
    def addParty(self, avId, partyId, start, end, isPrivate, inviteTheme, activities, decorations, inviteeIds):
        try:
            partyId = str(partyId)
            partyId = partyId.split("L")[0]
            partyId = int(partyId)
        except:
            print("Could not remove L from partId") # NJF

        PARTY_TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        print('start time: %s' % start)
        startTime = datetime.strptime(start, PARTY_TIME_FORMAT)
        endTime = datetime.strptime(end, PARTY_TIME_FORMAT)
        print('start year: %s' % startTime.year)
        if avId in self.host2PartyId:
            if self.id2Party != {}:
                # Sorry, one party at a time
                print(self.id2Party)
                self.sendToAI('addPartyResponseUdToAi', [partyId, AddPartyErrorCode.TooManyHostedParties, self._formatParty(self.id2Party[partyId])])
        self.id2Party[partyId] = {'partyId': partyId, 'hostId': avId, 'start': startTime, 'end': endTime, 'isPrivate': isPrivate, 'inviteTheme': inviteTheme, 'activities': activities, 'decorations': decorations, 'inviteeIds': inviteeIds, 'status': PartyStatus.Pending}
        self.host2PartyId[avId] = partyId
        self.sendToAI('addPartyResponseUdToAi', [partyId, AddPartyErrorCode.AllOk, self._formatParty(self.id2Party[partyId])])
        if self.wantInstantParties:
            taskMgr.remove('GlobalPartyManager_checkStarts')
            taskMgr.doMethodLater(15, self.__checkPartyStarts, 'GlobalPartyManager_checkStarts')
        return
        
    def queryParty(self, hostId):
        # An AI is wondering if the host has a party. We'll tell em!
        if hostId in self.host2PartyId:
            # Yep, he has a party.
            party = self.id2Party[self.host2PartyId[hostId]]
            self.sendToAI('partyInfoOfHostResponseUdToAi', [self._formatParty(party), party.get('inviteeIds', [])])
            return
        print('query failed, av %s isnt hosting anything' % hostId)

    def requestPartySlot(self, partyId, avId, gateId):
        if partyId not in self.party2PubInfo:
            recipient = self.GetPuppetConnectionChannel(avId)
            sender = simbase.air.getAvatarIdFromSender()
            dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('partyRequestDenied').aiFormatUpdate(gateId, recipient, sender, [PartyGateDenialReasons.Unavailable])
            self.air.send(dg)
            return
        party = self.party2PubInfo[partyId]
        if party['numGuests'] >= party['maxGuests']:
            recipient = self.GetPuppetConnectionChannel(avId)
            sender = simbase.air.getAvatarIdFromSender()
            dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('partyRequestDenied').aiFormatUpdate(gateId, recipient, sender, [PartyGateDenialReasons.Full])
            self.air.send(dg)
            return
        # get them a slot
        party['numGuests'] += 1
        self.__updatePartyCount(partyId)
        # note that they might not show up
        self.tempSlots[avId] = partyId
        
        #give the client a minute to connect before freeing their slot
        taskMgr.doMethodLater(60, self._removeTempSlot, 'partyManagerTempSlot%d' % avId, extraArgs=[avId])
        
        # now format the pubPartyInfo
        actIds = []
        for activity in self.id2Party[partyId]['activities']:
            actIds.append(activity[0])
        info = [party['shardId'], party['zoneId'], party['numGuests'], party['hostName'], actIds, 0] # the param is minleft
        # find the hostId
        hostId = self.id2Party[party['partyId']]['hostId']
        # send update to client's gate
        recipient = self.GetPuppetConnectionChannel(avId)
        sender = simbase.air.getAvatarIdFromSender() # try to pretend the AI sent it. ily2 cfsworks
        dg = self.air.dclassesByName['DistributedPartyGateAI'].getFieldByName('setParty').aiFormatUpdate(gateId, recipient, sender, [info, hostId])
        self.air.send(dg)
        
    def _removeTempSlot(self, avId):
        partyId = self.tempSlots.get(avId)
        if partyId:
            del self.tempSlots[avId]
            self.party2PubInfo.get(partyId, {'numGuests': 0})['numGuests'] -= 1
            self.__updatePartyCount(partyId)

    def allocIds(self, numIds):
        ids = []
        while len(ids) < numIds:
            ids.append(self.partyAllocator.allocate())
        self.sendToAI('receiveId', ids)



