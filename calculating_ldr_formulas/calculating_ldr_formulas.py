### Combines, transforms and outputs provided data, so it can be processed further in Excel ###

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

"""Gets the LDR resistance given a sensor value"""
def getResistance(sensorValue):
    KNOWN_RESISTANCE = 2000
    if(sensorValue == 0):
        sensorValue = 1
        #prevents divide by 0
    resistance = ((4095.0 / sensorValue) - 1) * KNOWN_RESISTANCE
    return resistance

#The csv file structure:
#time, red_led,green_led,blue_led, piece1, piece2, piece3,  piece4, piece5, piece6,  piece7, piece8, piece9

# 0      1       2          3        4       5       6         7       8      9         10     11      12

file_contents = ""
distances = [5,10,15,20,25,30]
offset = 1.8#cm - the distance from the 0cm mark on the ruler to the surface of the ldr

#the tests preformed
file_titles = [["none", 1], 
["none", 5],
["none", 6],
["red", 1],
["red", 4],
["green", 1],
["green", 5],
["green", 6],
["blue", 6]]

#creates the csv header
file_contents += "intensity,"
for title in file_titles:
    colour = title[0]
    piece_number = title[1]
    file_contents += colour + str(piece_number) + ","
file_contents += "\n"

#fills in the data
for distance in distances:
    intensity = str(1/((distance + offset) ** 2))
    file_contents += intensity + ","
    for title in file_titles:
        colour = title[0]
        piece_number = title[1]

        file_name = colour + str(piece_number) + "_" + str(distance) + "cm.csv"

        raw_values = getColumn(3 + piece_number, getData(file_name))
        resistances = [getResistance(x) for x in raw_values]
        #I averaged the resistances as they will be rolling averages in the toy (to reduce noise)
        average_resistance = sum(resistances) / len(resistances)

        file_contents += str(average_resistance) + ","
    file_contents += "\n"

#writes the prepared content and closes the file
file = open("all_results.csv","w")
file.write(file_contents)
file.close()