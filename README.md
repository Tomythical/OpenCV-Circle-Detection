# OpenCV Circle Detection

## Table of contents
* [Project Aim](#project-aim)
* [My Role](#my-role)
* [Technologies](#technologies)


## Project Aim
This project was undertaken as part of my Team Project Module in Durham University where my team and I provided solutions for the pressure-sensing solutions company 
Peratech. Our objective was to find a way to quantify the performance of the smoothing algorithm Peratech had developed from the test data they provided. 
This consisted of detecting and measuring the differences between the output of the tracking algorithm and the input test pattern.

## My Role
I was in charge of developing a method to quantify the inaccuracy of images of circles given to me. The images came in the form of .pngs which I then pre-processed using Otsu's binarization to remove anti-aliasing from the image and then applied morphological transformations to further reduce any unwanted noise.
This is an example of a circle I was given to anlayse:

<p align="center">
<img width="200" height="200" src=https://github.com/Tomythical/OpenCV-Circle-Detection/blob/main/Images/E0007-07_C2mm_AP_50g%2018%20Thresh%3D750.png>
</p>	

Firstly, in order to measure how good the algorithm was at returning the input circle, the desired circle needed to be formed so a comparison to the algorithm’s output could be made. This was achieved this by approximating the centre of the desired circle from the output image and then by calculating a suitable radius to plot the perfect circle. To approximate the perfect cirlce, the image was initially segmented so that its properties could be more easily analysed. This entailed finding the contours of the circle using OpenCV and then calculating its image moments.The radius of the desired circle was calculated by measuring the distance from the centre of the desired circle to each pixel of the output circle. The metrics to quantify the "goodness" of a circle were: Standard Deviation of Radius, Pixel Difference Percentage, and Eccentricity

<p align="center">
<img width="200" height="200" src=https://github.com/Tomythical/OpenCV-Circle-Detection/blob/main/Images/Std%2520circle.png>
<img width="210" height="200" src=https://github.com/Tomythical/OpenCV-Circle-Detection/blob/main/Images/Eccentricity%2520Circle.png>
<img width="210" height="200" src=https://github.com/Tomythical/OpenCV-Circle-Detection/blob/main/Images/Pixel%2520Difference.png>	
</p>
<p align = "center">
Examples of perfect circles fitted
</p>


## Technologies
Project is created with:
* OpenCV
* Python version: 3.89

