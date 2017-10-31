import time
from ..windowhelper import WindowHelper
from..context import Context
from ..context import search as ctx_search

class WeakWindowHelper(WindowHelper):

    def __init__(self, name,ctx, initial_attrs):
        super(WeakWindowHelper, self).__init__(name, ctx, initial_attrs)
        self._origTime = time.time()


    def unbindContext(self):
        self._ctx = None

    def rst(self):
        self._origTime = time.time()

    def addIdmef(self, idmef):
        now = time.time()
        if now - self._origTime < self._ctx.getOptions()["expire"]:
         self._ctx.update(options=self._ctx.getOptions(), idmef=idmef)
        else:
          #window is expired
          self._ctx.destroy()
          self.rst()
          print("I am {} , Context is destroyed".format(self._name))
          tmp_ctx = Context(self._name, self._ctx.getOptions(), update = False)
          #tmp_ctx.set("alert.correlation_alert.name", self._ctx.get("alert.correlation_alert.name"))
          #tmp_ctx.set("alert.classification.text", self._ctx.get("alert.classification.text"))
          #tmp_ctx.set("alert.assessment.impact.severity", self._ctx.get("alert.assessment.impact.severity"))
          for key,value in self.initialAttrs:
              tmp_ctx.set(key,value)
          self._ctx = tmp_ctx
          self._ctx.update(options=self._ctx.getOptions(), idmef=idmef)


    def checkCorrelationWindow(self):

        #if now - self._origTime < self._ctx.getOptions()["expire"]:
         # check number of alert received
        alert_received = self._ctx.get("alert.correlation_alert.alertident(*).analyzerid")
        if alert_received is None:
         alert_received = 0
        else:
         alert_received = len(alert_received)
        print("I am {} : these are my alert received {}".format(self._name, alert_received))
        if alert_received >= self._ctx.getOptions()["threshold"]:
         return True
        #else:
        #  self._ctx.destroy()
        #  print("I am {} , Context is destroyed".format(self._name))
        #  self.unbindContext()

        return False

    def generateCorrelationAlert(self):
        tmp_ctx = ctx_search(self._name)
        self._ctx.destroy()
        self.unbindContext()
        self.rst()
        tmp_ctx.alert()
