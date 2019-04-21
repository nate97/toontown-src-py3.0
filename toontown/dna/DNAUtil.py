from panda3d.core import LVector4f
#import copy

def dgiExtractString8(dgi):

    #dgi2 = copy.copy(dgi)
    #print dgi2.extractBytes(dgi2.getUint8())

    return dgi.extractBytes(dgi.getUint8())

def dgiExtractColor(dgi):
    a, b, c, d = (dgi.getUint8() / 255.0 for _ in xrange(4))
    return LVector4f(a, b, c, d)

