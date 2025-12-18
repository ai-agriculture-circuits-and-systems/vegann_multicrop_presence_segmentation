#!/usr/bin/env python3
"""
Reorganize VegAnn dataset to standard structure.
"""
import os
import json
import csv
import shutil
from pathlib import Path
from collections import defaultdict

def get_category_name(species):
    """Convert species name to category directory name (plural form)."""
    # Map species to plural category names
    category_map = {
        'Alfalfa': 'alfalfas',
        'Barley': 'barleys',
        'Bean': 'beans',
        'Cabbage': 'cabbages',
        'Faba beans': 'faba_beans',
        'Grassland': 'grasslands',
        'Maize': 'maizes',
        'Mix': 'mixes',
        'Mustard': 'mustards',
        'Oat': 'oats',
        'Onion': 'onions',
        'Pea': 'peas',
        'Pepper': 'peppers',
        'Potato': 'potatoes',
        'Radish': 'radishes',
        'Rapeseed': 'rapeseeds',
        'Raspberry': 'raspberries',
        'Rice': 'rices',
        'Sorghum': 'sorghums',
        'Sorrel': 'sorrels',
        'Soybean': 'soybeans',
        'Sugarbeet': 'sugarbeets',
        'Sunflower': 'sunflowers',
        'Tabacco': 'tobaccos',
        'Vetch': 'vetches',
        'Wheat': 'wheats'
    }
    return category_map.get(species, species.lower() + 's')

def read_dataset_csv(csv_path):
    """Read dataset CSV and organize by category."""
    data_by_category = defaultdict(list)
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            species = row['Species']
            if species in ['Species', 'Na'] or not species:
                continue
            
            image_name = row['Name']
            category = get_category_name(species)
            data_by_category[category].append({
                'image_name': image_name,
                'species': species,
                'split1': row.get('TVT-split1', 'Training'),
                'split2': row.get('TVT-split2', 'Training'),
                'split3': row.get('TVT-split3', 'Training'),
                'split4': row.get('TVT-split4', 'Training'),
                'split5': row.get('TVT-split5', 'Training')
            })
    
    return data_by_category

def create_csv_annotation(json_path, csv_path):
    """Create CSV annotation from JSON annotation file."""
    if not os.path.exists(json_path):
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        annotations = data.get('annotations', [])
        if not annotations:
            return False
        
        with open(csv_path, 'w', encoding='utf-8') as f:
            f.write('#item,x,y,width,height,label\n')
            for idx, ann in enumerate(annotations):
                bbox = ann.get('bbox', [0, 0, 0, 0])
                x, y, w, h = bbox
                category_id = ann.get('category_id', 1)
                f.write(f'{idx},{x},{y},{w},{h},{category_id}\n')
        
        return True
    except Exception as e:
        print(f"Error creating CSV for {json_path}: {e}")
        return False

def create_labelmap(category_dir, species_name):
    """Create labelmap.json for a category."""
    labelmap_path = os.path.join(category_dir, 'labelmap.json')
    labelmap = [
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
            "object_name": species_name.lower().replace(' ', '_')
        }
    ]
    
    with open(labelmap_path, 'w', encoding='utf-8') as f:
        json.dump(labelmap, f, indent=2, ensure_ascii=False)

def organize_dataset():
    """Main function to reorganize dataset."""
    root_dir = Path(__file__).parent.parent  # Go up from scripts/ to root
    csv_path = root_dir / 'data' / 'origin' / 'VegAnn_dataset.csv'
    images_dir = root_dir / 'data' / 'origin' / 'images'
    annotations_dir = root_dir / 'data' / 'origin' / 'annotations_original'
    
    # Read dataset CSV
    print("Reading dataset CSV...")
    data_by_category = read_dataset_csv(csv_path)
    print(f"Found {len(data_by_category)} categories")
    
    # Create directory structure for each category
    for category, items in data_by_category.items():
        print(f"\nProcessing category: {category} ({len(items)} images)")
        
        # Create category directories
        category_dir = root_dir / category
        for subdir in ['csv', 'json', 'images', 'segmentations', 'sets']:
            (category_dir / subdir).mkdir(parents=True, exist_ok=True)
        
        # Get species name (singular form)
        species_name = items[0]['species']
        
        # Create labelmap.json
        create_labelmap(category_dir, species_name)
        
        # Organize images, JSON annotations, and segmentation masks
        train_images = []
        val_images = []
        test_images = []
        all_images = []
        
        for item in items:
            image_name = item['image_name']
            image_stem = Path(image_name).stem
            
            # Copy image
            src_image = images_dir / image_name
            if src_image.exists():
                dst_image = category_dir / 'images' / image_name
                shutil.copy2(src_image, dst_image)
            
            # Copy JSON annotation
            src_json = images_dir / f"{image_stem}.json"
            if src_json.exists():
                dst_json = category_dir / 'json' / f"{image_stem}.json"
                shutil.copy2(src_json, dst_json)
                
                # Create CSV annotation
                csv_path_cat = category_dir / 'csv' / f"{image_stem}.csv"
                create_csv_annotation(src_json, csv_path_cat)
            
            # Copy segmentation mask
            src_mask = annotations_dir / image_name
            if src_mask.exists():
                dst_mask = category_dir / 'segmentations' / image_name
                shutil.copy2(src_mask, dst_mask)
            
            # Organize splits (use split1 as default)
            split = item['split1']
            all_images.append(image_stem)
            if split == 'Test':
                test_images.append(image_stem)
            elif split == 'Validation':
                val_images.append(image_stem)
            else:  # Training
                train_images.append(image_stem)
        
        # Write split files
        sets_dir = category_dir / 'sets'
        with open(sets_dir / 'train.txt', 'w') as f:
            f.write('\n'.join(train_images) + '\n')
        with open(sets_dir / 'val.txt', 'w') as f:
            f.write('\n'.join(val_images) + '\n')
        with open(sets_dir / 'test.txt', 'w') as f:
            f.write('\n'.join(test_images) + '\n')
        with open(sets_dir / 'all.txt', 'w') as f:
            f.write('\n'.join(all_images) + '\n')
        with open(sets_dir / 'train_val.txt', 'w') as f:
            f.write('\n'.join(train_images + val_images) + '\n')
        
        print(f"  - Created {len(train_images)} train, {len(val_images)} val, {len(test_images)} test images")
    
    print("\nDataset reorganization completed!")

if __name__ == '__main__':
    organize_dataset()


