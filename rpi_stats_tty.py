#!/usr/bin/env python3


import os
import psutil

"""
rpi-stats.py

Program to gather stats, format and print on the screen
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

    print(stats_dict)



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
