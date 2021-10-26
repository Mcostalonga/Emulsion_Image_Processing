# Image Processing with OpenCV Module

## Comments

This script is used to identify and determine the droplets diameters from pictures of emulsions take at microscope.

## :warning: This script is under development :warning:

I'm developing this script to identify and determine the droplets sizes using the **OpenCV** module. But it is under development yet, so keep it in mind.

## Input

The input data is a picture (or a folder with a number of pictures in the future), like the one in Fig. (1).

<p><img src="https://i.ibb.co/tCx6Cqd/img2.png" height=50%, width=50%/></p>
<p>Figure 1. Example of input datat.</p>

## Output

Currently, the script is capable of identifying droplets using the Hough Circle Transform, like those showed in Fig. (1). The pinkish circles were the droplets identified. Although not all droplets were identified, the script shows some advantages when compared to manual measurements, such as the increase in the number of pictures analysed and minimal observer interference.

<p><img src="https://i.ibb.co/yXLtLbC/img2-hordiv10-verdiv10.png" height=50%, width=50%/></p>
<p>Figure 2. Example of processed image obtained using the script.</p>

Furthermore, it can write a .TXT file with the droplets diameters that were identify, Fig. (3). Both the image file and the text file can be check in the "results" folder.

<p><img src="https://i.ibb.co/QpJQNf6/img-10div-diameters.png" height=50%, width=50%/></p>
<p>Figure 3. Example of text file with droplets diameters information.</p>

The number of of droplets identified can be optmize by changing the values of "hor_div" and "ver_div" variables in the script, where the variables are the number of divisions in horizontal and vertical direction, respectively. For results showed in Fig. (2) it was used 10 divisions for both variables.

## Future features

When I'm done I hope the script could be capable of:

- Process a bunch of images

## Future goals
- Use Machine Learning to do it all alone
