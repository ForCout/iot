import sys
import paho.mqtt.client

from azure.eventhub import TransportType
from azure.eventhub import EventHubConsumerClient

# Event Hub-compatible endpoint

EVENTHUB_COMPATIBLE_ENDPOINT = "sb://ihsuprodparres004dednamespace.servicebus.windows.net/"


# Event Hub-compatible name

EVENTHUB_COMPATIBLE_PATH = "iothub-ehub-moncho-10784903-9afa4f7ca8"

# Primary key 
IOTHUB_SAS_KEY ="pQ8k3QcM+G9REQs6P5plCwHhlA5CgLVXDBPmPddxKsQ="



CONNECTION_STR = f'Endpoint={EVENTHUB_COMPATIBLE_ENDPOINT}/;SharedAccessKeyName=service;SharedAccessKey={IOTHUB_SAS_KEY};EntityPath={EVENTHUB_COMPATIBLE_PATH}'

# Define callbacks to process events
def on_event_batch(partition_context, events):
    for event in events:
        print("Received event from partition: {}.".format(partition_context.partition_id))
        print("Telemetry received: ", event.body_as_str())
        print("Properties (set by device): ", event.properties)
        print("System properties (set by IoT Hub): ", event.system_properties)
        print()
    partition_context.update_checkpoint()

def on_error(partition_context, error):

    if partition_context:
        print("An exception: {} occurred during receiving from Partition: {}.".format(
            partition_context.partition_id,
            error
        ))
    else:
        print("An exception: {} occurred during the load balance process.".format(error))


def main():
    client = EventHubConsumerClient.from_connection_string(
        conn_str=CONNECTION_STR,
        consumer_group="$default",
      
    )
    try:
        with client:
            client.receive_batch(
                on_event_batch=on_event_batch,
                on_error=on_error
            )
    except KeyboardInterrupt:
        print("Receiving has stopped.")

if __name__ == '__main__':
    main()