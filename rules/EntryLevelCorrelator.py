from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.context import Context
from preludecorrelator.context import search as context_search
#from preludecorrelator.windows.StrongWindowHelper import StrongWindowHelper
from preludecorrelator.windows.WeakWindowHelper import WeakWindowHelper

LEVEL = 1
print("{}, {} Level Correlation".format("EntryLevelCorrelator", LEVEL))
#The context should be unique, it's better add the class name since we know it's unique
context_id = "{}Layer{}Correlation".format("EntryLevelCorrelator", LEVEL)

class EntryLevelCorrelator(Plugin):
    def run(self, idmef):
        #Receive only simple alerts, not correlation alerts
        if idmef.get("alert.correlation_alert.name") is not None:
         return

        window = self.getWindowHelper(context_id)
        print(window)
        if window is None:
         options = { "expire": 1, "threshold": 5 ,"alert_on_expire": False }
         initial_attrs = {"alert.correlation_alert.name":"Layer {} Correlation".format(LEVEL),
         "alert.classification.text": "MyFirstEntryLevelScan",
         "alert.assessment.impact.severity": "high"}
         #Create a context that:
         #- expires after 1 seconds of inactivity
         #- generates a correlation alert after 5 msg received
         #- checks for the threshold in a window of 1 second, if the window expires the correlation period restarts
         window = self.bindCtxToNewWindow(WeakWindowHelper, context_id, options, initial_attrs)
        #window = self.getWindowHelper(StrongWindowHelper, context_id)
        window.addIdmef(idmef)

        if window.checkCorrelationWindow():
          print("Hello from {}".format(self.__class__.__name__))
          print(window.getCtx().get("alert.classification.text"))
          window.generateCorrelationAlert()
          print("{} Alert finished".format(self.__class__.__name__))
