from context import search as ctx_search
from context import getName as getCtxName

class WindowHelper(object):

    def __init__(self, name):
        self._name = getCtxName(name)
        self._options = {}
        self._initialAttrs = {}
        self._ctx = None

    def getOptions(self):
        return self._options

    def setOptions(self, options):
        self._options = options

    def getInitialAttrs(self):
        return self._initialAttrs

    def setInitialAttrs(self, initial_attrs):
        self._initialAttrs = initial_attrs

    def getCtx(self):
        return self._ctx

    def isEmpty(self):
        pass

    def getIdmefField(self, idmef_field):
        pass

    def setIdmefField(self, idmef_field, value):
        pass

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

    def bindContext(self, options, initial_attrs):
        pass

    def unbindContext(self):
        pass


class WindowHolder(object):

    def __init__(self):
        self._windowHelpers = []

    def getWindowHelper(self, class_name, ctx_name):
        for w in self._windowHelpers:
            if w.getName() == getCtxName(ctx_name):
                return w
        new_inst = class_name(ctx_name)
        self.addWindowHelper(new_inst)
        return new_inst



    '''
    def bindWindowHelper(self, class_name, ctx_name):
        ctx = ctx_search(ctx_name)
        if ctx is None:
            return None
        for w in self._windowHelpers:
            if w.getName() == getCtxName(ctx_name):
                if w.getCtx() is None:
                    w.setCtx(ctx)
                    w.rst()
                return w
        new_inst = class_name(ctx, ctx_name)
        self.addWindowHelper(new_inst)
        return new_inst
    '''

    def getWindowHelpers(self):
        return self._windowHelpers()

    def addWindowHelper(self, window_helper):
        self._windowHelpers.append(window_helper)
