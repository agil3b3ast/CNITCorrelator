import time
from ..windowhelper import WindowHelper
from..context import Context
from ..context import search as ctx_search

class WeakWindowHelper(WindowHelper):

    def __init__(self, name,ctx):
        super(WeakWindowHelper, self).__init__(name, ctx)
        self._origTime = time.time()


    def unbindContext(self):
        self._ctx = None

    def rst(self):
        self._origTime = time.time()

    def addIdmef(idmef):
        self._ctx.update(options=self._ctx.getOptions(), idmef=idmef)

    def checkCorrelationWindow(self):
        if self._ctx is None:
            return False

        now = time.time()

        if now - self._origTime < self._ctx.getOptions()["expire"]:
         # check number of alert received
         alert_received = self._ctx.get("alert.correlation_alert.alertident(*).analyzerid")
         if alert_received is None:
             alert_received = 0
         else:
             alert_received = len(alert_received)
         if alert_received >= self._ctx.getOptions()["threshold"]:
             return True
        else:
          self._ctx.destroy()
          self.unbindContext()

        return False

    def generateCorrelationAlert(self):
        tmp_ctx = ctx_search(self._name)
        self._ctx.destroy()
        self.unbindContext()
        tmp_ctx.alert()
