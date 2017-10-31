from context import search as ctx_search

class WindowHelper(object):

    def __init__(self, ctx):
        self._ctx = ctx
        self._name = ctx.getName()

    def getCtx():
        return self._ctx

    def setCtx(self, ctx):
        self._ctx = ctx

    def getName():
        return self._name

    def checkCorrelationWindow(self):
        pass

    def rst():
        pass

    def addIdmef():
        pass

    def unbindContext():
        pass


class WindowHolder(object):

    def __init__(self):
        self._windowHelpers = []

    def getWindowHelper(self, class_name, ctx_name):
        ctx = ctx_search(ctx_name)
        if ctx is None:
            return None
        for w in self._windowHelpers:
            if w.getName() == ctx.getName():
                if w.getContext() is None:
                    w.setContext(ctx)
                    w.rst()
                return w
        return class_name(name, ctx)

    def getWindowHelpers(self):
        return self._windowHelpers()

    def addWindowHelper(self, window_helper):
        self._windowHelpers.append(window_helper)
