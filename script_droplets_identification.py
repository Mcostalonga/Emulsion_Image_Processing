# Importing modules

import os

# Used to count time

import time

# Computational Vision module

import cv2 as cv

# Used for scientific computing

import numpy as np

# Used for round up and check if a value is close to other

from math import isclose
import math

# Used for plot graphs

import matplotlib.pyplot as plt

# Used for format graphs

from matplotlib.ticker import (MultipleLocator)

# Used for write a .xlsx file

import xlsxwriter

# Inform the number of divisions

divisions = 40

# Inform name for .txt file with droplets diameter

path_f2 = 'OA 50% T80 1,0% 6000 rpm 3 min (3)'

# Starting

savefile = input('Would you like to save the processed images? Type "y" for "yes", "n" for "no" \n')

print('Start processing...')

# Start counting total time for processing

start_total = time.time()

# Creating list for saving droplets diameter_data

diameter_data = []

# Path for input data files

path = 'data/'

# Path for output data files

path_output = 'results/'

path_f3 = path_output + path_f2.replace(' ', '_') + '_info.txt'
path_f4 = path_output + path_f2.replace(' ', '_')

path_f2 = path_output + path_f2.replace(' ', '_') + '.txt'

# Reading the input data files

entries = os.listdir(path)

# For every data file, do:

for entry in entries:

    # Starting time count for process one picture

    start = time.time()

    # Default path to input data and output folder

    file_d = path + entry

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

    # Image Smoothing - Gaussian Blur

    gray = cv.GaussianBlur(gray,(5,5),cv.BORDER_ISOLATED)

    # Creating a black background plane with the height and width of original image

    background = np.zeros([height, width], np.uint8)
    image_complete = background.copy()

    # Defining the size of the mask

    # Inform the number of divisions (must be greater than 4)

    hor_div = divisions
    ver_div = divisions

    # Conversion factor

    conversion_factor = 200/277

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

    # Creating an empty list

    diameter = []
    x1_pos = []
    y1_pos = []

    # Identifying circles with Hough Circle Transform for every part of image

    j = 0
    contx = 0
    conty = 0

    for i in range(len(hor_pos)):
        # color specified the color of border line of rectangle to be draw
        # if thickness = -1 px will fill the rectangle shape by the specified color
        mask = cv.rectangle(background,(hor_pos[i], ver_pos[i]), (size[1] + hor_pos[i], size[0] + ver_pos[i]),
                            color=(255,255,255), thickness=-1)

        proc_image = cv.bitwise_and(gray, mask)

        circles = cv.HoughCircles(proc_image, cv.HOUGH_GRADIENT, 1, height / 8,
                                  param1=50, param2=30,
                                  minRadius=10, maxRadius=75)

        # Saving circles detected in lists

        if circles is not None:

            circles = np.uint16(np.around(circles))

            for i in circles[0, :]:

                for item in x1_pos:
                    if isclose(i[0], item, rel_tol=0.005, abs_tol=0) == True:
                        contx += 1

                for item in y1_pos:
                    if isclose(i[1], item, rel_tol=0.005, abs_tol=0) == True:
                        conty += 1

                if (contx == 0 and conty == 0) == True:
                    diameter.append(i[2] * 2)
                    x1_pos.append(i[0])
                    y1_pos.append(i[1])
                    contx = 0
                    conty = 0
                contx = 0
                conty = 0

        background = np.zeros([height, width], np.uint8)
        i += 1

    # Drawing circles if any number of circles was identified

    for i in range(len(x1_pos)):
        cv.circle(or_image, (int(x1_pos[i]),int(y1_pos[i])), 1, (0, 100, 100), 3)
        # circle outline
        cv.circle(or_image, (int(x1_pos[i]),int(y1_pos[i])), int((diameter[i]/2)), (255, 0, 255), 3)
        i += 1

    diameter = np.array(diameter) * conversion_factor

    # Writing the test name

    path_f = 'results/' + test_name + '_hordiv' + str(hor_div) + '_verdiv' + str(ver_div) + '.png'

    # Saving the image

    if (savefile == 'y') == True:
        cv.imwrite(path_f, or_image)

    # Stop time counting

    end = time.time()

    # Saving values of diameter

    diameter_data.append(diameter)

    # Printing info about processing

    print('\nPROCESSING INFORMARTION:', entry)
    print('\nElapsed time:', round(end - start, 2), 's')
    print('\nNumber of droplets identified:', len(x1_pos), 'droplets')
    print('\nMaximum diameter:', round(max(diameter),2), '\u03BCm')
    if min(diameter) == 0:
        diameter = set(diameter)
        print('\nMinimum diameter:', round(sorted(diameter)[1],2), '\u03BCm')
    else:
        print('\nMinimum diameter:', round(min(diameter), 2), '\u03BCm')

    # Writing info in .txt file

    with open(path_f3, 'a') as f:
        print('\nPROCESSING INFORMARTION:', entry, file=f)
        print('\nElapsed time:', round(end - start, 2), 's', file=f)
        print('\nNumber of droplets identified:', len(x1_pos), 'droplets', file=f)
        print('\nMaximum diameter:', round(max(diameter), 2), 'x 10-3 mm', file=f)
        if min(diameter) == 0:
            diameter = set(diameter)
            print('\nMinimum diameter:', round(sorted(diameter)[1], 2), 'x 10-3 mm', file=f)
        else:
            print('\nMinimum diameter:', round(min(diameter), 2), 'x 10-3 mm', file=f)
        print('\n', file=f)

# Concatenate data to numpy array

diameter_data = np.concatenate(diameter_data)

# Creating an fixed interval to make future comparisons easier

interval = list(np.arange(5, 200, 5))

# Calculating the relative and cumulative frequency for data

hist, edges = np.histogram(diameter_data, interval)
rel_freq = (hist / float(hist.sum()))
rel_freq = rel_freq * 100
cumulative_freq = np.zeros(len(rel_freq))
cumulative_freq[0] = 0
for i in range(len(rel_freq) - 1):
    cumulative_freq[i + 1] = cumulative_freq[i] + rel_freq[i]

d90_a = 0
i1 = 0
while cumulative_freq[i1] <= 90:
    i1 += 1
i2 = len(cumulative_freq) - 1

if cumulative_freq[i1] != 90:
    d90_a = ((cumulative_freq[i1-1] - 90) / (cumulative_freq[i1] - cumulative_freq[i1 - 1])) * (
            interval[i1] - interval[i1 - 1]) + interval[i1 - 1]
else:
    d90_a = interval[i1]

yd90 = [0, 100]
d90 = [d90_a, d90_a]

info = ('Column info', '1st - Droplet Diameter', '2nd - Interval', '3rd - Relative Frequency',
        '4th - Cumulative Frequency', '5th - Y to plot d 90', '6th - Value of d90')

# Writing data into .xlsx file

workbook = xlsxwriter.Workbook(path_f4 + '.xlsx')
worksheet = workbook.add_worksheet()
Line = 0
Column = 0
ProcData = [diameter_data[diameter_data != 0], interval, rel_freq, cumulative_freq, yd90, d90, info]
while Column < len(ProcData):
    for item in ProcData[Column]:
        worksheet.write(Line, Column, item)
        Line += 1
    Column += 1
    Line = 0
workbook.close()

# Plotting results

fig, ax = plt.subplots(figsize=(8, 6))
barchart = plt.bar(interval[:-1], rel_freq, width=5.0, align='edge', ec='k', alpha=0.7,
                   color=(0, 0, 1), label='Droplet size distribution')

ax2 = plt.twinx()
linechart, = plt.plot(interval[:-1], cumulative_freq, color=(0, 0, 0), label='Cumulative Frequency')
d90chart, = plt.plot(d90, yd90, '--', color=(0.4, 0.4, 0.4), label='d\u2089\u2080')
color_d90chart = d90chart.get_color()

# Legend

legends = barchart, linechart
labels = [item.get_label() for item in legends]
ax.legend(legends, labels, loc='center right')

d90_a = d90[0]
d90_a = '{0:.3f}'.format(d90_a)
ax2.text(d90[0] + 0.5, 80, '\u2190d\u2089\u2080 = ' + d90_a
         + ' \u03BCm', color=color_d90chart, font='Times New Roman', fontsize=12)

# Title

ax.set_title('Droplet Size Distribution and d\u2089\u2080', font='Times New Roman', fontsize=14, fontweight='bold')

# Formatting axes, labels, lines, tickmarks, gridlines

# X axis

ax.set_xlabel('Droplet Diameter [\u03BCm]', font='Times New Roman', fontsize=12, fontweight='bold')
ax.set_xlim([0, 250])

# Y axis - left

ax.set_ylabel('Relative Frequency [%]', font='Times New Roman', fontsize=12, fontweight='bold')
ax.set_ylim(0, math.ceil(max(rel_freq)))

# Y axis - right

ax2.set_ylabel('Cumulative Frequency [%]', font='Times New Roman', fontsize=12, fontweight='bold')
ax2.set_ylim(0, 100)

# Tickmarks positioning

ax.xaxis.set_ticks_position('both')
ax.tick_params(which='major', width=1.50, length=5, direction='in')
ax.tick_params(which='minor', width=1.5, length=3, labelsize=10, direction='in')
ax2.tick_params(which='major', width=1.50, length=5, direction='in')
ax2.tick_params(which='minor', width=1.5, length=3, labelsize=10, direction='in')

# Adding minor tickmarks

# X axis

ax.xaxis.set_minor_locator(MultipleLocator(5))

# Y axis - left

ax.yaxis.set_minor_locator(MultipleLocator(0.5))

# Y axis - right

ax2.yaxis.set_minor_locator(MultipleLocator(5))

# Label font and size

plt.setp(ax.get_xticklabels(), font='Times New Roman', fontsize=12)
plt.setp(ax.get_yticklabels(), font='Times New Roman', fontsize=12)
plt.yticks(font='Times New Roman', fontsize=12)

# Setting the line width to axes

for axis in ['top', 'bottom', 'left', 'right']:
    ax.spines[axis].set_linewidth(1.5)

# Saving the figure at path informed

plt.savefig(path_f4 + '.png', format='png', dpi=200)

# Stop counting total time elapsed

end_total = time.time()

# Printing processing info

print('\nNumber of photos analysed:', len(entries))

print('\nTotal elapsed time:', round(end_total - start_total, 2), 's')
