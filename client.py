import json

from iothub_client import IoTHubClient, IoTHubTransportProvider
from iothub_client import IoTHubMessage, IoTHubMessageDispositionResult


RECEIVE_CONTEXT = 0
TWIN_CONTEXT = 0


def noop(*a, **k):
    pass


# JSONDecodeError is only raised in python 3.5 and above
try:
    json_decode_error = json.JSONDecodeErrorsaer
except (ImportError, AttributeError):
    json_decode_error = ValueError


class AzureIoTClient(object):

    def __init__(self,
                 connection_string,
                 logger,
                 protocol=IoTHubTransportProvider.MQTT,
                 message_timeout=10000,
                 # Callback handlers
                 receive_message_callback=noop,
                 send_event_callback=noop,
                 reported_state_callback=noop
                 ):
        self._connection_string = connection_string
        self._logger = logger
        self._protocol = protocol
        self._message_timeout = message_timeout

        self.receive_message_callback = receive_message_callback
        self.send_event_callback = send_event_callback
        self.reported_state_callback = reported_state_callback

        self.client = None

        self._send_context = 0
        self._reported_state_context = 0

    def connect(self):
        self._logger.info("Connecting")
        self.client = IoTHubClient(self._connection_string, self._protocol)
        # set the time until a message times out
        self.client.set_option("messageTimeout", self._message_timeout)

        self.client.set_message_callback(self._receive_message_callback,
                                         RECEIVE_CONTEXT)

    def disconnect(self):
        self._logger.info("Disconnecting")
        self.client = None

    def _receive_message_callback(self, message, context):
        message_buffer = message.get_bytearray()
        size = len(message_buffer)
        body = message_buffer[:size].decode('utf-8')
        self._logger.debug("Data: {}, Size={}, counter".
                           format(body, size, context))

        map_properties = message.properties()
        properties = map_properties.get_internals()
        self._logger.debug("    Properties: {}".format(properties))

        if self.receive_message_callback:
            try:
                body = json.loads(body)
            except (json_decode_error, ValueError):
                # ignore if no json, pass it to callback as decoded body
                pass

            try:
                self.receive_message_callback(body, properties)
            except ValueError:
                return IoTHubMessageDispositionResult.REJECTED

        return IoTHubMessageDispositionResult.ACCEPTED

    def send_event(self, event, properties=None):
        """ Sends an event

        Args:
            event (dict): event values
            properties (dict): values to send as properties
        """
        if not isinstance(event, IoTHubMessage):
            event = json.dumps(event)
            event = IoTHubMessage(bytearray(event, 'utf8'))

        if properties and len(properties) > 0:
            prop_map = event.properties()
            for key in properties:
                prop_map.add_or_update(key, properties[key])

        self.client.send_event_async(
            event, self._send_event_callback, self._send_context)
        self._send_context += 1

    def _send_event_callback(self, message, result, user_context):
        self._logger.debug(
            "Confirmation[{}] received for send event message, result: {}".
            format(user_context, result))
        map_properties = message.properties()
        key_value_pair = map_properties.get_internals()
        self._logger.debug("Properties: {}".format(key_value_pair))

        # notify block is requested
        if self.send_event_callback:
            self.send_event_callback(result, key_value_pair)

    def send_reported_state(self, reported_state):
        """ Sends a reported state

        Args:
            reported_state (dict): state to report
        """
        reported_state = json.dumps(reported_state)
        self.client.send_reported_state(
            reported_state, len(reported_state),
            self._send_reported_state_callback, self._reported_state_context)
        self._reported_state_context += 1

    def _send_reported_state_callback(self, result, user_context):
        self._logger.debug(
            "Confirmation for reported state received with:"
            "\nresult = {}\ncontext = {}".
            format(result, user_context))

        # notify block is requested
        if self.reported_state_callback:
            self.reported_state_callback(result)
