import time
from ..windowhelper import WindowHelper
from..context import Context

class WeakWindowHelper(WindowHelper):

    def __init__(self, ctx):
        super(WeakWindowHelper, self).__init__(ctx)
        self._origTime = time.time()


    def unbindContext(self):
        self._ctx = None

    def rst():
        self._origTime = time.time()

    def addIdmef(idmef):
        self._ctx.update(options=self._ctx.getOptions(), idmef=idmef)

    def checkCorrelationWindow():
        if self._ctx is None:
            return False

        now = time.time()

        if now - self._origTime < self._ctx.getOptions()["expire"]:
         # remember that when we have a threshold of x reached, we have updated the context exactly x - 1 times
         if self._ctx.getUpdateCount() >= self._ctx.getOptions()["threshold"] - 1:
             #return True
             return True
        else:
          self._ctx.destroy()
          self.unbindContext()

        return False

    def generateCorrelationAlert():
        self._ctx.destroy()
        self.unbindContext()
        self._ctx.alert()
