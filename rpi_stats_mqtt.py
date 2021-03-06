#!/usr/bin/env python3


import os
import psutil
import json
import paho.mqtt.client as mqtt
import time

"""
rpi-stats.py

Program to gather stats, format in a JSON string and send to Mosquitto
"""
def main():
    # collect OS stats
    disk = psutil.disk_usage('/')
    mem = psutil.virtual_memory()
    load = os.getloadavg()

    # Get the temperature
    temp = get_cpu_temp()

    # Create a dictionary object
    stats_dict = {
        "load_1": load[0],
        "load_5": load[1],
        "load_15": load[2],
        "mem_total": mem.total,
        "mem_used": mem.used,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "temp": temp
    }

    # Create a JSON string from the disctionary object
    stats_json = json.dumps(stats_dict)
    #print(stats_json)

    # Publish MQTT message
    mqtt.Client.connected_flag=False
    broker="192.168.12.27"

    client = mqtt.Client("rpi_stats_mqtt") # Create a MQTT client object
    client.username_pw_set(username="kintzel_mqtt",password="Bl00d$ucker")
    client.on_connect=on_connect  #bind call back function
    client.loop_start()  #Start loop
    #print("Connecting to broker ", broker)

    client.connect(broker,port=1883,keepalive=60,bind_address="")
    while not client.connected_flag:
        time.sleep(1)

    client.publish("rpi-stats", stats_json)

    client.loop_stop()  #Stop loop
    client.disconnect()



"""
Obtains the current value of the CPU temperature.
:returns: Current value of the CPU temperature if successful, zero value otherwise.
:rtype: float
"""
def get_cpu_temp():
    # Initialize the result.
    result = 0.0

    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            line = f.readline().strip()

        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000

    # Give the result back to the caller.
    return result


def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True
        #print("connected OK Returned code=",rc)
    #else:
        #print("Bad connection Returned code=", rc)


if __name__ == "__main__":
    main()
