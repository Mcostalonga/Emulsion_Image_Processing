# Image Processing with OpenCV Module

## Comments

This script is used to identify and determine the droplets diameters from pictures of emulsions take at microscope.

## Input data

The input data is a picture (or a folder with a number of pictures), like the one in Fig. (1).

<p><img src="https://i.ibb.co/tCx6Cqd/img2.png" height=50%, width=50%/></p>
<p>Figure 1. Example of input datat.</p>

## Output data

Currently, the script is capable of identifying droplets using the Hough Transform, like those showed in Fig. (2) and (3). The pinkish circles showed in those figures are droplets that were identified. Although not all droplets were recognized, the script shows some advantages when compared to manual measurements, such as the increase in the number of pictures analysed and minimal observer interference. At the begining, when you run the script, you can choose to save the pictures with the pinkish circles showing the droplets identified. I recommend you to save one picture to do the initial calibration, after that you decide to save all pictures or not.

<p><img src="https://i.ibb.co/yXLtLbC/img2-hordiv10-verdiv10.png" height=50%, width=50%/></p>
<p>Figure 2. Example 1 of processing obtained using the script.</p>

<p><img src="https://i.ibb.co/KXwpQWy/image.png" height=50%, width=50%/></p>
<p>Figure 3. Example 2 of processed image obtained using the script.</p>

For pictures like that in Fig. (3) you need more division to minimize the false positive droplets and diameter measurement error. This can be done by changing the value of "divisions" variable (it must be a integer). E.g. when you declare "divisions = 20" the script create a matrix of 20 x 20 to be analysed for each picture where each cell represents one part of the original picture. If you wish, you can divide the image with different width and height sizes. It can be done by changing the values of "hor_div" and "ver_div", respectively. For results showed in Fig. (2) it was used 10 divisions for both variables, on the other hand, in Fig. (3) it was necessary to use 40 divisions.

Furthermore, it can write a .TXT file with information about processing for every photo, Fig. (4). For every picture, even though you choose to save the processed pictures or not, you get the following information on that file:

- Elapsed time for processing
- Number of droplets identified
- Maximum and minimum diameter of droplets

To obtain diameters values in real world dimensions you must inform the "conversion_factor" variable. In this script the "conversion_factor" variable is informed in &mu;m/px. 

<p><img src="https://i.ibb.co/JHKXY8n/image.png" height=50%, width=50%/></p>
<p>Figure 4. Example of text file with processing information.</p>

Finally, after all images get processed a relative frequency histogram is plot using the barplot function. The cumulative frequency and d<sub>90</sub> are plot using the normal plot function. Fig. (5) shows this result. To create the histogram you can choose a fixed interval, in my case it makes future comparisson easier (you can determine the intervals in "interval" variable) or use a determined number of bins.

<p><img src="https://i.ibb.co/QPthVtY/image.png" height=50%, width=50%/></p>
<p>Figure 5. Example of relative frequency histogram with cumulative frequency and d<sub>90</sub>.</p>

The output data values of diameters, intervals, relative and cumulative frequency, and d<sub>90</sub> are stored in a .XLSX file like the on in Fig. (6).

<p><img src="https://i.ibb.co/fQSZNcY/image.png" height=50%, width=50%/></p>
<p>Figure 5. Example of .XLSX file with output data values</sub>.</p>

## Solution

To achieve all results commented above I used the OpenCV, NumPy, Math, Time, Matplotlib and Xlsxwriter modules.

## Future goals
- Use Machine Learning to identify and measure droplets
