### Plots all of the intensity readings when pieces are in and out ###

import matplotlib.pyplot as plt

"""Gets the data from a csv file"""
def getData(fileName):
    data = []
    file = open(fileName,"r")
    for line in file:
        stripped = line.replace(" ","")
        values = stripped.split(",")
        data.append(values)
    file.close()
    return data

"""Returns a column of the specified data"""
def getColumn(columnNumber, data):#columnNumber starts at 0(timestamp)
    column_data = []
    for sample in data:
        value = float(sample[columnNumber])
        column_data.append(int(value))#converting it to an int as all the values are integers
    return column_data

"""Gets the frequency of each value in given data"""
def getDistribution(data):
    MAX_VALUE = 4096
    distribution_dict = {}
    for value in data:
        if(value in distribution_dict):
            distribution_dict[value] += 1
        else:
            distribution_dict[value] = 1
    return distribution_dict

"""Plots the distribution"""
def plotDistribution(distribution, style):
    keys = list(distribution.keys())
    keys.sort()
    x = []
    y = []
    for key in keys:
        x.append(key)
        y.append(distribution[key])
    ax.plot(x,y, linestyle=style)


"""Gets the LDR resistance given a sensor value"""
def getResistance(sensorValue):
    KNOWN_RESISTANCE = 2000
    if(sensorValue == 0):
        sensorValue = 1
        #prevents divide by 0
    resistance = ((4095.0 / sensorValue) - 1) * KNOWN_RESISTANCE
    return resistance

"""Gets the light intensity given a sensor value"""
def getIntensity(sensorValue):
    resistance = getResistance(sensorValue)
    return 1600000000 * (resistance ** -1.75)

#The csv file structure:
#time, red_led,green_led,blue_led, piece1, piece2, piece3,  piece4, piece5, piece6,  piece7, piece8, piece9

# 0      1       2          3        4       5       6         7       8      9         10     11      12

#Creates the graph
fig = plt.figure()
ax = plt.axes()
plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.title("Intensities when pieces in and out")

#Loops through each piece and adds it to the graph
PIECES = 9
for i in range(PIECES):
    #gets the raw data
    out_raw = getColumn(i + 4, getData("intensities_out.csv"))
    in_raw = getColumn(i + 4, getData("intensities_in.csv"))

    #calculates the intensities
    out_intensities = [getIntensity(x) for x in out_raw]
    in_intensities = [getIntensity(x) for x in in_raw]

    #calculates the frequency of each intensity value
    out_distribution = getDistribution(out_intensities)
    in_distribution = getDistribution(in_intensities)

    #plots this data on the chart
    plotDistribution(out_distribution, "dashed")
    plotDistribution(in_distribution, "solid")

#Displays the graph
plt.show()