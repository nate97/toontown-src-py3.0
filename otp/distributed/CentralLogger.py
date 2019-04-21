from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal


REPORT_PLAYER = 'report-player'
ReportFoulLanguage = 'foul-language'
ReportPersonalInfo = 'personal-info'
ReportRudeBehavior = 'rude-behavior'
ReportBadName = 'bad-name'
ReportHacking = 'hacking'


class CentralLogger(DistributedObjectGlobal):
    PlayersReportedThisSession = {}

    def hasReportedPlayer(self, targetDISLId, targetAvId):
        return (targetDISLId, targetAvId) in self.PlayersReportedThisSession

    def reportPlayer(self, category, targetDISLId, targetAvId, description='None'):
        if self.hasReportedPlayer(targetDISLId, targetAvId):
            return False
        self.PlayersReportedThisSession[targetDISLId, targetAvId] = 1
        self.sendUpdate('sendMessage', [category, REPORT_PLAYER, targetDISLId, targetAvId])
        return True

    def writeClientEvent(self, eventString, sender=0, receiver=0):
        self.sendUpdate('sendMessage', ['client-event', eventString, sender, receiver])
