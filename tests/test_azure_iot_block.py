from unittest.mock import patch, Mock

from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal
from nio import Block

from ..azure_iot_base_block import AzureIoTBase
from ..azure_iot_send_event_block import AzureIoTSendEvent
from ..azure_iot_send_reported_state_block import AzureIoTSendReportedState
from ..azure_iot_receive_message_block import AzureIoTReceiveMessage

class TestAzureBase(NIOBlockTestCase):

    @patch("{}.{}".format(AzureIoTBase.__module__, 'AzureIoTClient'))
    def test_configure(self, patched_client):
        """Assert connect/disconnect calls."""

        class AzureIoTBlock(AzureIoTBase, Block):
            pass

        blk = AzureIoTBlock()
        blk.connection_string = "my_conn_string"

        self.assertEqual(patched_client.call_count, 0)

        self.configure_block(blk, {})
        blk.start()
        blk.stop()
        self.assertEqual(blk._client.connect.call_count, 1)
        self.assertEqual(blk._client.disconnect.call_count, 1)
        self.assertEqual(patched_client.call_count, 1)


class TestAzureSendEvent(NIOBlockTestCase):

    @patch("{}.{}".format(AzureIoTBase.__module__, 'AzureIoTClient'))
    def test_process_signals(self, patched_client):

        blk = AzureIoTSendEvent()
        blk.connection_string = "my_conn_string"

        self.assertEqual(patched_client.call_count, 0)
        self.configure_block(blk, {})
        self.assertEqual(patched_client.call_count, 1)

        blk.start()
        self.assertEqual(blk._client.send_event.call_count, 0)
        payload = {"text": "hello"}
        blk.process_signals([Signal(payload)])
        self.assertEqual(blk._client.send_event.call_count, 1)
        args, = blk._client.send_event.call_args_list[0][0]
        self.assertDictEqual(args, payload)
        blk.stop()

        self.assert_num_signals_notified(0)

        self.assertEqual(patched_client.call_count, 1)


class TestAzureSendReportedState(NIOBlockTestCase):

    @patch("{}.{}".format(AzureIoTBase.__module__, 'AzureIoTClient'))
    def test_process_signals(self, patched_client):

        blk = AzureIoTSendReportedState()
        blk.connection_string = "my_conn_string"

        self.assertEqual(patched_client.call_count, 0)
        self.configure_block(blk, {})
        self.assertEqual(patched_client.call_count, 1)

        blk.start()
        self.assertEqual(blk._client.send_reported_state.call_count, 0)
        payload = {"text": "hello"}
        blk.process_signals([Signal(payload)])
        self.assertEqual(blk._client.send_reported_state.call_count, 1)
        args, = blk._client.send_reported_state.call_args_list[0][0]
        self.assertDictEqual(args, payload)
        blk.stop()

        self.assert_num_signals_notified(0)

        self.assertEqual(patched_client.call_count, 1)


class TestAzureReceiveMessage(NIOBlockTestCase):

    @patch("{}.{}".format(AzureIoTBase.__module__, 'AzureIoTClient'))
    def test_process_signals(self, patched_client):

        blk = AzureIoTReceiveMessage()
        blk.notify_signals = Mock()
        blk.connection_string = "my_conn_string"

        self.assertEqual(patched_client.call_count, 0)
        self.configure_block(blk, {})
        self.assertEqual(patched_client.call_count, 1)

        blk.start()
        self.assertEqual(blk.notify_signals.call_count, 0)
        body = {"body_key": "body_key_value"}
        properties = {"property1": "property1_value"}
        blk._handle_message(body, properties)
        self.assertEqual(blk.notify_signals.call_count, 1)
        expected_args = {
            "body": body,
            "properties": properties
        }
        args, = blk.notify_signals.call_args_list[0][0]
        self.assertDictEqual(args[0].to_dict(), expected_args)
        blk.stop()

        self.assertEqual(patched_client.call_count, 1)
