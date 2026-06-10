#!/usr/bin/env python3
"""
Generate publication-ready visualizations for the Gangotri Glacier project.
Run this from the root of the repository: python 03_visualization.py
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import cv2
from scipy.ndimage import zoom
from rasterio.windows import Window
from skimage import exposure
import warnings
import os

warnings.filterwarnings("ignore")

def generate_trend_plot(results, output_dir):
    years = list(results.keys())
    areas = list(results.values())

    plt.figure(figsize=(12, 7))
    plt.plot(years, areas, 'o-', linewidth=4, markersize=12, color='#1f77b4', markerfacecolor='white', markeredgewidth=2)
    plt.fill_between(years, areas, alpha=0.2, color='#1f77b4')

    plt.title('Gangotri Glacier Snow/Ice Cover Trend\nT44RLV Tile (NDSI Analysis)', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Year (Late June Observations)', fontsize=14)
    plt.ylabel('Snow/Ice Area (km²)', fontsize=14)
    plt.ylim(0, max(areas) * 1.1)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    save_path = f'{output_dir}/gangotri_ndsi_trend.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved trend plot to {save_path}")

def generate_gallery(years_data, window_10m, window_20m, output_dir):
    fig, axs = plt.subplots(2, 5, figsize=(25, 10))
    fig.suptitle('Gangotri Glacier Basin: 5-Year Late-June Snow Cover Volatility (2019-2024)', fontsize=24, fontweight='bold', y=0.98)

    cmap_snow = mcolors.ListedColormap(['none', 'cyan'])

    for i, (year, paths) in enumerate(years_data.items()):
        try:
            with rasterio.open(paths['B03']) as g_src, rasterio.open(paths['B11']) as s_src:
                green = g_src.read(1, window=window_10m).astype(np.float32) / 10000
                swir = s_src.read(1, window=window_20m).astype(np.float32) / 10000

            swir_10m = zoom(swir, 2.0, order=1)
            ndsi = (green - swir_10m) / (green + swir_10m + 1e-6)
            snow_mask = ndsi > 0.40
            snow_km2 = (snow_mask.sum() * 100) / 1_000_000

            axs[0, i].imshow(green, cmap='gray', vmin=0, vmax=0.8)
            axs[0, i].set_title(f"June {year}\nOptical Satellite View", fontsize=16)
            axs[0, i].axis('off')

            axs[1, i].imshow(green, cmap='gray', vmin=0, vmax=0.8)
            axs[1, i].imshow(snow_mask, cmap=cmap_snow, alpha=0.5)
            axs[1, i].set_title(f"Detected Snow Area\n{snow_km2:.2f} km²", fontsize=16, fontweight='bold', color='darkblue')
            axs[1, i].axis('off')
        except Exception as e:
            print(f"Skipping {year} in gallery: missing data.")
            axs[0, i].axis('off')
            axs[1, i].axis('off')

    plt.tight_layout()
    plt.subplots_adjust(top=0.88, wspace=0.05, hspace=0.1)

    save_path = f'{output_dir}/5_year_visual_gallery.png'
    plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"Saved gallery to {save_path}")

def generate_true_color(output_dir):
    path_b02 = 'data/raw_jp2/T44RLV_20210630T051649_B02_10m.jp2'
    path_b03 = 'data/raw_jp2/T44RLV_20210630T051649_B03_10m.jp2'
    path_b04 = 'data/raw_jp2/T44RLV_20210630T051649_B04_10m.jp2'

    window = Window(4000, 4000, 2000, 2000)

    try:
        with rasterio.open(path_b04) as src_r, rasterio.open(path_b03) as src_g, rasterio.open(path_b02) as src_b:
            red = (src_r.read(1, window=window).astype(np.float32) / 10000).clip(0, 1)
            green = (src_g.read(1, window=window).astype(np.float32) / 10000).clip(0, 1)
            blue = (src_b.read(1, window=window).astype(np.float32) / 10000).clip(0, 1)

        rgb_image = np.dstack((red, green, blue))
        gamma_corrected = exposure.adjust_gamma(rgb_image, gamma=0.45)
        p2, p98 = np.percentile(gamma_corrected, (2, 98))
        final_rgb = exposure.rescale_intensity(gamma_corrected, in_range=(p2, p98))

        plt.figure(figsize=(10, 10))
        plt.imshow(final_rgb)
        plt.title('Study Area: Gangotri Glacier Basin\nTrue Color RGB (June 2021)', fontsize=16, fontweight='bold', pad=15)
        plt.axis('off')
        plt.text(50, 1950, 'Resolution: 10m/pixel', color='white', fontsize=12,
                 bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

        plt.tight_layout()
        save_path = f'{output_dir}/gangotri_true_color_study_area.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='black')
        plt.close()
        print(f"Saved true color image to {save_path}")

    except Exception as e:
        print(f"Could not generate True Color RGB. Ensure 2021 JP2 files are in data/raw_jp2/.")

def generate_methodology(output_dir):
    path_b03 = 'data/raw_sentinel2_cogs/T44RLV_20210630T051649_B03_10m.tif'
    path_b11 = 'data/raw_sentinel2_cogs/T44RLV_20210630T051649_B11_20m.tif'

    window_10m = Window(4000, 4000, 2000, 2000)
    window_20m = Window(2000, 2000, 1000, 1000)

    try:
        with rasterio.open(path_b03) as g_src, rasterio.open(path_b11) as s_src:
            green = (g_src.read(1, window=window_10m).astype(np.float32) / 10000).clip(0, 1)
            swir = (s_src.read(1, window=window_20m).astype(np.float32) / 10000).clip(0, 1)

        swir_10m = zoom(swir, 2.0, order=1)
        ndsi = (green - swir_10m) / (green + swir_10m + 1e-6)
        snow_mask = (ndsi > 0.40).astype(np.uint8)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        clean_mask = cv2.morphologyEx(snow_mask, cv2.MORPH_OPEN, kernel)

        fig, axs = plt.subplots(1, 3, figsize=(18, 6))
        fig.suptitle('Algorithm Pipeline: Normalized Difference Snow Index (NDSI)', fontsize=20, fontweight='bold', y=1.05)

        axs[0].imshow(green, cmap='gray', vmin=0, vmax=0.8)
        axs[0].set_title('Step 1: Input Optical Data\n(Band 03 - Green)', fontsize=14)
        axs[0].axis('off')

        im1 = axs[1].imshow(ndsi, cmap='coolwarm', vmin=-1, vmax=1)
        axs[1].set_title('Step 2: NDSI Calculation\n(B03 - B11) / (B03 + B11)', fontsize=14)
        axs[1].axis('off')
        fig.colorbar(im1, ax=axs[1], fraction=0.046, pad=0.04, label='NDSI Value')

        axs[2].imshow(clean_mask, cmap='gray')
        axs[2].set_title('Step 3: Binary Snow Mask\n(Threshold > 0.40)', fontsize=14)
        axs[2].axis('off')

        fig.text(0.5, -0.05,
                 "Methodology: 20m SWIR data was upsampled using bilinear interpolation to match the 10m Green band.\n"
                 "NDSI was calculated, and a strict >0.40 threshold was applied to isolate pure snow/ice pixels.",
                 ha='center', fontsize=12, style='italic', bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'))

        plt.tight_layout()
        save_path = f'{output_dir}/methodology_3_panel_ndsi.png'
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"Saved methodology graphic to {save_path}")

    except Exception as e:
        print(f"Could not generate methodology graphic: {e}")

def main():
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    results = {
        '2019': 85.50,
        '2020': 78.20,
        '2021': 92.10,
        '2022': 71.40,
        '2024': 68.30
    }

    base_dir = "data/raw_sentinel2_cogs"
    years_data = {
        '2019': {'B03': f'{base_dir}/T44RLV_20190626T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20190626T051701_B11_20m.tif'},
        '2020': {'B03': f'{base_dir}/T44RLV_20200630T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20200630T051701_B11_20m.tif'},
        '2021': {'B03': f'{base_dir}/T44RLV_20210630T051649_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20210630T051649_B11_20m.tif'},
        '2022': {'B03': f'{base_dir}/T44RLV_20220625T051659_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20220625T051659_B11_20m.tif'},
        '2024': {'B03': f'{base_dir}/T44RLV_20240619T051701_B03_10m.tif', 'B11': f'{base_dir}/T44RLV_20240619T051701_B11_20m.tif'}
    }

    window_10m = Window(4000, 4000, 2000, 2000)
    window_20m = Window(2000, 2000, 1000, 1000)

    print("Generating visualizations...")
    generate_trend_plot(results, output_dir)
    generate_gallery(years_data, window_10m, window_20m, output_dir)
    generate_true_color(output_dir)
    generate_methodology(output_dir)
    print("All visualizations complete. Check the 'outputs' directory.")

if __name__ == "__main__":
    main()
