from direct.distributed.DistributedObjectUD import DistributedObjectUD


class CentralLoggerUD(DistributedObjectUD):
    def sendMessage(self, category, description, sender, receiver):
        self.air.writeServerEvent(category, sender, receiver, description)

    def logAIGarbage(self):
        pass
