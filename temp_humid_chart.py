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

    # reduce the number of points, take every 20th, and convert elements from String to float/int
    t = [float(x) for x in t[::20]]
    h = [float(x) for x in h[::20]]
    z = [int(x) for x in z[::20]]

    outputFile = open("temphumid.log", 'w')
    outputFile.write("Time, temperature C, humidity %\n")
    for (tt, hh, zz) in zip(t, h, z):
        outputFile.write("{}, {}, {}\n".format(zz, tt, hh))
        print("time: {0:10}  temp = {1:3.1f}  humid = {2:3.1f}".format(zz, tt, hh))
    outputFile.close()
    #print(plotData)
    #print(len(t), len(h), len(z))
    # plt.plot(z, h)
    # plt.show()

    # Plot the graphs
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(z, t, 'b-', label='temperature, C')
    ax1.set_xlabel('time, seconds', color='grey')

    ax2 = ax1.twinx()
    ax2.plot(z, h, 'r-', label='humidity, %')

    fig.legend()

    for tl in ax1.get_yticklabels():
        tl.set_color('b')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')

    plt.show()
