from preludecorrelator.pluginmanager import Plugin
from preludecorrelator.contexthelpers.WeakWindowHelper import WeakWindowHelper
from preludecorrelator import log

LEVEL = 2
NUMBER = 1
context_id = "{}Layer{}Correlation{}".format("AdvancedLevelCorrelator", LEVEL, NUMBER)
logger = log.getLogger(__name__)

class ExtendedWindowHelper(WeakWindowHelper):

    def corrConditions(self):
        alert_received = self.countAlertsReceivedInWindow()
        return alert_received >= self._ctx.getOptions()["threshold"]

class AdvancedLevelCorrelator(Plugin):

    def __init__(self, env):
        super(AdvancedLevelCorrelator, self).__init__(env)
        logger.info("Loading %s", self.__class__.__name__)

    def run(self, idmef):
        corr_name = idmef.get("alert.correlation_alert.name")
        # We are not interested in simple alerts
        if corr_name is None:
         return
        # We do not want correlation alerts from upper layers
        if corr_name != "Layer {} Correlation".format(LEVEL - 1):
         return

        correlator = self.getContextHelper(context_id,ExtendedWindowHelper)


        if correlator.isEmpty():

            options = { "expire": 2, "threshold": 2 ,"alert_on_expire": False, "window": 2, "reset_ctx_on_window_expiration": True }
            initial_attrs = {"alert.correlation_alert.name": "Layer {} Correlation".format(LEVEL), "alert.classification.text": "MyFirstAdvancedLevelScan{}".format(NUMBER), "alert.assessment.impact.severity": "high"}

            correlator.bindContext(options, initial_attrs)


        correlator.processIdmef(idmef=idmef, addAlertReference=True)


        if correlator.checkCorrelation():
          correlator.generateCorrelationAlert(send=True, destroy_ctx=True)
