from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.idmef import IDMEF
from preludecorrelator.context import Context


print("SimpleCorrelator")

class SimpleCorrelator(Plugin):
    def run(self, idmef):
         ctx = Context(context_id, { "expire": 5, "threshold": 5, "window" : 1 ,"alert_on_expire": False }, update = True, idmef=idmef)
         if ctx.getUpdateCount() == 0:
             ctx.set("alert.correlation_alert.name", "Layer {} Correlation".format(LEVEL))
             ctx.set("alert.classification.text", "MyFirstEntryLevelScan")
             ctx.set("alert.assessment.impact.severity", "high")

        if ctx.getUpdateCount() >= ctx.getOptions()["threshold"] - 1:
          print("Hello from {}".format(self.__class__.__name__))
          print(ctx.get("alert.classification.text"))
          ctx.alert()
          print("{} Alert finished".format(self.__class__.__name__))
