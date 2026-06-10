#!/usr/bin/env python3
"""
Convert raw JPEG2000 Sentinel-2 imagery into Cloud Optimized GeoTIFFs (COGs).
Run this from the root of the repository: python 01_convert_to_cog.py
"""

import subprocess
from pathlib import Path
import sys

def main():
    jp2_folder = Path("data/raw_jp2")
    cog_folder = Path("data/raw_sentinel2_cogs")

    if not jp2_folder.exists():
        print(f"Error: Input folder {jp2_folder} does not exist.")
        print("Please place your raw .jp2 files there.")
        sys.exit(1)

    cog_folder.mkdir(parents=True, exist_ok=True)

    # Only convert the B03 and B11 files needed for NDSI, plus B02/B04 for true color
    needed_bands = ['B02_10m', 'B03_10m', 'B04_10m', 'B11_20m']
    jp2_files = [f for f in jp2_folder.glob("*.jp2") if any(band in f.name for band in needed_bands)]

    if not jp2_files:
        print(f"No matching .jp2 files found in {jp2_folder}.")
        sys.exit(1)

    print(f"Converting {len(jp2_files)} essential files...")

    for jp2_path in jp2_files:
        cog_filename = jp2_path.stem + ".tif"
        cog_path = cog_folder / cog_filename

        if cog_path.exists():
            print(f"[SKIP] {cog_filename} already exists.")
            continue

        cmd = [
            "gdal_translate",
            "-of", "COG",
            "-co", "COMPRESS=LZW",
            "-co", "TILED=YES",
            "-co", "BLOCKXSIZE=512",
            "-co", "BLOCKYSIZE=512",
            str(jp2_path),
            str(cog_path)
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"[SUCCESS] {cog_filename}")
        else:
            print(f"[ERROR] {jp2_path.name}: {result.stderr[:100]}")

    print(f"\nCOG conversion complete. Files are ready in {cog_folder}")

if __name__ == "__main__":
    main()
