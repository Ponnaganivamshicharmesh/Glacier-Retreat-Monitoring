#!/usr/bin/env python3
"""
Calculate the Normalized Difference Snow Index (NDSI) for the Gangotri Glacier.
Run this from the root of the repository: python 02_ndsi_pipeline.py
"""

import rasterio
import numpy as np
from scipy.ndimage import zoom
import cv2
from rasterio.windows import Window
import warnings

warnings.filterwarnings("ignore")

def main():
    base_dir = "data/raw_sentinel2_cogs"
    years_data = {
        '2019': {'B03': f'{base_dir}/T44RLV_20190626T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20190626T051701_B11_20m.tif'},
        '2020': {'B03': f'{base_dir}/T44RLV_20200630T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20200630T051701_B11_20m.tif'},
        '2021': {'B03': f'{base_dir}/T44RLV_20210630T051649_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20210630T051649_B11_20m.tif'},
        '2022': {'B03': f'{base_dir}/T44RLV_20220625T051659_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20220625T051659_B11_20m.tif'},
        '2024': {'B03': f'{base_dir}/T44RLV_20240619T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20240619T051701_B11_20m.tif'}
    }

    results = {}
    window_10m = Window(4000, 4000, 2000, 2000)
    window_20m = Window(2000, 2000, 1000, 1000)

    print("Calculating NDSI Snow Cover for Gangotri Glacier...\n")

    for year, paths in years_data.items():
        try:
            with rasterio.open(paths['B03']) as g_src, rasterio.open(paths['B11']) as s_src:
                green = (g_src.read(1, window=window_10m).astype(np.float32) / 10000).clip(0, 1)
                swir = (s_src.read(1, window=window_20m).astype(np.float32) / 10000).clip(0, 1)

                swir_10m = zoom(swir, 2.0, order=1)
                ndsi = (green - swir_10m) / (green + swir_10m + 1e-6)

                snow_mask = (ndsi > 0.40).astype(np.uint8)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                clean_mask = cv2.morphologyEx(snow_mask, cv2.MORPH_OPEN, kernel)

                snow_km2 = (clean_mask.sum() * 100) / 1_000_000
                results[year] = snow_km2
                print(f"{year}: {snow_km2:.2f} km² snow/ice cover")

        except rasterio.errors.RasterioIOError:
            print(f"Skipping {year}: File not found. Ensure {paths['B03']} exists.")
        except Exception as e:
            print(f"Error processing {year}: {e}")

    print("\nPipeline complete.")

if __name__ == "__main__":
    main()
