import os
import rasterio
import rasterio.mask as mask
import numpy as np
import matplotlib.pyplot as plt


from image_processing import resample, create_mask


SOURCE_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data"
IMAGERY_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Imagery"
SNOW_MASK_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask"
DEST_FILEPATH = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/Cut_Images"

locations = [
    'DeerCreekTrail', 'EastRiverTrail', 'Elkton', 'JuddFalls', 'LupineTrail', 
    'ParadiseBasin', 'RustlersGulch', 'SlideRockRoad', 'SnodgrassTrailhead', 
    'SouthBaldy', 'StrandHill', 'VirginiaBasin'
]

bad_files = [
    "VirginiaBasin_2019_07_10_snow.tif", "VirginiaBasin_2019_07_17_snow.tif",
    "VirginiaBasin_2019_07_24_snow.tif", "VirginiaBasin_2019_07_30_snow.tif",
    "VirginiaBasin_2020_08_01_snow.tif", "VirginiaBasin_2020_08_08_snow.tif",
    "ParadiseBasin_2020_06_12_snow.tif", "ParadiseBasin_2019_08_02_snow.tif",
    "EastRiverTrail_2020_05_26_snow.tif", "DeerCreekTrail_2019_05_11_snow.tif",
    "EastRiverTrail_2020_05_05_snow.tif",
]

def crop_image_to_mask(image_path, mask_path, dest_image_path):
    with rasterio.open(image_path) as src:
        with rasterio.open(mask_path) as mask_src:
            # Rescale image to match mask
            print("Resampling image to match mask...")
            resampled_image = resample(src, mask_src)
            # Create a mask
            print("Creating mask...")
            mask_array = mask_src.read(1)
            mask_boolean = create_mask(mask_array)

            # Crop the resampled image using the mask
            print("Cropping image...")
            cropped_image = np.where(mask_boolean, resampled_image, np.nan)

            out_meta = mask_src.meta.copy()
            out_meta.update({
                "driver": "GTiff",
                "height": mask_src.height,
                "width": mask_src.width,
                "transform": mask_src.transform,
                "count": resampled_image.shape[0]
            })

            with rasterio.open(dest_image_path, "w", **out_meta) as dest:
                for i in range(out_meta['count']):
                    print("Writing the cropped image...")
                    dest.write(cropped_image[i], i + 1)



def process_images():
    '''
    don't look at the bad files
    1. Get the mask for the location
    2. Get the images for the location
    3. Crop the images to the size of the mask
    
    the destination directory will be the location in dest_path
    will have 2 subfolders 1 for the images and 1 for the masks
    
    '''
    location_count = 0
    for location in locations:
        print("Processing location: ", location)
        img_dir = os.path.join(IMAGERY_FILEPATH, location)
        mask_dir = os.path.join(SNOW_MASK_FILEPATH, location)
        img_dest_dir = os.path.join(DEST_FILEPATH, 'Imagery', location)
        mask_dest_dir = os.path.join(DEST_FILEPATH, 'Snow_Mask', location)

        os.makedirs(img_dest_dir, exist_ok=True)
        os.makedirs(mask_dest_dir, exist_ok=True)

        # Getting the IMG file names: 
        img_file_names = [img_file for img_file in os.listdir(img_dir) if img_file.endswith('.tif') and img_file not in bad_files]

        #Going through each image file in the location 
        for img_file in img_file_names:
            print("Processing image: ", img_file)
            img_path = os.path.join(img_dir, img_file)
            # img file ends in _snow.tif, mask ends in _snowbinary.tif
            # replace .tif with binary.tif to get the mask file name
            mask_file = img_file.replace('.tif', 'binary.tif') 
            mask_path = os.path.join(mask_dir, mask_file)
            dest_img_path = os.path.join(img_dest_dir, os.path.splitext(img_file)[0] + "_cropped.tif")

            if os.path.exists(mask_path):
                print("Cropping image to mask...")
                crop_image_to_mask(img_path, mask_path, dest_img_path)
                # Explicitly delete variables to free up memory
                del img_path, mask_path, dest_img_path



# # Define test paths for a sample image and mask
sample_image_path = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Imagery/DeerCreekTrail/DeerCreekTrail_2020_06_13_snow.tif"
sample_mask_path = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask/DeerCreekTrail/DeerCreekTrail_2019_06_13_snowbinary.tif"
sample_dest_image_path = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/Cut_Images/Imagery/DeerCreekTrail/DeerCreekTrail_2019_06_13_snow.tif"

# # Create necessary directories if they don't exist
os.makedirs(os.path.dirname(sample_dest_image_path), exist_ok=True)

# # Call the function with the test paths
crop_image_to_mask(sample_image_path, sample_mask_path, sample_dest_image_path)
# DeerCreekTrail_2019_05_11_snow.tif
# DeerCreekTrail_2019_05_11_snowbinary.tif


# if __name__ == "__main__":
#     print("Processing images...")
#     process_images()
#     print("Done processing images.")