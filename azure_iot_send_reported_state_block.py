from nio.properties import VersionProperty, Property
from nio import TerminatorBlock

from .azure_iot_base_block import AzureIoTBase


class AzureIoTSendReportedState(AzureIoTBase, TerminatorBlock):
    """A block to send reported state to Azure cloud.
    """
    version = VersionProperty("1.0.0")
    state_to_report = Property(title="State to Report",
                               default="{{ $.to_dict() }}", order=2)

    def process_signals(self, signals):
        for signal in signals:
            data = self.state_to_report(signal)
            if not isinstance(data, dict):
                self.logger.error("Data: {} rejected, a dict is expected".
                                  format(data))
                return

            self.logger.info("Sending: {}".format(data))
            self._client.send_reported_state(data)

    def get_callbacks(self):
        return {"reported_state_callback": self._reported_state_callback}

    def _reported_state_callback(self, result):
        self.logger.debug(
            "Confirmation for reported state received with result: {}".
            format(result))
