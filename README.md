# Gangotri Glacier Snow Retreat Monitoring

This project tracks snow and ice cover variations in the Gangotri Glacier region from 2019 to 2024 using Sentinel-2 satellite imagery. It applies the Normalized Difference Snow Index (NDSI) and computer vision techniques to quantify seasonal retreat patterns.

## Technical Approach

- **Data Conversion:** Translates raw Copernicus JPEG2000 (JP2) imagery into Cloud Optimized GeoTIFFs (COGs) using GDAL for efficient processing.
- **Targeted Data Extraction:** Uses `rasterio` windowed reading with `Window(4000, 4000, 2000, 2000)` to extract a precise 400 km² Region of Interest (ROI), avoiding the need to load 5GB raw scenes into memory.
- **Resolution Alignment:** Upsamples 20m SWIR data (Band 11) to match the 10m Green band (Band 3) using bilinear interpolation via `scipy.ndimage.zoom`.
- **Index Calculation:** Computes NDSI and applies a `> 0.40` threshold to generate binary snow masks.
- **Morphological Cleaning:** Applies OpenCV morphological opening (`MORPH_OPEN`) with a `3x3` elliptical kernel to clean the binary mask and remove isolated noise pixels.
- **Image Enhancement:** Uses `skimage.exposure` to apply gamma correction and percentile-based contrast stretching for true-color visual verification.

## Tech Stack

- **Geospatial:** Rasterio, GDAL
- **Computer Vision and Math:** OpenCV (`cv2`), SciPy, NumPy, Scikit-Image
- **Visualization:** Matplotlib

## Repository Structure

```text
project/
├── data/
│   ├── raw_sentinel2_cogs/   # COG files (not tracked in git)
├── notebooks/                # Exploratory data analysis
├── src/
│   ├── 01_convert_to_cog.py  # GDAL conversion script
│   ├── 02_ndsi_pipeline.py   # Core analysis and masking logic
│   └── 03_visualization.py   # Generation of trend plots and galleries
├── outputs/                  # High-resolution PNG outputs
└── README.md
```

## Setup and Usage

### 1. Install dependencies

```bash
pip install rasterio numpy scipy opencv-python matplotlib scikit-image
```

### 2. Data preparation

Sentinel-2 Level-2A imagery is required for this project. Download the required `B02`, `B03`, `B04`, and `B11` JP2 files for the selected dates from Copernicus Browser.

Convert the raw JPEG2000 files into Cloud Optimized GeoTIFFs using:

```bash
python src/01_convert_to_cog.py
```

### 3. Run analysis

Execute the NDSI pipeline to calculate snow cover, generate binary masks, and estimate snow-covered area:

```bash
python src/02_ndsi_pipeline.py
```

### 4. Generate visual outputs

Run the visualization script to create trend plots, visual galleries, and methodology graphics:

```bash
python src/03_visualization.py
```

## Key Outputs

- **5-Year Trend Graph:** Tracks total snow and ice cover area in late June observations from 2019 to 2024.
- **Methodology Pipeline Graphic:** A 3-panel visualization showing Green band input, NDSI heatmap, and final binary snow mask.
- **Visual Gallery:** A 2x5 comparison of optical satellite views and detected snow masks across five years.
- **True Color Map:** A high-contrast RGB image of the Gangotri Glacier study area for visual interpretation.

## Notes

- Raw Sentinel-2 files are large, so they are not included in the repository.
- Only processed COG-based workflow files and outputs should be documented in the repo.
- The project focuses on a fixed study window for consistent year-to-year comparison.
