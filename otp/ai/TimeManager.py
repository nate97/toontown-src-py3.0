import base64
from direct.directnotify import DirectNotifyGlobal
from direct.distributed import DistributedObject
from direct.distributed.ClockDelta import *
from direct.showbase import GarbageReport
from direct.showbase import PythonUtil
from direct.showbase.DirectObject import *
from direct.task import Task
import os
from panda3d.core import *
import re
import sys
import time
import traceback

from otp.otpbase import OTPGlobals
from toontown.chat.ChatGlobals import *


class TimeManager(DistributedObject.DistributedObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('TimeManager')
    neverDisable = 1

    def __init__(self, cr):
        DistributedObject.DistributedObject.__init__(self, cr)
        self.updateFreq = base.config.GetFloat('time-manager-freq', 1800)
        self.minWait = base.config.GetFloat('time-manager-min-wait', 10)
        self.maxUncertainty = base.config.GetFloat('time-manager-max-uncertainty', 1)
        self.maxAttempts = base.config.GetInt('time-manager-max-attempts', 5)
        self.extraSkew = base.config.GetInt('time-manager-extra-skew', 0)
        if self.extraSkew != 0:
            self.notify.info('Simulating clock skew of %0.3f s' % self.extraSkew)
        self.reportFrameRateInterval = base.config.GetDouble('report-frame-rate-interval', 300.0)
        self.talkResult = 0
        self.thisContext = -1
        self.nextContext = 0
        self.attemptCount = 0
        self.start = 0
        self.lastAttempt = -self.minWait * 2

    def generate(self):
        self._gotFirstTimeSync = False
        if self.cr.timeManager != None:
            self.cr.timeManager.delete()
        self.cr.timeManager = self
        DistributedObject.DistributedObject.generate(self)
        self.accept(OTPGlobals.SynchronizeHotkey, self.handleHotkey)
        self.accept('clock_error', self.handleClockError)
        if __dev__ and base.config.GetBool('enable-garbage-hotkey', 0):
            self.accept(OTPGlobals.DetectGarbageHotkey, self.handleDetectGarbageHotkey)
        if self.updateFreq > 0:
            self.startTask()
        return

    def announceGenerate(self):
        DistributedObject.DistributedObject.announceGenerate(self)
        self.synchronize('TimeManager.announceGenerate')

    def gotInitialTimeSync(self):
        return self._gotFirstTimeSync

    def disable(self):
        self.ignore(OTPGlobals.SynchronizeHotkey)
        if __dev__:
            self.ignore(OTPGlobals.DetectGarbageHotkey)
        self.ignore('clock_error')
        self.stopTask()
        taskMgr.remove('frameRateMonitor')
        if self.cr.timeManager == self:
            self.cr.timeManager = None
        del self._gotFirstTimeSync
        DistributedObject.DistributedObject.disable(self)
        return

    def delete(self):
        self.ignore(OTPGlobals.SynchronizeHotkey)
        self.ignore(OTPGlobals.DetectGarbageHotkey)
        self.ignore('clock_error')
        self.stopTask()
        taskMgr.remove('frameRateMonitor')
        if self.cr.timeManager == self:
            self.cr.timeManager = None
        DistributedObject.DistributedObject.delete(self)
        return

    def startTask(self):
        self.stopTask()
        taskMgr.doMethodLater(self.updateFreq, self.doUpdate, 'timeMgrTask')

    def stopTask(self):
        taskMgr.remove('timeMgrTask')

    def doUpdate(self, task):
        self.synchronize('timer')
        taskMgr.doMethodLater(self.updateFreq, self.doUpdate, 'timeMgrTask')
        return Task.done

    def handleHotkey(self):
        self.lastAttempt = -self.minWait * 2
        if self.synchronize('user hotkey'):
            self.talkResult = 1
        else:
            base.localAvatar.setChatAbsolute('Too soon.', CFSpeech | CFTimeout)

    def handleClockError(self):
        self.synchronize('clock error')

    def synchronize(self, description):
        now = globalClock.getRealTime()
        if now - self.lastAttempt < self.minWait:
            self.notify.debug('Not resyncing (too soon): %s' % description)
            return 0
        self.talkResult = 0
        self.thisContext = self.nextContext
        self.attemptCount = 0
        self.nextContext = self.nextContext + 1 & 255
        self.notify.info('Clock sync: %s' % description)
        self.start = now
        self.lastAttempt = now
        self.sendUpdate('requestServerTime', [self.thisContext])
        return 1

    def serverTime(self, context, timestamp, timeOfDay):
        end = globalClock.getRealTime()
        aiTimeSkew = timeOfDay - self.cr.getServerTimeOfDay()
        if context != self.thisContext:
            self.notify.info('Ignoring TimeManager response for old context %d' % context)
            return
        elapsed = end - self.start
        self.attemptCount += 1
        self.notify.info('Clock sync roundtrip took %0.3f ms' % (elapsed * 1000.0))
        self.notify.info('AI time delta is %s from server delta' % PythonUtil.formatElapsedSeconds(aiTimeSkew))
        average = (self.start + end) / 2.0 - self.extraSkew
        uncertainty = (end - self.start) / 2.0 + abs(self.extraSkew)
        globalClockDelta.resynchronize(average, timestamp, uncertainty)
        self.notify.info('Local clock uncertainty +/- %.3f s' % globalClockDelta.getUncertainty())
        if globalClockDelta.getUncertainty() > self.maxUncertainty:
            if self.attemptCount < self.maxAttempts:
                self.notify.info('Uncertainty is too high, trying again.')
                self.start = globalClock.getRealTime()
                self.sendUpdate('requestServerTime', [self.thisContext])
                return
            self.notify.info('Giving up on uncertainty requirement.')
        if self.talkResult:
            base.localAvatar.setChatAbsolute('latency %0.0f ms, sync \xc2\xb1%0.0f ms' % (elapsed * 1000.0, globalClockDelta.getUncertainty() * 1000.0), CFSpeech | CFTimeout)
        self._gotFirstTimeSync = True
        messenger.send('gotTimeSync')

        toontownTimeManager = getattr(base.cr, 'toontownTimeManager', None)
        if toontownTimeManager:
            toontownTimeManager.updateLoginTimes(timeOfDay, int(time.time()), globalClock.getRealTime())

    def setDisconnectReason(self, disconnectCode):
        self.notify.info('Client disconnect reason %s.' % disconnectCode)
        self.sendUpdate('setDisconnectReason', [disconnectCode])

    def setExceptionInfo(self):
        info = traceback.format_exc()
        self.notify.info('Client exception: %s' % info)
        self.sendUpdate('setExceptionInfo', [info])
        self.cr.flush()



