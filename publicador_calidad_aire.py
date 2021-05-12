import sys
import random
import time
import paho.mqtt.client

from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=Moncho.azure-devices.net;DeviceId=jardin_calidad_aire;SharedAccessKey=64Vz3BOz42ioYujUU9KxdaCtsmznXWKT6IFySoVK/Ps="
CALIDAD_AIRE = 50.0

MSG_TXT = '{{"Calidad_Aire": {wind}}}'

def iothub_client_init():
   
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():

    try:
        client = iothub_client_init()
     

        while True:
           
            aire = CALIDAD_AIRE + (random.random() * 15)
          
            msg_txt_formatted = MSG_TXT.format(wind=aire)
            message = Message(msg_txt_formatted)

            
            if aire > 100:
              message.custom_properties["Aviso_de_Calidad_Aire"] = "Contaminacion"
            else:
              message.custom_properties["Aviso_de_Calidad_Aire"] = "Nivel contaminacion correcto"

            # Send the message.
            print( "Sending message: {}".format(message) )
            client.send_message(message)
            print ( "Message successfully sent" )
            time.sleep(1)

    except KeyboardInterrupt:
        print ( "IoTHubClient sample stopped" )

if __name__ == '__main__':
   
    iothub_client_telemetry_sample_run()