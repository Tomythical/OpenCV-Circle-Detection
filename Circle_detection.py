import cv2
import numpy as np
from scipy import stats
import math
import pandas as pd
 
"""This function takes an image and breaks down its properties"""
def img_moment(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Converts coloured image to grayscale

    _,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) #Binarizes the image using Otsu's method to automatically choose a threshold
    thresh = cv2.bitwise_not(thresh) #Inverts the image colour

    element = cv2.getStructuringElement(shape=cv2.MORPH_ELLIPSE, ksize=(5, 5)) #Used for the morphological transform

    morph_img = thresh.copy()   
    cv2.morphologyEx(src=thresh, op=cv2.MORPH_CLOSE, kernel=element, dst=morph_img)  #A morphological transform that performs a closing operation that reduces noise in the image  

    contours,_ = cv2.findContours(morph_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)    #Find the contours of the circle which is normally the whole boundary

    areas = [cv2.contourArea(c) for c in contours]
    sorted_areas = np.sort(areas)
    cnt=contours[areas.index(sorted_areas[-1])] # Finds the biggest contour if there are multiple

    M = cv2.moments(cnt)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00']) #Calculates the centre of the circle from the largest contour using image moments as (cx,cy)

    threshold_level = 1 #Thresholds above the black background pixels
    whitepix = np.column_stack(np.where(thresh > threshold_level))  #Stores the pixel coordinates of the white circle as a 2d array

    return (cx,cy,whitepix,cnt) #Returns the centre, the pixel coordinates and the largest contour

    # for i in range(len(whitepix)):
    #     img[whitepix[i][0], whitepix[i][1]] = [23,23,140]

"""This function applies the metrics to the circle"""
def img_properties(img):
    xpos = []
    ypos = []
    radii = []
    cx = img_moment(img)[0]
    cy = img_moment(img)[1]
    whitepix = img_moment(img)[2]
    for i in range(len(whitepix)):
        xpos.append(whitepix[i][0])
        ypos.append(whitepix[i][1])   #Separating x and y coordinates of the circle into xpos and ypos

    for i in range(len(whitepix)):
        distance_from_radius = math.hypot((cy-xpos[i]),(cx-ypos[i]))  # Calculates distance from centre of circle to each pixel coordinate
        rounded = round(distance_from_radius,5)
        radii.append(rounded) #Stores distances in list 'radii'

    mode_radius = stats.mode(radii)[0][0] # The mode of the radii is calculated
    
    # mean_radius = np.mean(radii) #This will calculate the mean of the distances

    mode_difference = [(res-mode_radius)**2 for res in radii]
    res_sum = sum(mode_difference)
    std = math.sqrt(res_sum*(1/(len(radii)-1))) #Calculates standard deviation of modal residuals

    """Calculates pixel difference"""
    height,width,cols = img.shape # Gets shape of image
    blank_image = np.zeros((height,width,3), np.uint8) # Creates a new blank image of same size
    cv2.circle(blank_image,(cx,cy),int(mode_radius),(0,255,0),1)  #Plots mode circle onto blank image in green with line thickness 1
    greenpix = np.column_stack(np.where(blank_image > 1)) #Stores the pixel coordinates of the mode circle in 2d array 'greenpix'
    greenpix = np.delete(greenpix,2,axis = 1) #Reformats array for easier comparison to 'whitepix'
   
    nrows, ncols = greenpix.shape
    dtype={'names':['f{}'.format(i) for i in range(ncols)],
        'formats':ncols * [greenpix.dtype]}

    C = np.intersect1d(greenpix.view(dtype), whitepix.view(dtype)) #Finds all the pixel coordinates of 'whitepix' and 'greenpix' that intersect

    # This bit is optional if you're okay with "C" being a structured array...
    C = C.view(greenpix.dtype).reshape(-1, ncols)
    pixel_diff = 100-((len(C)/len(greenpix))*100) #Calculates the pixel difference as a percentage

    return (mode_radius,std,pixel_diff) 

"""Calculates the eccentricity of the circle"""
def get_ecc(img):
    ellipse = cv2.fitEllipse(img_moment(img)[3]) #OpenCV fits an ellipse to the image
    cv2.ellipse(img,ellipse,(255,0,0),1) #Draws the ellipse in blue

    smaller = min(ellipse[1])  #Gets the semi-minor axis
    bigger = max(ellipse[1])   #Gets the semi-major axis
    ecc = math.sqrt(1-((smaller**2)/(bigger**2))) #Calculates eccentricity
    return ecc

"""Runs through each circle, applies metrics, and outputs as a csv table"""
if __name__ == '__main__':
    variables  = [1,11,21,31,41,51,61,71,81,91,101] # The value for each MATLAB parameter we tested. E.g. This is for Window Length
    for var in variables: #Creates a new table for each MATLAB parameter value
        images = []
        for i in range(3,21,3): #The samples names ranged from 3-18
            images.append(cv2.imread(f"/Users/ThomasMatheickal/OneDrive - Durham University/20g Circles/E0007-07_C2mm_AP_20g WL/E0007-07_C2mm_AP_20g {i} WL={var}.png")) #Stores each individual circle in a list
        outs = pd.DataFrame(np.zeros((len(images),4))) #Uses pandas to create a table
        outs.columns = ["Mode Radius", "Standard Deviation", "Pixel Difference Percentage","Eccentricity" ] #Column names
        rownames = []
        for i in range(3,21,3):
            rownames.append(f"E0007-07_C2mm_AP_20g {i} WL={var}.png") #Row Names are each circle with the same MATLAB parameter value
        outs.index = rownames
        for i in range(len(images)):
            outs.iloc[i] = np.array([img_properties(images[i])[0],img_properties(images[i])[1],img_properties(images[i])[2],get_ecc(images[i])]) #Inserts metric values
        # outs.to_csv(f"/Users/ThomasMatheickal/OneDrive - Durham University/CSVs/20g Circles/WL/WL={var}.csv") #Stores tables as .csv files
        print(outs)
        images = [] #Resets image list
        


