from panda3d.core import LVector4f

def dgiExtractString8(dgi):

    code = dgi.extractBytes(dgi.getUint8())

    if isinstance(code, bytes):
        codeBackup = code
        try:
            code = code.decode('utf-8')
        except:
            code = codeBackup

    return code

def dgiExtractColor(dgi):
    a, b, c, d = (dgi.getUint8() / 255.0 for _ in range(4))
    return LVector4f(a, b, c, d)



