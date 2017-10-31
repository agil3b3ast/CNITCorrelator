from context import search as ctx_search
from context import getName as getCtxName
from context import Context

class WindowHelper(object):

    def __init__(self, name, ctx, initial_attrs):
        self._ctx = ctx
        self._name = getCtxName(name)
        self._options = ctx.getOptions()
        self._initialAttrs = initial_attrs

    def getOptions():
        return self._options

    def getInitialAttrs():
        return self._initialAttrs

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

    def addIdmef(self,idmef):
        pass

    def unbindContext(self):
        pass


class WindowHolder(object):

    def __init__(self):
        self._windowHelpers = []

    def bindCtxToNewWindow(self, class_name, context_id, options, initial_attrs):
        ctx = ctx_search(context_id)
        if ctx is None:
            ctx = Context(context_id, options, update = False)
            for key, value in initial_attrs.iteritems():
                ctx.set(key, value)
        return class_name(ctx, context_id, options, initial_attrs)

    def getWindowHelper(self, ctx_name):
        #ctx = ctx_search(ctx_name)
        #if ctx is None:
        #    return None
        for w in self._windowHelpers:
            if w.getName() == getCtxName(ctx_name):
                res = ctx_search(ctx_name)
                if res is None:
                    res = Context(ctx_name, w.getOptions(), update = False)
                    for key, value in w.getInitialAttrs().iteritems():
                        res.set(key, value)
                w.setCtx(res)
                #if w.getCtx() is None:
                #    w.rst()
                return w
        return None
        #new_inst = class_name(ctx_name, ctx, init)
        #self.addWindowHelper(new_inst)
        #return new_inst

    def getWindowHelpers(self):
        return self._windowHelpers()

    def addWindowHelper(self, window_helper):
        self._windowHelpers.append(window_helper)
