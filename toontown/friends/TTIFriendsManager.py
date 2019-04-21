from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.otpbase import OTPLocalizer
from toontown.hood import ZoneUtil

class TTIFriendsManager(DistributedObjectGlobal):
    def d_removeFriend(self, friendId):
        self.sendUpdate('removeFriend', [friendId])

    def d_requestAvatarInfo(self, friendIds):
        self.sendUpdate('requestAvatarInfo', [friendIds])

    def d_requestFriendsList(self):
        self.sendUpdate('requestFriendsList', [])

    def friendInfo(self, resp):
        base.cr.handleGetFriendsListExtended(resp)

    def friendList(self, resp):
        base.cr.handleGetFriendsList(resp)

    def friendOnline(self, id, commonChatFlags, whitelistChatFlags):
        base.cr.handleFriendOnline(id, commonChatFlags, whitelistChatFlags)

    def friendOffline(self, id):
        base.cr.handleFriendOffline(id)

    def d_getAvatarDetails(self, avId):
        self.sendUpdate('getAvatarDetails', [avId])

    def friendDetails(self, avId, inventory, trackAccess, trophies, hp, maxHp, defaultShard, lastHood, dnaString, experience, trackBonusLevel):
        fields = [
            ['setExperience' , experience],
            ['setTrackAccess' , trackAccess],
            ['setTrackBonusLevel' , trackBonusLevel],
            ['setInventory' , inventory],
            ['setHp' , hp],
            ['setMaxHp' , maxHp],
            ['setDefaultShard' , defaultShard],
            ['setLastHood' , lastHood],
            ['setDNAString' , dnaString],
        ]
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)

    def d_getPetDetails(self, avId):
        self.sendUpdate('getPetDetails', [avId])




    def petDetails(self, avId, ownerId, petName, traitSeed, sz, traits, moods, dna, lastSeen):
        fields = list(zip(("setHead", "setEars", "setNose", "setTail", "setBodyTexture", "setColor", "setColorScale", "setEyeColor", "setGender"), dna))
        fields.extend(zip(("setBoredom", "setRestlessness", "setPlayfulness", "setLoneliness",
                           "setSadness", "setAffection", "setHunger", "setConfusion", "setExcitement",
                           "setFatigue", "setAnger", "setSurprise"), moods))
        fields.extend(zip(("setForgetfulness", "setBoredomThreshold", "setRestlessnessThreshold",
                           "setPlayfulnessThreshold", "setLonelinessThreshold", "setSadnessThreshold",
                           "setFatigueThreshold", "setHungerThreshold", "setConfusionThreshold",
                           "setExcitementThreshold", "setAngerThreshold", "setSurpriseThreshold",
                           "setAffectionThreshold"), traits))
        fields.append(("setOwnerId", ownerId))
        fields.append(("setPetName", petName))
        fields.append(("setTraitSeed", traitSeed))
        fields.append(("setSafeZone", sz))
        fields.append(("setLastSeenTimestamp", lastSeen))
        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)





    """
    def petDetails(self, avId, ownerId, petName, traitSeed, sz, traits, moods, dna, lastSeen):
    


        fields = []
        
        # DNA
        fields.append(["setHead", dna[0]])
        fields.append(["setEars", dna[1]])
        fields.append(["setNose", dna[2]])
        fields.append(["setTail", dna[3]])
        fields.append(["setBodyTexture", dna[4]])
        fields.append(["setColor", dna[5]])
        fields.append(["setColorScale", dna[6]])
        fields.append(["setEyeColor", dna[7]])
        fields.append(["setGender", dna[8]])

        # MOODS
        fields.append(["setBoredom", moods[0]])
        fields.append(["setRestlessness", moods[1]])
        fields.append(["setPlayfulness", moods[2]])
        fields.append(["setLoneliness", moods[3]])
        fields.append(["setSadness", moods[4]])
        fields.append(["setAffection", moods[5]])
        fields.append(["setHunger", moods[6]])
        fields.append(["setConfusion", moods[7]])
        fields.append(["setExcitement", moods[8]])
        fields.append(["setFatigue", moods[9]])
        fields.append(["setAnger", moods[10]])
        fields.append(["setSurprise", moods[11]])

        # TRAITS
        fields.append(["setForgetfulness", traits[0]])
        fields.append(["setBoredomThreshold", traits[1]])
        fields.append(["setRestlessnessThreshold", traits[2]])
        fields.append(["setPlayfulnessThreshold", traits[3]])
        fields.append(["setLonelinessThreshold", traits[4]])
        fields.append(["setSadnessThreshold", traits[5]])
        fields.append(["setFatigueThreshold", traits[6]])
        fields.append(["setHungerThreshold", traits[7]])
        fields.append(["setConfusionThreshold", traits[8]])
        fields.append(["setExcitementThreshold", traits[9]])
        fields.append(["setAngerThreshold", traits[10]])
        fields.append(["setSurpriseThreshold", traits[11]])
        fields.append(["setAffectionThreshold", traits[12]])

        # OTHER
        fields.append(["setOwnerId", ownerId])
        fields.append(["setPetName", petName])
        fields.append(["setTraitSeed", traitSeed])
        fields.append(["setSafeZone", sz])
        fields.append(["setLastSeenTimestamp", lastSeen])

        base.cr.n_handleGetAvatarDetailsResp(avId, fields=fields)"""





    def d_teleportQuery(self, toId):
        self.sendUpdate('routeTeleportQuery', [toId])

    def teleportQuery(self, fromId):
        if not hasattr(base, 'localAvatar'):
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not hasattr(base.localAvatar, 'getTeleportAvailable') or not hasattr(base.localAvatar, 'ghostMode'):
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return
        if not base.localAvatar.getTeleportAvailable() or base.localAvatar.ghostMode:
            if hasattr(base.cr.identifyFriend(fromId), 'getName'):
                base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperFailedVisit % base.cr.identifyFriend(fromId).getName())
            self.sendUpdate('teleportResponse', [ fromId, 0, 0, 0, 0 ])
            return

        hoodId = base.cr.playGame.getPlaceId()
        if hasattr(base.cr.identifyFriend(fromId), 'getName'):
            base.localAvatar.setSystemMessage(fromId, OTPLocalizer.WhisperComingToVisit % base.cr.identifyFriend(fromId).getName())
        self.sendUpdate('teleportResponse', [
            fromId,
            base.localAvatar.getTeleportAvailable(),
            base.localAvatar.defaultShard,
            hoodId,
            base.localAvatar.getZoneId()
        ])

    def d_teleportResponse(self, toId, available, shardId, hoodId, zoneId):
        self.sendUpdate('teleportResponse', [toId, available, shardId,
            hoodId, zoneId]
        )

    def setTeleportResponse(self, fromId, available, shardId, hoodId, zoneId):
        base.localAvatar.teleportResponse(fromId, available, shardId, hoodId, zoneId)

    def d_whisperSCTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCTo', [toId, msgIndex])

    def setWhisperSCFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCFrom'):
            return
        base.localAvatar.setWhisperSCFrom(fromId, msgIndex)

    def d_whisperSCCustomTo(self, toId, msgIndex):
        self.sendUpdate('whisperSCCustomTo', [toId, msgIndex])

    def setWhisperSCCustomFrom(self, fromId, msgIndex):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCCustomFrom'):
            return
        base.localAvatar.setWhisperSCCustomFrom(fromId, msgIndex)

    def d_whisperSCEmoteTo(self, toId, emoteId):
        self.sendUpdate('whisperSCEmoteTo', [toId, emoteId])

    def setWhisperSCEmoteFrom(self, fromId, emoteId):
        if not hasattr(base, 'localAvatar'):
            return
        if not hasattr(base.localAvatar, 'setWhisperSCEmoteFrom'):
            return
        base.localAvatar.setWhisperSCEmoteFrom(fromId, emoteId)

    def receiveTalkWhisper(self, fromId, message):
        toon = base.cr.identifyAvatar(fromId)
        if toon:
            base.localAvatar.setTalkWhisper(fromId, 0, toon.getName(), message, [], 0)

    def d_requestSecret(self):
        self.sendUpdate('requestSecret', [])

    def requestSecretResponse(self, result, secret):
        messenger.send('requestSecretResponse', [result, secret])

    def d_submitSecret(self, secret):
        self.sendUpdate('submitSecret', [secret])

    def submitSecretResponse(self, result, avId):
        messenger.send('submitSecretResponse', [result, avId])

    def d_battleSOS(self, toId):
        self.sendUpdate('battleSOS', [toId])

    def setBattleSOS(self, fromId):
        base.localAvatar.battleSOS(fromId)

    def d_teleportGiveup(self, toId):
        self.sendUpdate('teleportGiveup', [toId])

    def setTeleportGiveup(self, fromId):
        base.localAvatar.teleportGiveup(fromId)

    def d_whisperSCToontaskTo(self, toId, taskId, toNpcId, toonProgress, msgIndex):
        self.sendUpdate('whisperSCToontaskTo', [toId, taskId, toNpcId,
            toonProgress, msgIndex]
        )

    def setWhisperSCToontaskFrom(self, fromId, taskId, toNpcId, toonProgress, msgIndex):
        base.localAvatar.setWhisperSCToontaskFrom(fromId, taskId, toNpcId,
            toonProgress, msgIndex
        )

    def d_sleepAutoReply(self, toId):
        self.sendUpdate('sleepAutoReply', [toId])

    def setSleepAutoReply(self, fromId):
        base.localAvatar.setSleepAutoReply(fromId)
