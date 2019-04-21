from panda3d.core import TextNode, PGButton, Point3

from toontown.chat import ChatGlobals
from toontown.chat.ChatBalloon import ChatBalloon
from toontown.margins import MarginGlobals
from toontown.margins.MarginVisible import MarginVisible
from toontown.nametag import NametagGlobals
from toontown.toontowngui.Clickable2d import Clickable2d


class WhisperPopup(Clickable2d, MarginVisible):
    CONTENTS_SCALE = 0.25

    TEXT_MAX_ROWS = 6
    TEXT_WORD_WRAP = 8

    WHISPER_TIMEOUT_MIN = 10
    WHISPER_TIMEOUT_MAX = 20

    def __init__(self, text, font, whisperType, timeout=None):
        Clickable2d.__init__(self, 'WhisperPopup')
        MarginVisible.__init__(self)

        self.text = text
        self.font = font
        self.whisperType = whisperType
        if timeout is None:
            self.timeout = len(text) * 0.33
            if self.timeout < self.WHISPER_TIMEOUT_MIN:
                self.timeout = self.WHISPER_TIMEOUT_MIN
            elif self.timeout > self.WHISPER_TIMEOUT_MAX:
                self.timeout = self.WHISPER_TIMEOUT_MAX
        else:
            self.timeout = timeout

        self.active = False

        self.senderName = ''
        self.fromId = 0
        self.isPlayer = 0

        self.contents.setScale(self.CONTENTS_SCALE)

        self.whisperColor = ChatGlobals.WhisperColors[self.whisperType]

        self.textNode = TextNode('text')
        self.textNode.setWordwrap(self.TEXT_WORD_WRAP)
        self.textNode.setTextColor(self.whisperColor[PGButton.SInactive][0])
        self.textNode.setFont(self.font)
        self.textNode.setText(self.text)

        self.chatBalloon = None

        self.timeoutTaskName = self.getUniqueName() + '-timeout'
        self.timeoutTask = None

        self.setPriority(MarginGlobals.MP_high)
        self.setVisible(True)

        self.update()

        self.accept('MarginVisible-update', self.update)

    def destroy(self):
        self.ignoreAll()

        if self.timeoutTask is not None:
            taskMgr.remove(self.timeoutTask)
            self.timeoutTask = None

        if self.chatBalloon is not None:
            self.chatBalloon.removeNode()
            self.chatBalloon = None

        self.textNode = None

        Clickable2d.destroy(self)

    def getUniqueName(self):
        return 'WhisperPopup-' + str(id(self))

    def update(self):
        if self.chatBalloon is not None:
            self.chatBalloon.removeNode()
            self.chatBalloon = None

        self.contents.node().removeAllChildren()

        self.draw()

        if self.cell is not None:
            # We're in the margin display. Reposition our content, and update
            # the click region:
            self.reposition()
            self.updateClickRegion()
        else:
            # We aren't in the margin display. Disable the click region if one
            # is present:
            if self.region is not None:
                self.region.setActive(False)

    def draw(self):
        if self.isClickable():
            foreground, background = self.whisperColor[self.clickState]
        else:
            foreground, background = self.whisperColor[PGButton.SInactive]
        self.chatBalloon = ChatBalloon(
            NametagGlobals.chatBalloon2dModel,
            NametagGlobals.chatBalloon2dWidth,
            NametagGlobals.chatBalloon2dHeight, self.textNode,
            foreground=foreground, background=background
        )
        self.chatBalloon.reparentTo(self.contents)

        # Calculate the center of the TextNode:
        left, right, bottom, top = self.textNode.getFrameActual()
        center = self.contents.getRelativePoint(
            self.chatBalloon.textNodePath,
            ((left+right) / 2.0, 0, (bottom+top) / 2.0))

        # Translate the chat balloon along the inverse:
        self.chatBalloon.setPos(self.chatBalloon, -center)

    def manage(self, marginManager):
        MarginVisible.manage(self, marginManager)

        self.timeoutTask = taskMgr.doMethodLater(
            self.timeout, self.unmanage, self.timeoutTaskName, [marginManager])

    def unmanage(self, marginManager):
        MarginVisible.unmanage(self, marginManager)

        self.destroy()

    def setClickable(self, senderName, fromId, isPlayer=0):
        self.senderName = senderName
        self.fromId = fromId
        self.isPlayer = isPlayer
        self.setClickEvent('clickedWhisper', extraArgs=[fromId, isPlayer])
        self.setActive(True)

    def applyClickState(self, clickState):
        if self.chatBalloon is not None:
            foreground, background = self.whisperColor[clickState]
            self.chatBalloon.setForeground(foreground)
            self.chatBalloon.setBackground(background)

    def setClickState(self, clickState):
        if self.isClickable():
            self.applyClickState(clickState)
        else:
            self.applyClickState(PGButton.SInactive)

        Clickable2d.setClickState(self, clickState)

    def enterDepressed(self):
        if self.isClickable():
            base.playSfx(NametagGlobals.clickSound)

    def enterRollover(self):
        if self.isClickable() and (self.lastClickState != PGButton.SDepressed):
            base.playSfx(NametagGlobals.rolloverSound)

    def updateClickRegion(self):
        if self.chatBalloon is not None:
            right = self.chatBalloon.width / 2.0
            left = -right
            top = self.chatBalloon.height / 2.0
            bottom = -top

            self.setClickRegionFrame(left, right, bottom, top)
            self.region.setActive(True)
        else:
            if self.region is not None:
                self.region.setActive(False)

    def marginVisibilityChanged(self):
        if self.cell is not None:
            # We're in the margin display. Reposition our content, and update
            # the click region:
            self.reposition()
            self.updateClickRegion()
        else:
            # We aren't in the margin display. Disable the click region if one
            # is present:
            if self.region is not None:
                self.region.setActive(False)

    def reposition(self):
        if self.contents is None:
            return

        origin = Point3()

        self.contents.setPos(origin)

        if self.chatBalloon is not None:
            self.chatBalloon.removeNode()
            self.chatBalloon = None

        self.contents.node().removeAllChildren()

        if (self.cell in base.leftCells) or (self.cell in base.rightCells):
            text = self.text.replace('\x01WLDisplay\x01', '').replace('\x02', '')
            textWidth = self.textNode.calcWidth(text)
            if (textWidth / self.TEXT_WORD_WRAP) > self.TEXT_MAX_ROWS:
                self.textNode.setWordwrap(textWidth / (self.TEXT_MAX_ROWS-0.5))
        else:
            self.textNode.setWordwrap(self.TEXT_WORD_WRAP)

        self.draw()

        left, right, bottom, top = self.textNode.getFrameActual()
        left -= self.chatBalloon.BALLOON_X_PADDING
        right += self.chatBalloon.BALLOON_X_PADDING
        bottom -= self.chatBalloon.BALLOON_Z_PADDING
        top += self.chatBalloon.BALLOON_Z_PADDING

        if self.cell in base.bottomCells:
            # Move the origin to the bottom center of the chat balloon:
            origin = self.contents.getRelativePoint(
                self.chatBalloon.textNodePath, ((left+right) / 2.0, 0, bottom))
        elif self.cell in base.leftCells:
            # Move the origin to the left center of the chat balloon:
            origin = self.contents.getRelativePoint(
                self.chatBalloon.textNodePath, (left, 0, (bottom+top) / 2.0))
        elif self.cell in base.rightCells:
            # Move the origin to the right center of the chat balloon:
            origin = self.contents.getRelativePoint(
                self.chatBalloon.textNodePath, (right, 0, (bottom+top) / 2.0))

        self.contents.setPos(self.contents, -origin)
