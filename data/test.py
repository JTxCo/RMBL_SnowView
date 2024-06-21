import cv2
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import svm
from skimage.filters import roberts, sobel, scharr, prewitt
from sklearn import metrics
from scipy import ndimage as nd
import os



IMG_FILEPATH = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/Cut_Images"
image_filename = "DeerCreekTrail_2020_05_05_snow_cropped.tif"
image_path = os.path.join(IMG_FILEPATH, "Imagery/DeerCreekTrail", image_filename)


SNOW_MASK_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask/DeerCreekTrail"
snow_mask_filename = "DeerCreekTrail_2020_05_05_snowbinary.tif"
masked_path = os.path.join(SNOW_MASK_FILEPATH, snow_mask_filename)

# Looking at all the files in the DeerCreekTrail folder
# print out the num of files in the folder
# print out the num of files in the mask folder




# Count the number of ".tif" files in the Imagery/DeerCreekTrail directory
deer_creek_files = [file for file in os.listdir(os.path.join(IMG_FILEPATH, "Imagery/DeerCreekTrail")) if file.endswith(".tif")]
print(len(deer_creek_files))

# Count the number of ".tif" files in the SNOW_MASK_FILEPATH directory
snow_mask_files = [file for file in os.listdir(SNOW_MASK_FILEPATH) if file.endswith(".tif")]
print(len(snow_mask_files))

