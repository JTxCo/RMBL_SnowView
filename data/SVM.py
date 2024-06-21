# SVM for image segmentation
import cv2 
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import svm
from skimage.filters import roberts, sobel, scharr, prewitt
from sklearn import metrics
from scipy import ndimage as nd
import os

IMG_FILEPATH = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/Cut_Images/Imagery/DeerCreekTrail"
image_filename = "DeerCreekTrail_2020_05_05_snow_cropped.tif"
image_path = os.path.join(IMG_FILEPATH, image_filename)



SNOW_MASK_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask/DeerCreekTrail"
snow_mask_filename = "DeerCreekTrail_2020_05_05_snowbinary.tif"
masked_path = os.path.join(SNOW_MASK_FILEPATH, snow_mask_filename)


def add_image_to_df(image_file, df):
    img = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
    if img is not None:
        # Read successful
        img = np.nan_to_num(img, nan=0)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img2 = img.reshape(-1)
        column_name = f'Image_{image_file}'
        if column_name in df.columns:
            df[column_name + '_new'] = img2
        else:
            df[column_name] = img2
        print(f"Image {image_file} added successfully.")
    else:
        # Read failed
        print(f"Error: Image {image_file} could not be read.")
    return df, img



def add_mask_to_df(mask_file, df):
    mask = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)
    if mask is not None:
        # Read successful
        if len(mask.shape) > 2:
            mask = cv2.cvtColor(mask, cv2.COLOR_RGB2GRAY)
        mask1 = mask.reshape(-1)
        column_name = f'Mask_{mask_file}'
        if column_name in df.columns:
            df[column_name + '_new'] = mask1
        else:
            df[column_name] = mask1
        print(f"Mask {mask_file} added successfully.")
    else:
        # Read failed
        print(f"Error: Mask {mask_file} could not be read.")
    return df, mask

    
# Generate Gabor Features

def generateGaborFeatures(img2, df):
    img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    num = 1 
    kernels = []
    for theta in range(2):
        theta = theta / 4. * np.pi
        for sigma in (1, 3):
            for lamda in np.arange(0, np.pi, np.pi / 4):
                for gamma in (0.05, 0.5): 
                    gabor_label = 'Gabor' + str(num)
                    ksize = 9
                    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lamda, gamma, 0, ktype=cv2.CV_32F)
                    kernels.append(kernel)
                    fimg = cv2.filter2D(img_gray, cv2.CV_8UC3, kernel)
                    filtered_img = fimg.reshape(-1)
                    df[gabor_label] = filtered_img
                    # print(gabor_label, ': theta=', theta, ': sigma=', sigma, ': lamda=', lamda, ': gamma=', gamma)
                    num += 1
    return df          
                
def extractEdgefeatures(img, df):
    
    img_uint8 = cv2.convertScaleAbs(img)
    if len(img_uint8.shape) > 2:
        img_gray = cv2.cvtColor(img_uint8, cv2.COLOR_BGR2GRAY)
        print("Image converted to grayscale successfully!")
    else:
        print("already binary")
        img_gray = img_uint8
        
    # Canny Edge
    edges = cv2.Canny(img_uint8, 100, 200)
    # Ensure edges1 is a one-dimensional array
    edges1 = np.ravel(edges)


    print("Shape of the DataFrame before assignment:", df.shape)

    # Try inserting edges1 into the DataFrame
    try:
        df['Canny Edge'] = edges1
        print("Canny Edge data added to the DataFrame successfully!")
    except Exception as e:
        print("Error: Unable to assign Canny Edge data to the DataFrame.")
        print(e)

    # Check the shape of the DataFrame after assignment
    print("Shape of the DataFrame after assignment:", df.shape)
    
    # Edge Roberts
    if len(img_uint8.shape) == 3:  # Check if img_uint8 is 3D, typically due to color channels
        edge_roberts = roberts(img_gray).astype(np.uint8)  # Apply Roberts edge detection
    else:
        edge_roberts = roberts(img_uint8.squeeze()).astype(np.uint8)
 
    edge_roberts1 = edge_roberts.ravel()

    if edge_roberts1.size == df.shape[0]:
        df['Roberts'] = edge_roberts1
        print("Roberts edge data added to the DataFrame successfully!")
    else:
        print("Error: Dimension mismatch between Roberts edge data and DataFrame length.")




    # Sobel
    if len(img_uint8.shape) == 3:  # Check if img_uint8 is 3D, typically due to color channels
        edge_sobel = sobel(img_gray).astype(np.uint8)
    else:
        edge_sobel = sobel(img_uint8).astype(np.uint8)

    edge_sobel1 = edge_sobel.ravel()
    if edge_sobel1.size == df.shape[0]:
        df['Sobel'] = edge_sobel1
        print("Sobel edge data added to the DataFrame successfully!")
    else:
        print("Error: Dimension mismatch between Sobel edge data and DataFrame length.")




    # Scharr
    if len(img_uint8.shape) == 3:
        edge_scharr = scharr(img_gray).astype(np.uint8)
    else:
        edge_scharr = scharr(img_uint8).astype(np.uint8)

    edge_scharr1 = edge_scharr.ravel()
    if edge_scharr1.size == df.shape[0]:
        df['Scharr'] = edge_scharr1
        print("Scharr edge data added to the DataFrame successfully!")
    else:
        print("Error: Dimension mismatch between Scharr edge data and DataFrame length.")

    # PreWitt
    if len(img_uint8.shape) == 3:
        
        edge_prewitt = prewitt(img_gray).astype(np.uint8)
    else:
        edge_prewitt = prewitt(img_uint8).astype(np.uint8)

    edge_prewitt1 = edge_prewitt.ravel()
    if edge_prewitt1.size == df.shape[0]:
        df['PreWitt'] = edge_prewitt1
        print("PreWitt edge data added to the DataFrame successfully!")
    else:
        print("Error: Dimension mismatch between PreWitt edge data and DataFrame length.")
    

    # Gaussian filter (sigma=3)
    
    guassian_img = nd.gaussian_filter(img_gray, sigma=3)
    guassian_img1 = guassian_img.reshape(-1)
    df['Gaussian s3'] = guassian_img1
 
        
    # Gaussian filter (sigma=7)
    guassian_img2 = nd.gaussian_filter(img_gray, sigma=7)
    guassian_img3 = guassian_img2.reshape(-1)
    df['Gaussian s7'] = guassian_img3


    # Median filter (size=3)
    median_img = nd.median_filter(img_gray, size=3)
    median_img1 = median_img.reshape(-1)
    df['Median s3'] = median_img1


    print("Edge features extracted successfully!")
    return df




def extract_features(img, df):
    print("Extracting edge features")
    df = extractEdgefeatures(img, df)
    print("Extracting Gabor features")
    df = generateGaborFeatures(img, df)
    print("Features extracted successfully")
    return df

def train_model(df):
    print("Spliting the data into training and test sets")
    print(df.head())
    num_bins = 3
    y_train_bins = pd.cut(df['Mask'], bins=num_bins, labels=False)

    # Drop the 'Mask' column from the features
    X = df.drop(labels=['Mask'], axis=1)

    # Split the data into training and test sets with the updated target variable
    print("Splitting the data into training and test sets")
    X_train, X_test, y_train_bins, y_test = train_test_split(X, y_train_bins, test_size=0.3, random_state=42)

    # Training the SVM model with the updated target variable
    print("Training the SVM model")
    model = svm.SVC(kernel='linear', C=1, gamma=1)
    model.fit(X_train, y_train_bins)

    # Predicting the test set result
    print("Predicting the test set result")
    y_pred = model.predict(X_test)

    # Evaluating the model
    accuracy = metrics.accuracy_score(y_test, y_pred)
    print("Accuracy: ", accuracy)

    # Displaying the classification report
    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred))

    # print the confusion matrix
    print("Confusion Matrix:")
    cm = metrics.confusion_matrix(y_test, y_pred)
    print(cm)



def extract_common_identifier(file_name):
    return file_name.split('_')[0] 

def main():
    df = pd.DataFrame()
    img_file_names = [img_file for img_file in os.listdir(IMG_FILEPATH) if img_file.endswith('.tif')]
    # Process each image file and its matched mask file based on the common identifier
    for img_file in img_file_names:
        img_path = os.path.join(IMG_FILEPATH, img_file)
        # Find the matching mask file based on the common identifier
        print("img_file: ", img_file)
        mask_file = img_file.replace('_cropped.tif', 'binary.tif')
        mask_path = os.path.join(SNOW_MASK_FILEPATH, mask_file)
        if os.path.exists(mask_path):   
        
            # print(f"Processing image {img_path}")
            # print("Mask file: ", mask_path)
            df, img = add_image_to_df(img_path, df)
            df = add_mask_to_df(mask_file, df)
            if img is not None:
                # Read successful
                print(f"Image {img_path} read successfully.")
                df = extract_features(img, df)

            else:
                # Read failed
                print(f"Error: Image {img_path} could not be read.")
        else:
            print(f"No matching mask found for image file: {img_path}")
    
    # Train the model after processing all image and mask files
    train_model(df)

    


if __name__ == "__main__":
    main()