import os
import rasterio
import rasterio.mask as mask
import numpy as np
# import tpqm 



SOURCE_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data"
IMAGERY_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Imagery"
SNOW_MASK_FILEPATH = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask"
DEST_FILEPATH = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/TinyImages"

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
            mask_array = mask_src.read(1)
            mask_geom = mask_src.bounds
            mask_geom = [{
                "type": "Polygon",
                "coordinates": [[
                    [mask_geom.left, mask_geom.top],
                    [mask_geom.right, mask_geom.top],
                    [mask_geom.right, mask_geom.bottom],
                    [mask_geom.left, mask_geom.bottom],
                    [mask_geom.left, mask_geom.top]
                ]]
            }]

            out_image, out_transform = mask.mask(src, mask_geom, crop=True)
            out_meta = src.meta.copy()

            out_meta.update({
                "driver": "GTiff",
                "height": out_image.shape[1],
                "width": out_image.shape[2],
                "transform": out_transform
            })

            with rasterio.open(dest_image_path, "w", **out_meta) as dest:
                dest.write(out_image)



def process_images():
    '''
    don't look at the bad files
    1. Get the mask for the location
    2. Get the images for the location
    3. Crop the images to the size of the mask
    
    the destination directory will be the location in dest_path
    will have 2 subfolders 1 for the images and 1 for the masks
    
    '''
    for location in locations:
        img_dir = os.path.join(IMAGERY_FILEPATH, location)
        mask_dir = os.path.join(SNOW_MASK_FILEPATH, location)
        img_dest_dir = os.path.join(DEST_FILEPATH, 'Imagery', location)
        mask_dest_dir = os.path.join(DEST_FILEPATH, 'Snow_Mask', location)

        os.makedirs(img_dest_dir, exist_ok=True)
        os.makedirs(mask_dest_dir, exist_ok=True)

        for img_file in os.listdir(img_dir):
            if img_file.endswith('.tif') and img_file not in bad_files:
                img_path = os.path.join(img_dir, img_file)
                mask_path = os.path.join(mask_dir, img_file)
                dest_img_path = os.path.join(img_dest_dir, os.path.splitext(img_file)[0] + "_cropped.tif")

                if os.path.exists(mask_path):
                    crop_image_to_mask(img_path, mask_path, dest_img_path)
                    # Explicitly delete variables to free up memory
                    del img_path, mask_path, dest_img_path



# Define test paths for a sample image and mask
sample_image_path = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Imagery/DeerCreekTrail/DeerCreekTrail_2019_05_11_snow.tif"
sample_mask_path = "/Users/joel-carlson/Library/CloudStorage/OneDrive-SharedLibraries-UCB-O365/Travis Hainsworth - RMBL/2 - Source Data/2019-2020_Data/Snow_Mask/DeerCreekTrail/DeerCreekTrail_2019_05_11_snowbinary.tif"
sample_dest_image_path = "/Users/joel-carlson/Library/Mobile Documents/com~apple~CloudDocs/Summer-2024/RMBL/RMBL_SnowView/data/TinyImages/Imagery/DeerCreekTrail/DeerCreekTrail_2019_05_11_snow.tif"

# Create necessary directories if they don't exist
os.makedirs(os.path.dirname(sample_dest_image_path), exist_ok=True)

# Call the function with the test paths
crop_image_to_mask(sample_image_path, sample_mask_path, sample_dest_image_path)
