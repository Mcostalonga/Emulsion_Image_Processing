# Importing modules

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Default path to input data and output folder

file_d = 'data/img2.png'

# Getting the test name

name = file_d.split('/')
name_split = name[len(name) - 1].split('.')
test_name = name_split[0]

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

# Inform the number of divisions (must be greater than 4)
hor_div = 20
ver_div = 20

size = [round(height / (ver_div - 1)), round(width / (hor_div - 1))]

# Calculanting the size of the step

step_height = height/ver_div - (1/(ver_div**2)) * height/ver_div
step_width = width/hor_div - (1/(hor_div**2)) * width/hor_div

step_height = int(step_height)
step_width = int(step_width)

# Declaring variables

hor_pos = np.zeros((hor_div * ver_div))
ver_pos = np.zeros((ver_div * hor_div))

# Defining the position to apply the mask

j = 0
for i in range(len(hor_pos)):
    hor_pos[i] = hor_pos[i] + step_width * j
    j += 1
    if j == hor_div:
        j = 0

k = 0
j = 0
for i in range(len(ver_pos)):
    ver_pos[i] = ver_pos[i] + step_height * j
    k += 1
    if k == hor_div:
        j += 1
        k = 0

hor_pos = hor_pos.astype(int)
ver_pos = ver_pos.astype(int)

# Identifying circles with Hough Circle Transform for every part of image

i = 0
for i in range(len(hor_pos)):
    # color specified the color of border line of rectangle to be draw
    # if thickness = -1 px will fill the rectangle shape by the specified color
    mask = cv.rectangle(background,(hor_pos[i], ver_pos[i]), (size[1] + hor_pos[i], size[0] + ver_pos[i]),
                        color=(255,255,255), thickness=-1)

    proc_image = cv.bitwise_and(gray, mask)

    circles = cv.HoughCircles(proc_image, cv.HOUGH_GRADIENT, 1, height / 8,
                              param1=100, param2=30,
                              minRadius=1, maxRadius=200)

    # Drawing circles if any number of circles was identified

    if circles is not None:

        circles = np.uint16(np.around(circles))

        for i in circles[0, :]:
            # circle center
            center = (i[0], i[1])

            # circle outline
            cv.circle(or_image, center, 1, (0, 100, 100), 3)
            radius = i[2]
            cv.circle(or_image, center, radius, (255, 0, 0), 3)

    background = np.zeros([height, width], np.uint8)
    i += 1
    # Show inside the "for"
    #cv.imshow('', proc_image)
    #cv.waitKey()

# Showing the image with the droplets identified

#cv.imshow('', or_image)
#cv.waitKey()

# Writing the test name

path_f = 'results/' + test_name + '_hordiv' + str(hor_div) + '_verdiv' + str(ver_div) + '.png'

# Saving the image

cv.imwrite(path_f, or_image)
