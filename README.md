# VegAnn Multicrop Presence Segmentation Dataset

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://zenodo.org/records/7636408)

A comprehensive dataset of agricultural crop images for multicrop presence segmentation, collected and organized for computer vision and deep learning research in agricultural applications.

**Project page**: `https://zenodo.org/records/7636408`

## TL;DR

- **Task**: Segmentation, Object Detection
- **Modality**: RGB
- **Platform**: Ground/Field (Handheld Cameras)
- **Real/Synthetic**: Real
- **Images**: 3,645 agricultural crop images across 26 categories
- **Resolution**: Variable (typically 512×512 pixels)
- **Annotations**: CSV (per-image), JSON (per-image), COCO JSON (generated), Segmentation masks (PNG)
- **License**: CC BY 4.0
- **Citation**: see below

## Table of Contents

- [Download](#download)
- [Dataset Structure](#dataset-structure)
- [Sample Images](#sample-images)
- [Annotation Schema](#annotation-schema)
- [Stats and Splits](#stats-and-splits)
- [Quick Start](#quick-start)
- [Evaluation and Baselines](#evaluation-and-baselines)
- [Datasheet (Data Card)](#datasheet-data-card)
- [Known Issues and Caveats](#known-issues-and-caveats)
- [License](#license)
- [Citation](#citation)
- [Changelog](#changelog)
- [Contact](#contact)

## Download

**Original dataset**: `https://zenodo.org/records/7636408/files/VegAnn_dataset.zip?download=1`

This repo hosts structure and conversion scripts only; place the downloaded folders under this directory.

**Local license file**: See `LICENSE` in the root directory.

## Dataset Structure

```
vegann_multicrop_presence_segmentation/
├── alfalfas/                          # Alfalfa crop category
│   ├── csv/                           # CSV annotation files (per-image)
│   ├── json/                          # JSON annotation files (per-image)
│   ├── images/                        # Image files
│   ├── segmentations/                 # Segmentation mask files (PNG)
│   ├── sets/                          # Dataset split files
│   │   ├── train.txt                  # Training set image list
│   │   ├── val.txt                    # Validation set image list
│   │   ├── test.txt                   # Test set image list
│   │   ├── all.txt                    # All images list
│   │   └── train_val.txt              # Train+val images list
│   └── labelmap.json                  # Label mapping file
│
├── barleys/                           # Barley crop category
│   └── ...                           # Same structure as alfalfas
│
├── beans/                             # Bean crop category
│   └── ...                           # Same structure as alfalfas
│
├── cabbages/                          # Cabbage crop category
│   └── ...                           # Same structure as alfalfas
│
├── faba_beans/                         # Faba bean crop category
│   └── ...                           # Same structure as alfalfas
│
├── grasslands/                         # Grassland vegetation category
│   └── ...                           # Same structure as alfalfas
│
├── maizes/                            # Maize/corn crop category
│   └── ...                           # Same structure as alfalfas
│
├── mixes/                             # Mixed crop category
│   └── ...                           # Same structure as alfalfas
│
├── mustards/                          # Mustard crop category
│   └── ...                           # Same structure as alfalfas
│
├── oats/                              # Oat crop category
│   └── ...                           # Same structure as alfalfas
│
├── onions/                            # Onion crop category
│   └── ...                           # Same structure as alfalfas
│
├── peas/                              # Pea crop category
│   └── ...                           # Same structure as alfalfas
│
├── peppers/                            # Pepper crop category
│   └── ...                           # Same structure as alfalfas
│
├── potatoes/                           # Potato crop category
│   └── ...                           # Same structure as alfalfas
│
├── radishes/                           # Radish crop category
│   └── ...                           # Same structure as alfalfas
│
├── rapeseeds/                          # Rapeseed crop category
│   └── ...                           # Same structure as alfalfas
│
├── raspberries/                        # Raspberry crop category
│   └── ...                           # Same structure as alfalfas
│
├── rices/                              # Rice crop category
│   └── ...                           # Same structure as alfalfas
│
├── sorghums/                           # Sorghum crop category
│   └── ...                           # Same structure as alfalfas
│
├── sorrels/                            # Sorrel crop category
│   └── ...                           # Same structure as alfalfas
│
├── soybeans/                           # Soybean crop category
│   └── ...                           # Same structure as alfalfas
│
├── sugarbeets/                         # Sugar beet crop category
│   └── ...                           # Same structure as alfalfas
│
├── sunflowers/                         # Sunflower crop category
│   └── ...                           # Same structure as alfalfas
│
├── tobaccos/                           # Tobacco crop category
│   └── ...                           # Same structure as alfalfas
│
├── vetches/                            # Vetch crop category
│   └── ...                           # Same structure as alfalfas
│
├── wheats/                             # Wheat crop category
│   └── ...                           # Same structure as alfalfas
│
├── annotations/                        # COCO format JSON files (generated)
│   ├── alfalfas_instances_train.json
│   ├── alfalfas_instances_val.json
│   ├── alfalfas_instances_test.json
│   ├── barleys_instances_*.json
│   ├── ...                            # Other category files
│   └── combined_instances_*.json      # Combined multi-category files
│
├── data/                               # Original data directory
│   └── origin/                         # Original dataset files (preserved)
│       ├── images/                     # Original image files
│       ├── annotations_original/       # Original segmentation masks (PNG)
│       └── VegAnn_dataset.csv          # Original dataset metadata CSV
│
├── scripts/                            # Utility scripts
│   ├── reorganize_dataset.py          # Reorganize dataset to standard structure
│   ├── convert_to_coco.py             # Convert CSV to COCO format
│   └── generate_coco_annotations.py   # Original COCO annotation generator
│
├── LICENSE                             # License file
├── README.md                           # This file
└── requirements.txt                    # Python dependencies
```

**Splits**: Splits provided via `{category}/sets/*.txt`. List image basenames (no extension). If missing, all images are used.

## Sample Images

<table>
  <tr>
    <th>Category</th>
    <th>Sample</th>
  </tr>
  <tr>
    <td><strong>Wheat</strong></td>
    <td>
      <img src="wheats/images/VegAnn_1010.png" alt="Wheat crop image" width="260"/>
      <div align="center"><code>wheats/images/VegAnn_1010.png</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Mix</strong></td>
    <td>
      <img src="mixes/images/VegAnn_0.png" alt="Mixed crop image" width="260"/>
      <div align="center"><code>mixes/images/VegAnn_0.png</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Rice</strong></td>
    <td>
      <img src="rices/images/VegAnn_100.png" alt="Rice crop image" width="260"/>
      <div align="center"><code>rices/images/VegAnn_100.png</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Rapeseed</strong></td>
    <td>
      <img src="rapeseeds/images/VegAnn_200.png" alt="Rapeseed crop image" width="260"/>
      <div align="center"><code>rapeseeds/images/VegAnn_200.png</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Maize</strong></td>
    <td>
      <img src="maizes/images/VegAnn_300.png" alt="Maize crop image" width="260"/>
      <div align="center"><code>maizes/images/VegAnn_300.png</code></div>
    </td>
  </tr>
  <tr>
    <td><strong>Sunflower</strong></td>
    <td>
      <img src="sunflowers/images/VegAnn_400.png" alt="Sunflower crop image" width="260"/>
      <div align="center"><code>sunflowers/images/VegAnn_400.png</code></div>
    </td>
  </tr>
</table>

## Annotation Schema

### CSV Format

Each image has a corresponding CSV annotation file in `{category}/csv/{image_name}.csv`:

```csv
#item,x,y,width,height,label
0,0,0,512,512,1
```

- **Coordinates**: `x, y` - top-left corner of bounding box (pixels)
- **Dimensions**: `width, height` - bounding box dimensions (pixels)
- **Label**: Category ID (1=category, 0=background)

For segmentation tasks, the bounding box typically covers the entire image `[0, 0, image_width, image_height]`.

### JSON Format (Per-Image)

Each image also has a corresponding JSON annotation file in `{category}/json/{image_name}.json`:

```json
{
  "info": {
    "description": "data",
    "version": "1.0",
    "year": 2025,
    "contributor": "search engine",
    "source": "augmented",
    "license": {
      "name": "Creative Commons Attribution 4.0 International",
      "url": "https://creativecommons.org/licenses/by/4.0/"
    }
  },
  "images": [
    {
      "id": 8054743615,
      "width": 512,
      "height": 512,
      "file_name": "VegAnn_0.png",
      "size": 544128,
      "format": "PNG",
      "url": "",
      "hash": "",
      "status": "success"
    }
  ],
  "annotations": [
    {
      "id": 1812191615,
      "image_id": 8054743615,
      "category_id": 1,
      "segmentation": [[0, 0, 511, 0, 511, 511, 0, 511]],
      "area": 261121,
      "bbox": [0, 0, 511, 511]
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "mix",
      "supercategory": "vegann"
    }
  ]
}
```

### COCO Format

COCO format JSON files are generated in the `annotations/` directory. Example structure:

```json
{
  "info": {
    "year": 2025,
    "version": "1.0",
    "description": "VegAnn Multicrop Presence Segmentation wheats train split",
    "url": "https://zenodo.org/records/7636408"
  },
  "images": [
    {
      "id": 1234567890,
      "file_name": "wheats/images/VegAnn_1010.png",
      "width": 512,
      "height": 512
    }
  ],
  "annotations": [
    {
      "id": 1,
      "image_id": 1234567890,
      "category_id": 1,
      "bbox": [0, 0, 512, 512],
      "area": 262144,
      "iscrowd": 0
    }
  ],
  "categories": [
    {
      "id": 1,
      "name": "wheat",
      "supercategory": "crop"
    }
  ],
  "licenses": []
}
```

### Label Maps

Each category directory contains a `labelmap.json` file:

```json
[
  {
    "object_id": 0,
    "label_id": 0,
    "keyboard_shortcut": "0",
    "object_name": "background"
  },
  {
    "object_id": 1,
    "label_id": 1,
    "keyboard_shortcut": "1",
    "object_name": "wheat"
  }
]
```

### Segmentation Masks

Segmentation masks are stored in `{category}/segmentations/{image_name}.png` as binary PNG images. White pixels represent crop areas.

**Note**: The original segmentation masks (PNG files) are preserved in `data/origin/annotations_original/`. The root `annotations/` directory is reserved for COCO format JSON files generated by the conversion scripts.

## Stats and Splits

### Image Counts by Category

- **Wheat**: 1,291 images
- **Mix**: 708 images
- **Rice**: 466 images
- **Rapeseed**: 276 images
- **Maize**: 256 images
- **Sunflower**: 187 images
- **Sugarbeet**: 84 images
- **Potato**: 76 images
- **Grassland**: 49 images
- **Faba beans**: 48 images
- **Sorghum**: 40 images
- **Tobacco**: 34 images
- **Alfalfa**: 27 images
- **Mustard**: 24 images
- **Vetch**: 18 images
- **Soybean**: 17 images
- **Radish**: 12 images
- **Raspberry**: 11 images
- **Pepper**: 7 images
- **Bean**: 5 images
- **Barley**: 3 images
- **Pea**: 2 images
- **Sorrel**: 1 image
- **Onion**: 1 image
- **Oat**: 1 image
- **Cabbage**: 1 image

**Total**: 3,645 images across 26 categories

### Dataset Splits

Splits are provided via `{category}/sets/*.txt`. The dataset uses the first split (TVT-split1) from the original CSV file:
- **Training set**: ~70-80% of images
- **Validation set**: ~5-15% of images
- **Test set**: ~5-20% of images

Note: Some categories have very few images, so splits may be imbalanced. Splits provided via `{category}/sets/*.txt`. You may define your own splits by editing those files.

## Quick Start

### Load COCO Format Annotations

```python
from pycocotools.coco import COCO
import matplotlib.pyplot as plt

# Load COCO annotation file
coco = COCO('annotations/combined_instances_train.json')

# Get all image IDs
img_ids = coco.getImgIds()
print(f"Total images: {len(img_ids)}")

# Get all category IDs
cat_ids = coco.getCatIds()
print(f"Categories: {[coco.loadCats(cat_id)[0]['name'] for cat_id in cat_ids]}")

# Load a specific image and its annotations
img_id = img_ids[0]
img_info = coco.loadImgs(img_id)[0]
ann_ids = coco.getAnnIds(imgIds=img_id)
anns = coco.loadAnns(ann_ids)

print(f"Image: {img_info['file_name']}")
print(f"Annotations: {len(anns)}")
```

### Convert CSV to COCO Format

```bash
# Convert all categories to COCO format
python scripts/convert_to_coco.py --root . --out annotations --combined

# Convert specific categories
python scripts/convert_to_coco.py --root . --out annotations \
    --categories wheats rices maizes --splits train val test

# Generate combined files
python scripts/convert_to_coco.py --root . --out annotations --combined
```

### Dependencies

**Required**:
- Python 3.6+
- Pillow>=9.5

**Optional** (for COCO API):
- pycocotools>=2.0.7

Install dependencies:
```bash
pip install -r requirements.txt
```

## Evaluation and Baselines

### Metrics

- **Segmentation mAP**: Mean Average Precision for segmentation tasks
- **Detection mAP**: Mean Average Precision for detection tasks
- **Pixel Accuracy**: Pixel-level accuracy for segmentation masks

### Baseline Results

(To be added)

## Datasheet (Data Card)

### Motivation

This dataset was created to support research in automated crop detection and segmentation in agricultural settings. The dataset enables the development and evaluation of computer vision models for multicrop presence segmentation and agricultural applications.

### Composition

- **Image Types**: RGB images of agricultural crops in field conditions
- **Categories**: 26 crop species (Alfalfa, Barley, Bean, Cabbage, Faba beans, Grassland, Maize, Mix, Mustard, Oat, Onion, Pea, Pepper, Potato, Radish, Rapeseed, Raspberry, Rice, Sorghum, Sorrel, Soybean, Sugarbeet, Sunflower, Tobacco, Vetch, Wheat)
- **Image Format**: PNG
- **Image Size**: Variable (typically 512×512 pixels)
- **Annotation Format**: CSV (per-image), JSON (per-image), COCO JSON (generated), Segmentation masks (PNG)

### Collection Process

Images were collected using handheld cameras in field conditions. The dataset includes images from various agricultural settings with different crop species. Each image was annotated with segmentation masks and bounding boxes.

### Preprocessing

- Images were standardized to consistent formats
- Annotations were created with segmentation masks and bounding boxes
- Dataset was split into train/val/test sets based on original CSV metadata

### Distribution

The dataset is distributed under CC BY 4.0 license. See `LICENSE` file for details.

### Maintenance

This repository maintains the standardized structure and conversion scripts. Original data sources should be referenced appropriately.

## Known Issues and Caveats

1. **Image Resolution**: Images are typically 512×512 pixels. Original resolutions may vary.

2. **Split Imbalance**: Some categories have very few images (e.g., Cabbage: 1 image, Oat: 1 image), leading to imbalanced splits. Users may need to adjust splits for their specific use cases.

3. **Annotation Format**: For segmentation tasks, each image has segmentation masks stored as PNG files. The bounding boxes cover the entire image `[0, 0, image_width, image_height]` for presence detection.

4. **File Naming**: Image filenames follow the pattern `VegAnn_{number}.png`. Ensure proper handling when processing files.

5. **Category Distribution**: The dataset is heavily imbalanced, with Wheat having 1,291 images while some categories have only 1-2 images. This should be considered when training models.

6. **Segmentation Masks**: Segmentation masks are stored as binary PNG images in the `segmentations/` directory. White pixels represent crop areas.

## License

This dataset is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

Check the original dataset terms and cite appropriately.

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{vegann2025,
  title={VegAnn Multicrop Presence Segmentation Dataset},
  author={Arvalis},
  year={2025},
  url={https://zenodo.org/records/7636408},
  license={CC BY 4.0}
}
```

## Changelog

- **V1.0.0** (2025): Initial standardized structure and COCO conversion utility

## Contact

- **Maintainers**: Dataset maintainers
- **Original Authors**: Arvalis
- **Source**: `https://zenodo.org/records/7636408`
