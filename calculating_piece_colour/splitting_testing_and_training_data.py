### Splits the original data into training and testing data ###

import random
random.seed(123)#seeding the pseudo-random number generator to improve repeatability

PERCENT_TRAINING = 0.75 # the percent of the original that is used for training the model (the rest is used for testing)

"""Splits the data into training data and testing data. Then saves each to a new file"""
def split_data(file_name):
    #gets the original data
    file = open(file_name + ".csv","r")
    data = []
    for line in file:
        line = line.replace("\n", "")
        data.append(line)
    file.close()

    #eachline only contains 1 reading so it takes 4 lines to get 1 data point(containing a none, red, green and blue reading)
    data_points = []
    for i in range(0,len(data), 4):
        data_points.append([data[i], data[i+1], data[i+2], data[i+3]])
    
    #shuffles the data points as over time the ambient light intensity decreased(as using natural light)
    random.shuffle(data_points)
    index_of_last_training = int(PERCENT_TRAINING * len(data_points)) - 1 #rounds and makes it an int

    #adds each data point to the correct group
    training_data = ""
    testing_data = ""
    for i, point in enumerate(data_points):
        if(i <= index_of_last_training):
            #training data
            for x in range(4):
                training_data += point[x] + "\n"
        else:
            #testing data
            for x in range(4):
                testing_data += point[x] + "\n"

    #removes the extra line added to the end of the data which could create errors in other programs
    training_data = training_data.removesuffix("\n")
    testing_data = testing_data.removesuffix("\n")

    #saves the training data
    file = open(file_name + "_training_data.csv","w")
    file.write(training_data)
    file.close()

    #saves the testing data
    file = open(file_name + "_testing_data.csv","w")
    file.write(testing_data)
    file.close()

#passes the data files to be split
split_data("green_pieces")
split_data("red_and_blue_pieces")