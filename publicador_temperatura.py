import sys
import random
import time
import paho.mqtt.client

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=Moncho.azure-devices.net;DeviceId=casa_temperatura;SharedAccessKey=3HNOaskydMUrjIVci72HkzYcxESgVXsjdeeGx1XX0zg="
TEMPERATURE = 20.0

MSG_TXT = '{{"temperatura": {temperature}}}'

def iothub_client_init():
   
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
     

        while True:
           
            temperature = TEMPERATURE + (random.random() * 15)
          
            msg_txt_formatted = MSG_TXT.format(temperature=temperature)
            message = Message(msg_txt_formatted)

            
            if temperature > 30:
              message.custom_properties["Aviso_de_Temperatura"] = "Elevada"
            else:
              message.custom_properties["Aviso_de_Temperatura"] = "Correcta"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
   
    iothub_client_telemetry_sample_run()