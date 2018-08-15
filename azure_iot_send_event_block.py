from nio.properties import VersionProperty, Property
from nio import TerminatorBlock

from .azure_iot_base_block import AzureIoTBase


class AzureIoTSendEvent(AzureIoTBase, TerminatorBlock):
    """A block to send events to Azure cloud.
    """

    version = VersionProperty("1.0.0")
    event_to_send = Property(title="Event to Send",
                             default="{{ $.to_dict() }}", order=2)

    def process_signals(self, signals):
        for signal in signals:
            data = self.event_to_send(signal)
            if not isinstance(data, dict):
                self.logger.error("Data: {} rejected, a dict is expected".
                                  format(data))
                return

            self.logger.info("Sending: {}".format(data))
            self._client.send_event(data)

    def get_callbacks(self):
        return {"send_event_callback": self._send_event_callback}

    def _send_event_callback(self, result, message):
        self.logger.info(
            "Confirmation for event sent received with result: {} "
            "and message: {}".format(result, message))
