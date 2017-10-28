from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.context import Context
from preludecorrelator.context import search as context_search
from preludecorrelator.windows.WeakWindowHelper import WeakWindowHelper
import time

LEVEL = 1
print("{}, {} Level Correlation".format("EntryLevelCorrelator", LEVEL))
#The context should be unique, it's better add the class name since we know it's unique
context_id = "{}Layer{}Correlation".format("EntryLevelCorrelator", LEVEL)

class EntryLevelCorrelator(Plugin):
    def run(self, idmef):
        #Receive only simple alerts, not correlation alerts
        if idmef.get("alert.correlation_alert.name") is not None:
         return

        if context_search(context_id) is None:
         ctx = Context(context_id, { "expire": 5, "threshold": 5, "window" : 1 ,"alert_on_expire": False }, update = False, idmef=idmef, windowhelper=WeakWindowHelper)
         #Create a context that:
         #- expires after 5 seconds of inactivity
         #- generates a correlation alert after 5 msg received
         #- checks for the threshold in a window of 1 second, if the window expires the correlation period restarts
         ctx.set("alert.correlation_alert.name", "Layer {} Correlation".format(LEVEL))
         ctx.set("alert.classification.text", "MyFirstEntryLevelScan")
         ctx.set("alert.assessment.impact.severity", "high")
        else:
         ctx.update(options={ "expire": 5, "threshold": 5, "window" : 1 ,"alert_on_expire": False }, idmef=idmef)

        if ctx.getWindowHelper().checkCorrelationWindow():
          print("Hello from {}".format(self.__class__.__name__))
          print(ctx.get("alert.classification.text"))
          ctx.alert()
          print("{} Alert finished".format(self.__class__.__name__))
