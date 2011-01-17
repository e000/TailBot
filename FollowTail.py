from twisted.internet.task import LoopingCall
from os import stat, fstat, path

class FollowTail:
    fileObj = None
    
    def __init__(self, filename, callback, *a, **kw):
        self.filename = filename
        assert path.exists(filename)
        self.lc = LoopingCall(self.check)
        self.callback = callback
        self.a, self.kw = a, kw
        
    def start(self, checkFreq = 0.5):
        self.fileObj = open(self.filename)
        self.fileObj.seek(0, 2)
        self.lc.start(checkFreq)
        
    def check(self):
        obj, callback, a, kw = self.fileObj, self.callback, self.a, self.kw
        obj.seek(obj.tell())
        for line in obj:
            callback(line, *a, **kw)
            

class ChainCallback:
    def __init__(self, *callbacks):
        self.callbacks = callbacks
        
    def __call__(self, *a, **kw):
        for callback in self.callbacks:
            callback(*a, **kw)