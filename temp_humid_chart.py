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
    p = []
    temp, humidity, time, pressure = 26.0, 50.0, 19, 733.0
    file = args[1]
    with open(file, 'r') as f:
        for ln in f.readlines():
            # parsing lines:
            # "AM2320: Temperature: 25.60 C, Humidity: 58.80 % time[39] s
            # "BMP180: Temperature: 25.20 C, Pressure: 736.37 mmhHg, Alt: 266.48m, Pressure (sea level): 98164"
            # "Temperature: 25.60 C, Humidity: 39.10 %, Pressure: 746.66 mmHg"
            #parseObjAm2320 = re.match(r'AM2320: Temperature: (-?\d{1,2}\.\d{2}) C, Humidity: (\d{1,3}\.\d{2}) % time\[(\d*)\] s', ln)
            #parseObjBmp180 = re.match(r'BMP180: Temperature: (-?\d{1,2}\.\d{2}) C, Pressure: (\d{1,3}\.\d{2}) mmhHg, Alt: (\d{1,3}\.\d{2})m, Pressure \(sea level\): (\d{1,6})', ln)
            parseObj = re.match(r'Temperature: (-?\d{1,2}\.\d{2}) C, Humidity: (\d{1,3}\.\d{2}) %, Pressure: (\d{1,3}\.\d{2}) mmHg', ln)
            if parseObj:
                temp = parseObj.group(1)
                humd = parseObj.group(2)
                pres = parseObj.group(3)
            # if parseObjAm2320:
            #     temp = parseObjAm2320.group(1)
            #     humidity = parseObjAm2320.group(2)
            #     time = parseObjAm2320.group(3)
            # else:
            #     pass
            #     # temp = 0
            #     # humidity = 0
            #     # time = 0
            # if parseObjBmp180:
            #     pressure = parseObjBmp180.group(2)
            # else:
            #     pass
            #     # pressure = 0
            # #plotData.append((temp, humidity, time))
                t.append(temp)
                h.append(humd)
                #z.append(time)
                p.append(pres)


    # reduce the number of points, take every 20th, and convert elements from String to float/int
    t = [float(x) for x in t]  # in t[::20]
    h = [float(x) for x in h]
    p = [float(x) for x in p]
    #z = [int(x) for x in z]
    # t = float(t)
    # h = float(h)
    # z = int(z)

    outputFile1 = open("temperature.log", 'w')
    outputFile2 = open("humidity.log", 'w')
    outputFile3 = open("pressure.log", 'w')
    #outputFile.write("Time, temperature C, humidity %, pressure mmHg\n")
    for (number, tt, hh, pp) in zip(list(range(len(t))), t, h, p):
        outputFile1.write("{}\t{}\n".format(number, tt))
        outputFile2.write("{}\t{}\n".format(number, hh))
        outputFile3.write("{}\t{}\n".format(number, pp))

    outputFile1.close()
    outputFile2.close()
    outputFile3.close()

    # -------------- Matplotlib -----------------------------------
    # outputFile = open("temphumid.log", 'w')
    # outputFile.write("Time, temperature C, humidity %\n")
    # for (tt, hh, zz) in zip(t, h, z):
    #     outputFile.write("{}, {}, {}\n".format(zz, tt, hh))
    #     print("time: {0:10}  temp = {1:3.1f}  humid = {2:3.1f}".format(zz, tt, hh))
    # outputFile.close()
    # #print(plotData)
    # #print(len(t), len(h), len(z))
    # # plt.plot(z, h)
    # # plt.show()
    #
    # # Plot the graphs
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # ax1.plot(z, t, 'b-', label='temperature, C')
    # ax1.set_xlabel('time, seconds', color='grey')
    #
    # ax2 = ax1.twinx()
    # ax2.plot(z, h, 'r-', label='humidity, %')
    #
    # ax3 = ax2.twinx()
    # ax3.plot(z, p, 'y-', label='pressure, mmHg')
    #
    # fig.legend()
    #
    # for tl in ax1.get_yticklabels():
    #     tl.set_color('b')
    # for tl in ax2.get_yticklabels():
    #     tl.set_color('r')
    # for tl in ax3.get_yticklabels():
    #     tl.set_color('y')
    #
    # plt.show()
    # ------------------------------------------------------------
