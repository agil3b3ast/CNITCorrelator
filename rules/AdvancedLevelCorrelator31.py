from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.contexthelpers.WeakContextHelper import WeakContextHelper

LEVEL = 3
print("{}, Layer {} Correlation".format("AdvancedLevelCorrelator", LEVEL))
context_id = "{}Layer{}Correlation".format("AdvancedLevelCorrelator", LEVEL)


class AdvancedLevelCorrelator31(Plugin):

    def run(self, idmef):
        corr_name = idmef.get("alert.correlation_alert.name")
        # We are not interested in simple alerts
        if corr_name is None:
         return
        # We do not want correlation alerts from upper layers
        if corr_name != "Layer {} Correlation".format(LEVEL - 1):
         return

        print("{} received correlation".format(self.__class__.__name__))

        ctx = WeakContextHelper( context_id, { "expire": 1, "threshold": 2 ,"alert_on_expire": False }, update = True, idmef=idmef)
        if ctx.getUpdateCount() == 0:
         ctx.set("alert.correlation_alert.name", "Layer 3 Correlation")
         ctx.set("alert.classification.text", "MyFirstAdvancedLevelScan31")
         ctx.set("alert.assessment.impact.severity", "high")

        if ctx.checkCorrelationAlert():
          print("Hello from %s" % self.__class__.__name__)
          print(ctx.get("alert.classification.text"))
          ctx.alert()
          print("Alert Finished AdvancedLevelCorrelator31")