import time
from ..contexthelper import ContextHelper
from..context import Context
from ..context import search as ctx_search

class WeakWindowHelper(ContextHelper):


    def __init__(self, name):
        super(WeakWindowHelper, self).__init__(name)
        self._origTime = time.time()
        self._received = 0


    def isEmpty(self):
        return ctx_search(self._name) is None


    def bindContext(self, options, initial_attrs):
        res = ctx_search(self._name)
        if res is None:
         self._ctx = Context(self._name, options, update=False)
         self._origTime = time.time()
         self._received = 0
        else:
         self._ctx = res
        self._options = options
        self.initialAttrs = initial_attrs
        for key,value in self.initialAttrs.iteritems():
         self._ctx.set(key,value)


    def _restoreContext(self, options, initial_attrs):
         self._ctx = Context(self._name, options, update=False)

         for key,value in initial_attrs.iteritems():
             self._ctx.set(key,value)

    def unbindContext(self):
        self._ctx = None

    def getIdmefField(self, idmef_field):
        return self._ctx.get(idmef_field)

    def setIdmefField(self, idmef_field, value):
        self._ctx.set(idmef_field, value)

    def rst(self):
        self._origTime = time.time()
        self._received = 0

    def processIdmef(self, idmef, addAlertReference=True):
        self._received = self._received + 1
        now = time.time()
        if now - self._origTime >= self._ctx.getOptions()["window"]:
            if self._ctx.getOptions()["reset_ctx_on_window_expiration"]:
                self._ctx.destroy()
                self._restoreContext(self._options, self._initialAttrs)
            self.rst()
        if addAlertReference:
            self._ctx.update(options=self._ctx.getOptions(), idmef=idmef, timer_rst=True)
        else:
            self._ctx.update(options=self._ctx.getOptions(), idmef=None, timer_rst=True)

    def countAlertsReceivedInWindow(self):
        #return self._ctx.getUpdateCount()
        return self._received

    def corrConditions(self):
        alert_received = self.countAlertsReceivedInWindow()
        #print("I am {}, alert received {}".format(self._name, alert_received))
        return alert_received >= self._ctx.getOptions()["threshold"]

    def checkCorrelation(self):
        return self._checkCorrelationWindow()

    def _checkCorrelationWindow(self):
         #alert_received = self._countAlertReceived()
         #print("I am {}, alert received {}".format(self._name, alert_received))
         #return alert_received >= self._ctx.getOptions()["threshold"]
         return self.corrConditions()

    def generateCorrelationAlert(self, send=True, destroy_ctx=False):
        tmp_ctx = ctx_search(self._name)
        if destroy_ctx:
            self._ctx.destroy()
            self.unbindContext()
        self.rst()
        if send:
            tmp_ctx.alert()
        else:
            return tmp_ctx
