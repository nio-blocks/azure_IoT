from .client import AzureIoTClient

from nio.properties import (StringProperty, IntProperty)
from nio.util.discovery import not_discoverable


@not_discoverable
class AzureIoTBase(object):
    """The base block for Azure IoT.
    """

    connection_string = StringProperty(title="Connection String", order=10)

    # maximum time in milliseconds until a message times out
    message_timeout = IntProperty(title="Message Timeout", default=10000,
                                  advanced=True, order=21)

    def __init__(self):
        super().__init__()
        self._client = None

    def configure(self, context):
        """set up properties"""
        super().configure(context)

        self._client = AzureIoTClient(
            self.connection_string(),
            self.logger,
            message_timeout=self.message_timeout(),
            **self.get_callbacks()
        )

        self.connect()

    def stop(self):
        self.disconnect()
        super().stop()

    def connect(self):
        self.logger.debug("Connecting...")
        self._client.connect()

    def disconnect(self):
        self.logger.debug("Disconnecting...")
        self._client.disconnect()

    def get_callbacks(self):
        """ Overrideable method specifying data of interest

        Returns:
            key-value dictionary to be used as kwargs
        """
        return {}
