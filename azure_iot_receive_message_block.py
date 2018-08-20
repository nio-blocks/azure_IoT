from nio.properties import VersionProperty
from nio import GeneratorBlock
from nio.signal.base import Signal

from .azure_iot_base_block import AzureIoTBase


class AzureIoTReceiveMessage(AzureIoTBase, GeneratorBlock):
    """A block to receive messages from Azure cloud.
    """

    version = VersionProperty("1.0.0")

    def get_callbacks(self):
        return {"receive_message_callback": self._handle_message}

    def _handle_message(self, body, properties):
        """ Receives a message sent from Azure's cloud broker

        Args:
            body (dict or decoded body): Body comes as a dict if conversion
                was successful otherwise comes as a decoded body
            properties (dict): key-value properties as a dictionary
        """
        self.notify_signals([Signal({"body": body,
                                     "properties": properties
                                     })])
