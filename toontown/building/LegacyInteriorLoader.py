import json


INTERIORS_PATH = 'phase_3/interiors/'
INTERIORS_FILE = 'interiors.json'


class LegacyInteriorLoader:
    def __init__(self):
        pass


    def loadJSONInteriors(self, filePath = INTERIORS_PATH + INTERIORS_FILE):
        if __debug__:
            filePath = '../resources/' + filePath
        else:
            filePath = '/' + filePath

        seedFile = open(filePath, 'rb')
        seedJson = seedFile.read()
        seedDict = json.loads(seedJson)
        seedFile.close() # Close json file

        return seedDict



