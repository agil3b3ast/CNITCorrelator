import time
from preludecorrelator.windowhelper import WindowHelper

class WeakWindowHelper(WindowHelper):

    def __init__(self, ctx):
        super(WeakWindowHelper, self).__init__(ctx)
        self._origTime = time.time()

    def checkCorrelationWindow(self):
        now = time.time()

        if now - self._origTime < self._ctx.getOptions()["window"]:
         # remember that when we have a threshold of x reached, we have updated the context exactly x - 1 times
         if self._ctx.getUpdateCount() >= self._ctx.getOptions()["threshold"] - 1:
             return True
        else:
          self._origTime = time.time()
        return False
