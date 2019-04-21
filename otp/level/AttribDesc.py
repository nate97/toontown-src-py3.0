

class AttribDesc:

    def __init__(self, name, default, datatype = 'string', params = {}):
        self.name = name
        self.default = default
        self.datatype = datatype
        self.params = params

    def getName(self):
        return self.name

    def getDefaultValue(self):
        return self.default

    def getDatatype(self):
        return self.datatype

    def getParams(self):
        return self.params

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'AttribDesc(%s, %s, %s, %s)' % (repr(self.name),
         repr(self.default),
         repr(self.datatype),
         repr(self.params))
