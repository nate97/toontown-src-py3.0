from direct.task import Task
from toontown.hood import ZoneUtil
from toontown.toonbase import ToontownGlobals

class ToontownAccess:
    def __init__(self):
        self.startupModules = []

    def initModuleInfo(self):
        self.startupModules = self.getModuleList()
        taskMgr.doMethodLater(300, self.checkModuleInfo, 'moduleListTask')

    def delete(self):
        taskMgr.remove('moduleListTask')
        del self.startupModules

    def checkModuleInfo(self, task):
        currentModuleList = self.getModuleList()
        newModules = []
        for module in currentModuleList:
            if module not in self.startupModules:
                self.startupModules.insert(0, module)
                newModules.insert(0, module)

        self.sendUpdate('setModuleInfo', [newModules])
        return task.again

    def getModuleList(self):
        # TODO: This funciton is supposed to return a list of all modules that
        # have been linked into the process at runtime. It is only needed for
        # hack detect.
        return []

    def sendUpdate(self, fieldName, args = [], sendToId = None):
        print (fieldName)
        if base.cr and hasattr(base, 'localAvatar'):
            dg = base.localAvatar.dclass.clientFormatUpdate(fieldName, sendToId or base.localAvatar.doId, args)
            base.cr.send(dg)

    def canAccess(self, zoneId=None):
        return True
