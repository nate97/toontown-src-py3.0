import random
from panda3d.core import *
from direct.directnotify.DirectNotifyGlobal import *
import random
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from otp.avatar import AvatarDNA
notify = directNotify.newCategory('CharDNA')
charTypes = ['mk',
 'vmk',
 'mn',
 'wmn',
 'g',
 'sg',
 'd',
 'fd',
 'dw',
 'p',
 'wp',
 'cl',
 'dd',
 'shdd',
 'ch',
 'da',
 'pch',
 'jda']

class CharDNA(AvatarDNA.AvatarDNA):

    def __init__(self, str = None, type = None, dna = None, r = None, b = None, g = None):
        if str != None:
            self.makeFromNetString(str)
        elif type != None:
            if type == 'c':
                self.newChar(dna)
        else:
            self.type = 'u'
        return

    def __str__(self):
        if self.type == 'c':
            return 'type = char, name = %s' % self.name_
        else:
            return 'type undefined'

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 'c':
            dg.addFixedString(self.name_, 2)
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type: ', self.type)
        return dg.getMessage()

    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)
        if self.type == 'c':
            self.name_ = sgi.getFixedString(2)
        else:
            notify.error('unknown avatar type: ', self.type)
        return None

    def __defaultChar(self):
        self.type = 'c'
        self.name_ = charTypes[0]

    def newChar(self, name = None):
        if name == None:
            self.__defaultChar()
        else:
            self.type = 'c'
            if name in charTypes:
                self.name_ = name
            else:
                notify.error('unknown avatar type: %s' % name)
        return

    def getType(self):
        if self.type == 'c':
            type = self.getCharName()
        else:
            notify.error('Invalid DNA type: ', self.type)
        return type

    def getCharName(self):
        if self.name_ == 'mk':
            return 'mickey'
        elif self.name_ == 'vmk':
            return 'vampire_mickey'
        elif self.name_ == 'mn':
            return 'minnie'
        elif self.name_ == 'wmn':
            return 'witch_minnie'
        elif self.name_ == 'g':
            return 'goofy'
        elif self.name_ == 'sg':
            return 'super_goofy'
        elif self.name_ == 'd':
            return 'donald'
        elif self.name_ == 'dw':
            return 'donald-wheel'
        elif self.name_ == 'fd':
            return 'franken_donald'
        elif self.name_ == 'dd':
            return 'daisy'
        elif self.name_ == 'shdd':
            return 'sockHop_daisy'
        elif self.name_ == 'p':
            return 'pluto'
        elif self.name_ == 'wp':
            return 'western_pluto'
        elif self.name_ == 'cl':
            return 'clarabelle'
        elif self.name_ == 'ch':
            return 'chip'
        elif self.name_ == 'da':
            return 'dale'
        elif self.name_ == 'pch':
            return 'police_chip'
        elif self.name_ == 'jda':
            return 'jailbird_dale'
        else:
            notify.error('unknown char type: ', self.name_)
