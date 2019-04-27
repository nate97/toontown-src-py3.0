import json


INTERIORS_PATH = 'phase_3/bin/'
INTERIORS_FILE = 'interiors.bin'


class LegacyInteriorLoader:
    def __init__(self):
        pass


    def loadBinInteriors(self, filePath = INTERIORS_PATH + INTERIORS_FILE):
        if __debug__:
            filePath = '../resources/' + filePath
        else:
            filePath = '/' + filePath

        seedFile = open(filePath, 'rb')
        seedBin = seedFile.read()
        seedDict = self.binaryToDict(seedBin)

        seedFile.close() # Close this
        return seedDict


    def binaryToDict(self, theBinary):
        jsonStream = ''.join(chr(int(x, 2)) for x in theBinary.split())
        theDict = json.loads(jsonStream)  
        return theDict


    def dictToBinary(self, theDict):
        dictStream = json.dumps(theDict)
        theBinary = ' '.join(format(ord(letter), 'b') for letter in dictStream)
        return theBinary



