import time
from ..windowhelper import WindowHelper
from preludecorrelator.context import Context

class WeakWindowHelper(WindowHelper):

    def __init__(self, name, ctx_options=None, correlation_attrs=None, ctx_restart=False):
        super(WeakWindowHelper, self).__init__(name, ctx_options, correlation_attrs)
        self._correlationAttrs = correlation_attrs
        self._name = name
        self._ctxRestart = False
        if ctx_options is not None:
            self.addCtx(name, ctx_options, correlation_attrs)

    @staticmethod
    def getWindow(window_holder, name, ctx_options=None, correlation_attrs=None):
        for w in window_holder.getWindowHelpers():
            if w.name == name:
                return w
        window_holder.addWindowHelper(WeakWindowHelper(name, ctx_options, correlation_attrs))

    def isEmpty():
        if hasattr(self, '_ctx'):
            if self._ctx is not None:
                return True
        return False

    def addCtx(name, ctx_options, correlation_attrs=None):
        #check if updateCount increments
        self._ctx = Context(name=self._name, options=ctx_options, update=True)
        self._ctxOptions = ctx_options
        if correlation_attrs is not None:
            self._setCtxCorrelationAttrs(self._ctx)
        self._origTime = time.time()

    def setCorrelationAttrs(self, correlation_attrs):
        self._correlationAttrs = correlation_attrs

    def _setCtxCorrelationAttrs(self, ctx, correlation_attrs):
        for key,value in correlation_attrs.iteritems():
            ctx.set(key,value)
        return ctx

    def checkCorrelationWindow(self, idmef):
        if self._ctx is None:
            return None

        self._ctx = Context(name=self._name, options=self.ctx_options, update=True, idmef=idmef)

        now = time.time()

        if now - self._origTime < self._ctx.getOptions()["expire"]:
         # remember that when we have a threshold of x reached, we have updated the context exactly x - 1 times
         if self._ctx.getUpdateCount() >= self._ctx.getOptions()["threshold"] - 1:
             #return True
             self._ctx.destroy()
             return self._ctx
        else:
          #self._origTime = time.time()
          self._ctx.destroy()
          # from another WindowHelper you can check that the WindowHelper is empty to destroy it
          if self._ctxRestart:
              self._ctx = Context(name=self._name, options=self.ctx_options, update=True, idmef=idmef)
              self._origTime = time.time()

        #return False
        return None
