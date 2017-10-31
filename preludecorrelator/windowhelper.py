from context import search as ctx_search
from context import getName as getCtxName

class WindowHelper(object):

    def __init__(self, name, ctx):
        self._ctx = ctx
        self._name = getCtxName(name)

    def getCtx(self):
        return self._ctx

    def setCtx(self, ctx):
        self._ctx = ctx

    def getName(self):
        return self._name

    def checkCorrelationWindow(self):
        pass

    def generateCorrelationAlert(self):
        pass

    def rst(self):
        pass

    def addIdmef(self):
        pass

    def unbindContext(self):
        pass


class WindowHolder(object):

    def __init__(self):
        self._windowHelpers = []

    def getWindowHelper(self, class_name, ctx_name):
        ctx = ctx_search(ctx_name)
        if ctx is None:
            return None
        for w in self._windowHelpers:
            if w.getName() == getCtxName(ctx_name):
                if w.getCtx() is None:
                    w.setCtx(ctx)
                    w.rst()
                return w
        new_inst = class_name(ctx_name, ctx)
        self.addWindowHelper(new_inst)
        return new_inst

    def getWindowHelpers(self):
        return self._windowHelpers()

    def addWindowHelper(self, window_helper):
        self._windowHelpers.append(window_helper)
