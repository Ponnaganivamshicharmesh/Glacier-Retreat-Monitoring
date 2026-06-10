Gangotri Glacier Snow Retreat Monitoring
This project tracks snow and ice cover variations in the Gangotri Glacier region from 2019 to 2024 using Sentinel-2 satellite imagery. It applies the Normalized Difference Snow Index (NDSI) and computer vision techniques to quantify seasonal retreat patterns.

Technical Approach
Data Conversion: Translates raw Copernicus JPEG2000 (JP2) imagery into Cloud Optimized GeoTIFFs (COGs) using GDAL for efficient processing.

Targeted Data Extraction: Uses rasterio windowed reading (Window(4000, 4000, 2000, 2000)) to extract a precise 400 km² Region of Interest (ROI), bypassing the need to load 5GB raw scenes into memory.

Resolution Alignment: Upsamples 20m SWIR data (Band 11) to match the 10m Green band (Band 3) using bilinear interpolation via scipy.ndimage.zoom.

Index Calculation: Computes NDSI and applies a >0.40 threshold to generate binary snow masks.

Morphological Cleaning: Applies OpenCV morphological opening (MORPH_OPEN) with a 3x3 elliptical kernel to clean the binary mask and remove isolated noise pixels.

Image Enhancement: Uses skimage.exposure to apply 2.2 gamma correction and percentile-based contrast stretching for true-color visual verification.

Tech Stack
Geospatial: Rasterio, GDAL

Computer Vision & Math: OpenCV (cv2), SciPy, NumPy, Scikit-Image

Visualization: Matplotlib

Repository Structure
text
project/
├── data/
│   ├── raw_sentinel2_cogs/   # COG files (Not tracked in git)
├── notebooks/                # Exploratory data analysis
├── src/
│   ├── 01_convert_to_cog.py  # GDAL conversion script
│   ├── 02_ndsi_pipeline.py   # Core analysis and masking logic
│   └── 03_visualization.py   # Generation of trend plots and galleries
├── outputs/                  # High-res PNG outputs
└── README.md
Setup and Usage
Install dependencies:

bash
pip install rasterio numpy scipy opencv-python matplotlib scikit-im
