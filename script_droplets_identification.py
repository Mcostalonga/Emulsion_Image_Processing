# Importing modules

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Default path to input data and output folder

file_d = 'data/img4.png'

# Getting the test name

name = file_d.split('/')
name_split = name[len(name) - 1].split('.')
test_name = name_split[0]

path_f = 'results/' + test_name + '_proc.png'

# Opening the image

or_image = cv.imread(file_d)

# Measuring the height and width of original image

height, width = or_image.shape[:2]

# Converting the original BGR image to gray scale

gray = cv.cvtColor(or_image, cv.COLOR_BGR2GRAY)

# Creating a black background plane with the height and width of original image

background = np.zeros([height, width], np.uint8)
image_complete = background.copy()

# Defining the size of the mask

size = [round(height/3), round(width/3)]

# Calculanting the size of the step

step_height = (size[0]/height)/2
step_width = (size[1]/width)/2

# Defining the position to apply the mask
pos_hor = [0, round(step_width*1*width), round(step_width*2*width), round(step_width*3*width), round(step_width*4*width), round(step_width*5*width),
           0, round(step_width*1*width), round(step_width*2*width), round(step_width*3*width), round(step_width*4*width), round(step_width*5*width),
           0, round(step_width*1*width), round(step_width*2*width), round(step_width*3*width), round(step_width*4*width), round(step_width*5*width),
           0, round(step_width*1*width), round(step_width*2*width), round(step_width*3*width), round(step_width*4*width), round(step_width*5*width),
           0, round(step_width*1*width), round(step_width*2*width), round(step_width*3*width), round(step_width*4*width), round(step_width*5*width),]

pos_ver = [0, 0, 0, 0, 0, 0,
           round(step_height*1*height), round(step_height*1*height), round(step_height*1*height),  round(step_height*1*height), round(step_height*1*height), round(step_height*1*height),
           round(step_height*2*height), round(step_height*2*height), round(step_height*2*height),  round(step_height*2*height), round(step_height*2*height), round(step_height*2*height),
           round(step_height*3*height), round(step_height*3*height), round(step_height*3*height),  round(step_height*3*height), round(step_height*3*height), round(step_height*3*height),
           round(step_height*4*height), round(step_height*4*height), round(step_height*4*height),  round(step_height*4*height), round(step_height*4*height), round(step_height*4*height),
           round(step_height*5*height), round(step_height*5*height), round(step_height*5*height),  round(step_height*5*height), round(step_height*5*height), round(step_height*5*height),]

# Identifying circles with Hough Circle Transform for every part of image

i = 0
for i in range(len(pos_hor)):
    mask = cv.rectangle(background, (pos_hor[i], pos_ver[i]), (size[1] + pos_hor[i], size[0] + pos_ver[i]), 255, -1)
    proc_image = cv.bitwise_and(gray, mask)
    circles = cv.HoughCircles(proc_image, cv.HOUGH_GRADIENT, 1, height / 8,
                              param1=100, param2=30,
                              minRadius=1, maxRadius=200)

    # Drawing circles if any number of circles was identified

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # circle center
            cv.circle(or_image, center, 1, (0, 100, 100), 3)
            # circle outline
            radius = i[2]
            cv.circle(or_image, center, radius, (255, 0, 255), 3)

    background = np.zeros([height, width], np.uint8)
    i += 1
    # Show inside the "for"
    #cv.imshow('', or_image)
    #cv.waitKey()

# Showing the image with the droplets identified

#cv.imshow('', or_image)
#cv.waitKey()

# Saving the image

#cv.imwrite(path_f, or_image)
