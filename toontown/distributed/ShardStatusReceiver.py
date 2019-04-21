class ShardStatusReceiver:
    def __init__(self, air):
        self.air = air

        self.shards = {}

        # Accept the shardStatus event:
        self.air.netMessenger.accept('shardStatus', self, self.handleShardStatus)

        # Query the status of any existing shards:
        self.air.netMessenger.send('queryShardStatus')

    def handleShardStatus(self, channel, status):
        self.shards.setdefault(channel, {}).update(status)

    def getShards(self):
        return self.shards
