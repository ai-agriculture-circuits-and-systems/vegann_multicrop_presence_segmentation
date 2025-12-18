import os
import json
import random
import time
import cv2
import numpy as np
from pathlib import Path

def generate_unique_id():
    random_part = random.randint(1000000, 9999999)
    timestamp_part = int(time.time()) % 1000
    return int(f"{random_part}{timestamp_part:03d}")

def find_white_regions(mask_path):
    if not os.path.exists(mask_path):
        return []
    
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return []
    
    white_pixels = np.where(mask > 127)
    
    if len(white_pixels[0]) == 0:
        return []
    
    y_coords = white_pixels[0]
    x_coords = white_pixels[1]
    
    x_min, x_max = np.min(x_coords), np.max(x_coords)
    y_min, y_max = np.min(y_coords), np.max(y_coords)
    
    bbox = [int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)]
    area = int((x_max - x_min) * (y_max - y_min))
    
    segmentation = [
        int(x_min), int(y_min),
        int(x_max), int(y_min),
        int(x_max), int(y_max),
        int(x_min), int(y_max)
    ]
    
    return [{
        "segmentation": [segmentation],
        "area": area,
        "bbox": bbox
    }]

def create_coco_annotation(image_path, annotation_path, image_id, category_id, category_name):
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    height, width = img.shape[:2]
    file_name = os.path.basename(image_path)
    file_size = os.path.getsize(image_path)
    
    annotations_data = find_white_regions(annotation_path)
    
    if not annotations_data:
        annotations_data = [{
            "segmentation": [[0, 0, width, 0, width, height, 0, height]],
            "area": width * height,
            "bbox": [0, 0, width, height]
        }]
    
    image_info = {
        "id": image_id,
        "width": width,
        "height": height,
        "file_name": file_name,
        "size": file_size,
        "format": "PNG",
        "url": "",
        "hash": "",
        "status": "success"
    }
    
    annotations = []
    for ann_data in annotations_data:
        annotation = {
            "id": generate_unique_id(),
            "image_id": image_id,
            "category_id": category_id,
            "segmentation": ann_data["segmentation"],
            "area": ann_data["area"],
            "bbox": ann_data["bbox"]
        }
        annotations.append(annotation)
    
    category = {
        "id": category_id,
        "name": category_name,
        "supercategory": "vegann"
    }
    
    coco_data = {
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
        "images": [image_info],
        "annotations": annotations,
        "categories": [category]
    }
    
    return coco_data

def read_csv_simple(csv_path):
    data = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines[1:]:
            parts = line.strip().split(';')
            if len(parts) >= 8:
                data.append({
                    'Name': parts[0],
                    'Species': parts[7]
                })
    return data

def main():
    print("Starting COCO annotation generation...")
    
    # Get root directory (go up from scripts/ to root)
    script_dir = Path(__file__).parent
    root_dir = script_dir.parent
    
    csv_path = root_dir / "data" / "origin" / "VegAnn_dataset.csv"
    images_dir = root_dir / "data" / "origin" / "images"
    annotations_dir = root_dir / "data" / "origin" / "annotations_original"
    
    data = read_csv_simple(csv_path)
    print(f"Read {len(data)} rows from CSV")
    
    species_set = set()
    for row in data:
        species = row['Species']
        if species not in ['Species', 'Na'] and species:
            species_set.add(species)
    
    species_list = list(species_set)
    category_mapping = {}
    for i, species in enumerate(species_list, 1):
        category_mapping[species] = i
    
    print(f"Found {len(species_list)} species: {species_list}")
    
    processed_count = 0
    for row in data:
        image_name = row['Name']
        species = row['Species']
        
        if species in ['Species', 'Na'] or not species:
            continue
        
        image_path = images_dir / image_name
        annotation_path = annotations_dir / image_name
        
        if not image_path.exists() or not annotation_path.exists():
            continue
        
        image_id = generate_unique_id()
        category_id = category_mapping[species]
        
        coco_data = create_coco_annotation(
            str(image_path), str(annotation_path), image_id, category_id, species
        )
        
        if coco_data is None:
            continue
        
        # Save JSON to original images directory (for backward compatibility)
        json_filename = os.path.splitext(image_name)[0] + ".json"
        json_path = images_dir / json_filename
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(coco_data, f, indent=2, ensure_ascii=False)
        
        processed_count += 1
        if processed_count % 100 == 0:
            print(f"Processed {processed_count} images...")
    
    print(f"Completed! Generated {processed_count} JSON files.")

if __name__ == "__main__":
    main() 