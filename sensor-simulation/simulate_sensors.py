import time
import random
from azure.iot.device import IoTHubDeviceClient, Message
from datetime import datetime

devices = {
    "Dow's Lake": "HostName=skateway-hub.azure-devices.net;DeviceId=sensor-dowslak;SharedAccessKey=ziEzHtRi8CIYe1If0aQHn7SAJ+CNrHBOFeNxxrBMSCA=",
    "Fifth Avenue": "HostName=skateway-hub.azure-devices.net;DeviceId=sensor-fifthave;SharedAccessKey=cWY09zgfBW/X6XuqYX3OE7xKkKV8E4A2uXPiQHMgqUs=",
    "NAC": "HostName=skateway-hub.azure-devices.net;DeviceId=sensor-nac;SharedAccessKey=lsjhC/nonLejsOtUQqojH5I3JM/I7MpjD+ermGegOgY="
}

def generate_payload(location):
    payload = {
        "location": location,
        "iceThickness": random.randint(20, 35),
        "surfaceTemperature": random.randint(-10, 2),
        "snowAccumulation": random.randint(0, 15),
        "externalTemperature": random.randint(-15, 5),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    return payload

def send_data():
    while True:
        for location, conn_str in devices.items():
            client = IoTHubDeviceClient.create_from_connection_string(conn_str)
            payload = generate_payload(location)
            msg = Message(str(payload))
            print(f"Sending from {location}: {msg}")
            client.send_message(msg)
            client.disconnect()
        time.sleep(10)

if __name__ == "__main__":
    send_data()

