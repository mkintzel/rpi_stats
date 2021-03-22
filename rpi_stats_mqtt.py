#!/usr/bin/env python3


import os
import psutil
import json
import paho.mqtt.client as mqtt

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
    ourClient = mqtt.Client("kintzel_mqtt") # Create a MQTT client object
    ourClient.connect("192.168.12.27", 1883) # Connect to the test MQTT broker
    ourClient.publish("rpi-stats", stats_json)


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



if __name__ == "__main__":
    main()
