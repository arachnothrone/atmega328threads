#!/usr/bin/env python3

"""
Temperature & humidity AM2320 log parser, plots the graphs
"""

import sys
import re
import matplotlib.pyplot as plt

if __name__ == "__main__":
    USAGE = "Usage: temp_humid_char.py <log_file_name>\n"
    args = sys.argv
    if len(args) != 2:
        sys.exit(USAGE)

    plotData = []
    t = []
    h = []
    z = []
    file = args[1]
    with open(file, 'r') as f:
        for ln in f.readlines():
            # parsing line:
            # "Temperature: 24.00 C, Humidity: 37.90 % time[72805] s"
            parseObj = re.match(r'Temperature: (-?\d{1,2}\.\d{2}) C, Humidity: (\d{1,3}\.\d{2}) % time\[(\d*)\] s', ln)
            if parseObj:
                temp = parseObj.group(1)
                humidity = parseObj.group(2)
                time = parseObj.group(3)
            else:
                temp = 0
                humidity = 0
                time = 0
            plotData.append((temp, humidity, time))
            t.append(temp)
            h.append(humidity)
            z.append(time)

    # "compress" the data - take every 100th element
    # for i in range(0, len(t)):
    #     if i % 100 == 0:
    #         pass
    #     else:
    #         t.pop(i)
    #         h.pop(i)
    #         z.pop(i)
    t = t[::100]
    h = h[::100]
    z = z[::100]
    #print(plotData)
    #print(len(t), len(h), len(z))
    plt.plot(z, h)
    plt.show()
