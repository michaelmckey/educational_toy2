### Tests the model created by the training program ###

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

VERBOSE_OUTPUT = False #if set to true highlights where anomalies in results are

#the model calculated by the training program
red_piece_expected = [0.5060, 0.2177, 0.2820]
green_piece_expected = [0.1559, 0.4286, 0.3988]
blue_piece_expected = [0.1933, 0.0102, 0.7946]

#The csv file structure:
#time, red_led,green_led,blue_led, piece1, piece2, piece3,  piece4, piece5, piece6,  piece7, piece8, piece9

# 0      1       2          3        4       5       6         7       8      9         10     11      12

#initialises the success count
red_error_count = 0
red_success_count = 0

green_error_count = 0
green_success_count = 0

blue_error_count = 0
blue_success_count = 0

#analyses the predictions for the green pieces
data = getData("green_pieces_testing_data.csv")

for i in range(0,len(data), 4):#4 lines form 1 data point
    output = ""
    #loops through all pieces(as a green was in every slot)
    for piece_number in range(9):
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
        
        #finds the cluster centre that the data point is closest to (in the colour space)
        red_piece_diff = (red_percent - red_piece_expected[0]) ** 2 + (green_percent - red_piece_expected[1]) ** 2 + (blue_percent - red_piece_expected[2]) ** 2
        green_piece_diff = (red_percent - green_piece_expected[0]) ** 2 + (green_percent - green_piece_expected[1]) ** 2 + (blue_percent - green_piece_expected[2]) ** 2
        blue_piece_diff = (red_percent - blue_piece_expected[0]) ** 2 + (green_percent - blue_piece_expected[1]) ** 2 + (blue_percent - blue_piece_expected[2]) ** 2
        min_diff = min(red_piece_diff, green_piece_diff, blue_piece_diff)

        if(red_piece_diff == min_diff):
            #green piece was predicted as being red (error)
            output += "red, "
            green_error_count += 1
        elif(green_piece_diff == min_diff):
            #green piece was predicted as being green (success)
            output += "green, "
            green_success_count += 1
        elif(blue_piece_diff == min_diff):
            #green piece was predicted as being blue (error)
            output += "blue, "
            green_error_count += 1

    #prints the prediction for every data point in order
    if(VERBOSE_OUTPUT):
        print(output)



#analyses the predictions for the red and blue pieces
data = getData("red_and_blue_pieces_testing_data.csv")

for i in range(0,len(data), 4):#4 lines form 1 data point
    output = ""
    #loops through all pieces(as a green was in every slot)
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

        #in the colour space finds the closest piece colour
        red_piece_diff = (red_percent - red_piece_expected[0]) ** 2 + (green_percent - red_piece_expected[1]) ** 2 + (blue_percent - red_piece_expected[2]) ** 2
        green_piece_diff = (red_percent - green_piece_expected[0]) ** 2 + (green_percent - green_piece_expected[1]) ** 2 + (blue_percent - green_piece_expected[2]) ** 2
        blue_piece_diff = (red_percent - blue_piece_expected[0]) ** 2 + (green_percent - blue_piece_expected[1]) ** 2 + (blue_percent - blue_piece_expected[2]) ** 2
        min_diff = min(red_piece_diff, green_piece_diff, blue_piece_diff)

        if(red_piece_diff == min_diff):
            output += "red, "
            if(piece_number == 0 or piece_number == 3):
                #red piece was predicted as being red (success)
                red_success_count += 1
            else:
                #blue piece was predicted as being red (error)
                blue_error_count += 1
            
        elif(green_piece_diff == min_diff):
            output += "green, "
            if(piece_number == 0 or piece_number == 3):
                #red piece was predicted as being green (error)
                red_error_count += 1
            else:
                #blue piece was predicted as being green (error)
                blue_error_count += 1

        elif(blue_piece_diff == min_diff):
            output += "blue, "
            if(piece_number == 0 or piece_number == 3):
                #red piece was predicted as being blue (error)
                red_error_count += 1
            else:
                #blue piece was predicted as being blue (success)
                blue_success_count += 1
    
    #prints the prediction for every data point in order
    if(VERBOSE_OUTPUT):
        print(output)

"""Converts a decimal to a percent(and rounds it)"""
def percent(rate):
    return str(round(rate * 100.0, 1)) + "%"

#prints the success rate of the model on the testing data
red_piece_success_rate = red_success_count / (red_success_count + red_error_count)
green_piece_success_rate = green_success_count / (green_success_count + green_error_count)
blue_piece_success_rate = blue_success_count / (blue_success_count + blue_error_count)

#prints results
print("%s effective at identifying red pieces" % percent(red_piece_success_rate))
print("%s effective at identifying green pieces" % percent(green_piece_success_rate))
print("%s effective at identifying blue pieces" % percent(blue_piece_success_rate))