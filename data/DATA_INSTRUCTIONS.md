# Data Requirements

The raw Sentinel-2 satellite imagery is approximately 5GB and is not included in this repository. 

To run this project, you need to download the data yourself:

1. Go to the [Copernicus Data Space](https://dataspace.copernicus.eu/).
2. Search for the Gangotri Glacier Region (Tile: T44RLV).
3. Download the Level-2A imagery for the late-June dates between 2019 and 2024.
4. Extract the `.jp2` files for Bands 02, 03, 04, and 11.
5. Place those `.jp2` files into the `data/raw_jp2/` folder.

Once the files are in place, run `python 01_convert_to_cog.py` from the root directory to convert them to Cloud Optimized GeoTIFFs.
