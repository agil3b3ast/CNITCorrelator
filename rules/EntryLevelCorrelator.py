from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.context import Context
from preludecorrelator.context import search as context_search
from preludecorrelator.windows.StrongWindowHelper import StrongWindowHelper

LEVEL = 1
print("{}, {} Level Correlation".format("EntryLevelCorrelator", LEVEL))
#The context should be unique, it's better add the class name since we know it's unique
context_id = "{}Layer{}Correlation".format("EntryLevelCorrelator", LEVEL)

class EntryLevelCorrelator(Plugin):
    def run(self, idmef):
        #Receive only simple alerts, not correlation alerts
        if idmef.get("alert.correlation_alert.name") is not None:
         return

        ctx = context_search(context_id)
        if ctx is None:
         ctx = Context(context_id, { "expire": 1, "threshold": 5, "window" : 1 ,"alert_on_expire": False }, update = False)
         #Create a context that:
         #- expires after 5 seconds of inactivity
         #- generates a correlation alert after 5 msg received
         #- checks for the threshold in a window of 1 second, if the window expires the correlation period restarts
         ctx.set("alert.correlation_alert.name", "Layer {} Correlation".format(LEVEL))
         ctx.set("alert.classification.text", "MyFirstEntryLevelScan")
         ctx.set("alert.assessment.impact.severity", "high")

        window = self.getWindowHelper(StrongWindowHelper, context_id)
        window.addIdmef(idmef)

        if window.checkCorrelationWindow():
          print("Hello from {}".format(self.__class__.__name__))
          print(window.getCtx().get("alert.classification.text"))
          window.generateCorrelationAlert()
          print("{} Alert finished".format(self.__class__.__name__))
