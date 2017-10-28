from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.context import Context
from preludecorrelator.context import search as context_search
from preludecorrelator.windows.WeakWindowHelper import WeakWindowHelper

LEVEL = 2
print("{}, Layer {} Correlation2".format("AdvancedLevelCorrelator", LEVEL))
context_id = "{}Layer{}Correlation2".format("AdvancedLevelCorrelator", LEVEL)


class AdvancedLevelCorrelator22(Plugin):

    def run(self, idmef):
        corr_name = idmef.get("alert.correlation_alert.name")
        # We are not interested in simple alerts
        if corr_name is None:
         return
        # We do not want correlation alerts from upper layers
        if corr_name != "Layer {} Correlation".format(LEVEL - 1):
         return

        print("{} received correlation".format(self.__class__.__name__))
        print(corr_name)

        ctx = context_search( context_id)
        if ctx is None:
         ctx = Context( context_id, { "expire": 5, "threshold": 2, "window" : 1 ,"alert_on_expire": False }, update = False, idmef=idmef, windowHelper=WeakWindowHelper)
         ctx.set("alert.correlation_alert.name", "Layer 2 Correlation")
         ctx.set("alert.classification.text", "MyFirstAdvancedLevelScan2")
         ctx.set("alert.assessment.impact.severity", "high")
        else:
         ctx.update(options={ "expire": 5, "threshold": 2, "window" : 1 ,"alert_on_expire": False }, idmef=idmef)

        if ctx.getWindowHelper().checkCorrelationWindow():
          print("Hello from %s" % self.__class__.__name__)
          print(ctx.get("alert.classification.text"))
          ctx.alert()
          print("Alert Finished AdvancedLevelCorrelator2")
