### Trains a model to identify the colour of an inserted piece ###

import numpy as np
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

#The csv file structure:
#time, red_led,green_led,blue_led, piece1, piece2, piece3,  piece4, piece5, piece6,  piece7, piece8, piece9

# 0      1       2          3        4       5       6         7       8      9         10     11      12

#analyses the green pieces
data = getData("green_pieces_training_data.csv")

g_x = []
g_y = []
g_z = []
for i in range(0,len(data), 4):#4 lines form 1 data point
    output = ""
    #loops through all pieces(as a green was in every slot)
    for piece_number in range(9):
        #calculates the absolute amount of each colour reflected
        red_change = float(data[i+1][piece_number + 4]) - float(data[i][piece_number + 4])# +1,+2,+3 selects the correct row
        green_change = float(data[i+2][piece_number + 4]) - float(data[i][piece_number + 4])# + 4 converts piece number into column number
        blue_change = float(data[i+3][piece_number + 4]) - float(data[i][piece_number + 4])

        if(red_change < 0):
            red_change = 0

        if(green_change < 0):
            green_change = 0

        if(blue_change < 0):
            blue_change = 0
        
        #calculates the relative amount of each colour reflected
        total_change = red_change + green_change + blue_change
        if(total_change != 0):
            red_percent = red_change / total_change
            green_percent = green_change / total_change
            blue_percent = blue_change / total_change
        else:
            red_percent = 0
            green_percent = 0
            blue_percent = 0
        
        #the piece is green so adds it to the green data
        g_x.append(red_percent)
        g_y.append(green_percent)
        g_z.append(blue_percent)


#analyses the red and blue pieces
data = getData("red_and_blue_pieces_training_data.csv")
r_x = []
r_y = []
r_z = []

b_x = []
b_y = []
b_z = []
for i in range(0,len(data), 4):#4 lines form 1 data point
    output = ""
    #calculates values for slot 1 (red piece inserted), slot 4 (red piece inserted) and slot 6(blue piece inserted)
    for piece_number in [0,3,5]:
        #calculates the absolute amount of each colour reflected
        red_change = float(data[i+1][piece_number + 4]) - float(data[i][piece_number + 4])
        green_change = float(data[i+2][piece_number + 4]) - float(data[i][piece_number + 4])
        blue_change = float(data[i+3][piece_number + 4]) - float(data[i][piece_number + 4])

        if(red_change < 0):
            red_change = 0

        if(green_change < 0):
            green_change = 0

        if(blue_change < 0):
            blue_change = 0
        
        #calculates the relative amount of each colour reflected
        total_change = red_change + green_change + blue_change
        if(total_change != 0):
            red_percent = red_change / total_change
            green_percent = green_change / total_change
            blue_percent = blue_change / total_change
        else:
            red_percent = 0
            green_percent = 0
            blue_percent = 0
        
        
        if(piece_number == 5):
            #the piece is blue so adds it to the blue data
            b_x.append(red_percent)
            b_y.append(green_percent)
            b_z.append(blue_percent)
        else:
            #the piece is red so adds it to the red data
            r_x.append(red_percent)
            r_y.append(green_percent)
            r_z.append(blue_percent)

#calculates the median point in each cluster
red_piece_expected = [np.median(r_x), np.median(r_y), np.median(r_z)]
green_piece_expected = [np.median(g_x), np.median(g_y), np.median(g_z)]
blue_piece_expected = [np.median(b_x), np.median(b_y), np.median(b_z)]

#prints the expected reflected values for each piece
print("red_piece_expected = " + str(red_piece_expected))
print("green_piece_expected = " + str(green_piece_expected))
print("blue_piece_expected = " + str(blue_piece_expected))

#creates the diagram
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_xlabel('percent red')
ax.set_ylabel('percent green')
ax.set_zlabel('percent blue')

#plots all of the data points
ax.scatter(r_x, r_y, r_z, marker='o', c="r")
ax.scatter(g_x, g_y, g_z, marker='^', c="g")
ax.scatter(b_x, b_y, b_z, marker='*', c="b")

#displays the diagram
plt.show()