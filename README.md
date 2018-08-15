AzureIoTReceiveMessage
====================
Block to receive messages from Azure IoT's cloud broker.

Properties
----------
- **connection_string**: Device connection string.
- **message_timeout**: Maximum time in milliseconds until a message times out.

Inputs
------
None

Outputs
-------
- **default**: Messages received from Azure IoT's cloud broker.

Commands
--------
None

Dependencies
------------
* azure-iothub-device-client

***

AzureIoTSendEvent
====================
Block to send events to Azure IoT's cloud broker.

Properties
----------
- **connection_string**: Device connection string.
- **message_timeout**: Maximum time in milliseconds until a message times out.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
* azure-iothub-device-client

***

AzureIoTSendReportedState
====================
Block to send reported states to Azure IoT's cloud broker.

Properties
----------
- **connection_string**: Device connection string.
- **message_timeout**: Maximum time in milliseconds until a message times out.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
* azure-iothub-device-client
