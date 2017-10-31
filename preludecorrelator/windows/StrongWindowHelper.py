import time
from ..windowhelper import WindowHelper
from ..context import Context
from ..idmef import AnalyzerContents
from ..context import search as ctx_search


class StrongWindowHelper(WindowHelper):

    def __init__(self, name, ctx):
        super(StrongWindowHelper, self).__init__(name, ctx)
        self._timestamps = []


    def unbindContext(self):
        self._ctx = None

    def rst(self):
        self._timestamps = []

    def addIdmef(self, idmef):
        tmp_analyzer = AnalyzerContents()
        tmp_analyzer.saveAnalyzerContents(idmef)
        self._timestamps.append([time.time(),idmef, tmp_analyzer])

    def checkCorrelationWindow(self):
        if self._ctx is None:
            return False

        now = time.time()
        len_timestamps = len(self._timestamps)
        print("I am {} : len timestamps {}".format(self._name, len_timestamps))
        counter = 0
        for t in range(len_timestamps-1,-1,-1):
            print("I am {} : timestamps[{}] < {}".format(self._name, t,self._ctx.getOptions()["expire"]))
            if now - self._timestamps[t][0] < self._ctx.getOptions()["expire"]:
             counter = counter + 1
             print("I am {} : reaching threshold with counter {}".format(self._name, counter))
             if counter >= self._ctx.getOptions()["threshold"]:
                 print("I am {} : threshold reached".format(self._name))
                 for c in range(t,t+counter):
                     self._timestamps[t][2].restoreAnalyzerContents(self._timestamps[t][1])
                     self._ctx.update(options=self._ctx.getOptions(), idmef=self._timestamps[t][1])
                 #self._ctx.destroy()
                 #self.unbindContext()
                 return True
            else:
              print("I am {} : del timestamps[{}]".format(self._name, t))
              self._timestamps.pop(t)

        return False

    def generateCorrelationAlert(self):
        tmp_ctx = ctx_search(self._name)
        self._ctx.destroy()
        self.unbindContext()
        tmp_ctx.alert()
