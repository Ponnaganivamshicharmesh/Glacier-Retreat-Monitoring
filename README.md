# Glacier Retreat Monitoring

A remote sensing project for tracking snow cover variation in the Gangotri Glacier region using Sentinel-2 satellite imagery, NDSI-based snow mapping, and multi-year temporal analysis in Python [1][2].

## Overview

This project analyzes snow cover changes over time to study glacier retreat patterns in the Gangotri Glacier region. The workflow uses Sentinel-2 imagery, processes Cloud Optimized GeoTIFF files, and applies the Normalized Difference Snow Index to identify snow-covered areas [3][4][1].

## Objectives

- Monitor snow cover extent in the Gangotri Glacier region across multiple time periods [2][5]
- Use Sentinel-2 imagery for high-resolution snow mapping [6][3]
- Apply NDSI-based segmentation to separate snow from non-snow surfaces [1][7]
- Compare temporal snow coverage trends to assess seasonal and long-term retreat patterns [8][9]

## Dataset

The project uses Sentinel-2 Level-2A imagery, which provides high-resolution optical data with broad land-surface coverage and frequent revisit intervals [3]. Data can be accessed in Cloud Optimized GeoTIFF format, which is structured for efficient cloud-based reading and partial retrieval [4][3].

## Methodology

1. Collect Sentinel-2 imagery for the study region across selected dates [3].
2. Preprocess imagery and handle cloud-aware masking before snow analysis [10][11].
3. Compute the Normalized Difference Snow Index using Sentinel-2 Band 3 and Band 11:

$$
NDSI = \frac{B3 - B11}{B3 + B11}
$$

This index is commonly used to distinguish snow because snow has strong reflectance in the green band and absorption in the SWIR band [1][7].

4. Apply threshold-based snow classification to generate snow masks. A commonly used threshold for Sentinel-2 snow mapping is around 0.42, though threshold tuning may vary by scene and conditions [1][10].
5. Measure snow-covered area for each observation date and compare results over time to study retreat behavior [8][2].

## Tech Stack

- Python for image processing, analysis, and temporal comparison
- Sentinel-2 satellite imagery for snow monitoring [3]
- Cloud Optimized GeoTIFF for efficient raster access [4]
- NDSI for snow cover extraction [1]
- Remote sensing workflows for glacier and snow cover assessment [2][9]

## Project Structure

```text
project/
├── data/
│   ├── raw_sentinel2_cogs/
│   └── processed/
├── notebooks/
├── src/
│   ├── preprocessing.py
│   ├── ndsi_analysis.py
│   └── temporal_analysis.py
├── outputs/
│   ├── snow_masks/
│   ├── plots/
│   └── summary_tables/
└── README.md
```

## Expected Outputs

- Snow cover masks for each selected Sentinel-2 scene
- Temporal comparison plots showing snow extent variation
- Area-based summaries of snow cover across years or seasons
- Visual evidence of snow retreat trends in the glacier region

## Resume Description

Developed a remote sensing pipeline to monitor snow cover variation in the Gangotri Glacier region using Sentinel-2 imagery and NDSI-based segmentation. Processed multi-year satellite data in Cloud Optimized GeoTIFF format and analyzed temporal snow extent changes in Python to identify seasonal retreat trends [1][4][3].

## Notes

Gangotri Glacier has been widely studied using remote sensing for snow and glacier monitoring, and NDSI remains a standard approach for snow cover extraction in optical imagery [2][9][1]. Sentinel-2 data is especially useful for this task because of its spatial resolution and repeat coverage [6][3].
