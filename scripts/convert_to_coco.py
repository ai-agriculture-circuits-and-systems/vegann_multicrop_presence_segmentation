#!/usr/bin/env python3
"""
Convert CSV annotations to COCO format for VegAnn Multicrop Presence Segmentation dataset.
"""

import os
import json
import csv
import argparse
from pathlib import Path
from PIL import Image
import random

def load_labelmap(labelmap_path):
    """Load labelmap.json"""
    with open(labelmap_path, 'r', encoding='utf-8') as f:
        labelmap = json.load(f)
    return {item['object_id']: item['object_name'] for item in labelmap}

def parse_csv(csv_path):
    """Parse CSV annotation file"""
    annotations = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip comment lines
            if row.get('#item', '').startswith('#'):
                continue
            try:
                item = int(row.get('#item', 0))
                x = float(row.get('x', 0))
                y = float(row.get('y', 0))
                width = float(row.get('width', row.get('w', row.get('dx', 0))))
                height = float(row.get('height', row.get('h', row.get('dy', 0))))
                label = int(row.get('label', row.get('class', row.get('category_id', 1))))
                annotations.append({
                    'item': item,
                    'bbox': [x, y, width, height],
                    'label': label
                })
            except (ValueError, KeyError) as e:
                continue
    return annotations

def get_image_info(image_path):
    """Get image dimensions"""
    try:
        with Image.open(image_path) as img:
            return img.size
    except Exception:
        return (512, 512)  # Default

def get_all_categories(root_dir):
    """Get all category directories"""
    root = Path(root_dir)
    categories = []
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in ['annotations', 'scripts', 'images', 'data', 'docs', 'extra']:
            # Check if it has the required structure
            if (item / 'images').exists() and (item / 'csv').exists():
                categories.append(item.name)
    return sorted(categories)

def convert_to_coco(root_dir, output_dir, categories=None, splits=None, combined=False):
    """Convert CSV annotations to COCO format"""
    root = Path(root_dir)
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    
    if categories is None:
        categories = get_all_categories(root)
    if splits is None:
        splits = ['train', 'val', 'test']
    
    # Build combined category mapping (for multi-category dataset)
    all_categories_map = {}
    category_id_counter = 1
    
    for category in categories:
        labelmap_path = root / category / 'labelmap.json'
        if labelmap_path.exists():
            labelmap = load_labelmap(labelmap_path)
            for obj_id, obj_name in sorted(labelmap.items()):
                if obj_id > 0:  # Skip background
                    if obj_name not in all_categories_map:
                        all_categories_map[obj_name] = category_id_counter
                        category_id_counter += 1
    
    # Build COCO categories list
    coco_categories = [{
        'id': 0,
        'name': 'background',
        'supercategory': 'background'
    }]
    for obj_name, cat_id in sorted(all_categories_map.items(), key=lambda x: x[1]):
        coco_categories.append({
            'id': cat_id,
            'name': obj_name,
            'supercategory': 'crop'
        })
    
    # Process each category and split
    all_coco_data = {}
    
    for category in categories:
        category_dir = root / category
        images_dir = category_dir / 'images'
        csv_dir = category_dir / 'csv'
        sets_dir = category_dir / 'sets'
        
        if not images_dir.exists():
            print(f"Warning: {images_dir} does not exist, skipping {category}")
            continue
        
        # Load category labelmap
        labelmap_path = category_dir / 'labelmap.json'
        if not labelmap_path.exists():
            print(f"Warning: {labelmap_path} does not exist, skipping {category}")
            continue
        
        category_labelmap = load_labelmap(labelmap_path)
        
        for split in splits:
            coco_data = {
                'info': {
                    'year': 2025,
                    'version': '1.0',
                    'description': f'VegAnn Multicrop Presence Segmentation {category} {split} split',
                    'url': 'https://zenodo.org/records/7636408'
                },
                'images': [],
                'annotations': [],
                'categories': coco_categories,
                'licenses': []
            }
            
            # Load split file
            split_file = sets_dir / f'{split}.txt'
            split_images = set()
            if split_file.exists():
                with open(split_file, 'r', encoding='utf-8') as f:
                    split_images = {line.strip() for line in f if line.strip()}
                print(f"Loaded {len(split_images)} images for {category}/{split}")
            else:
                print(f"Warning: Split file '{split_file}' does not exist, using all images")
            
            # Get images in this split
            if split_images:
                image_files = []
                for stem in split_images:
                    for ext in ['.jpg', '.png', '.jpeg', '.bmp']:
                        img_path = images_dir / f"{stem}{ext}"
                        if img_path.exists():
                            image_files.append(img_path)
                            break
                print(f"  Found {len(image_files)}/{len(split_images)} images for {category}/{split}")
            else:
                # If split file doesn't exist, use all images
                image_files = list(images_dir.glob('*.jpg'))
                image_files.extend(images_dir.glob('*.png'))
                image_files.extend(images_dir.glob('*.jpeg'))
                image_files.extend(images_dir.glob('*.bmp'))
                print(f"  No split file for {category}/{split}, using all {len(image_files)} images")
            
            # Process images
            image_id_map = {}
            annotation_id = 1
            
            for img_path in image_files:
                stem = img_path.stem
                
                # Check if in split (already filtered above, but double-check)
                if split_images and stem not in split_images:
                    continue
                
                # Get image info
                width, height = get_image_info(img_path)
                image_id = random.randint(1000000000, 9999999999)
                image_id_map[stem] = image_id
                
                coco_data['images'].append({
                    'id': image_id,
                    'file_name': f'{category}/images/{img_path.name}',
                    'width': width,
                    'height': height
                })
                
                # Load CSV annotations
                csv_path = csv_dir / f'{stem}.csv'
                if csv_path.exists():
                    annotations = parse_csv(csv_path)
                    for ann in annotations:
                        bbox = ann['bbox']
                        local_category_id = ann['label']
                        
                        # Map local category ID to global category ID
                        if local_category_id in category_labelmap:
                            obj_name = category_labelmap[local_category_id]
                            global_category_id = all_categories_map.get(obj_name, local_category_id)
                        else:
                            global_category_id = local_category_id
                        
                        coco_data['annotations'].append({
                            'id': annotation_id,
                            'image_id': image_id,
                            'category_id': global_category_id,
                            'bbox': bbox,
                            'area': bbox[2] * bbox[3],
                            'iscrowd': 0
                        })
                        annotation_id += 1
            
            # Save single category file
            output_file = output / f'{category}_instances_{split}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(coco_data, f, indent=2, ensure_ascii=False)
            print(f"Created {output_file}: {len(coco_data['images'])} images, {len(coco_data['annotations'])} annotations")
            
            if split not in all_coco_data:
                all_coco_data[split] = {
                    'info': {
                        'year': 2025,
                        'version': '1.0',
                        'description': f'VegAnn Multicrop Presence Segmentation combined {split} split',
                        'url': 'https://zenodo.org/records/7636408'
                    },
                    'images': [],
                    'annotations': [],
                    'categories': coco_categories,
                    'licenses': []
                }
            
            # Add to combined data
            all_coco_data[split]['images'].extend(coco_data['images'])
            all_coco_data[split]['annotations'].extend(coco_data['annotations'])
    
    # Create combined files if requested
    if combined:
        for split in splits:
            if split in all_coco_data:
                output_file = output / f'combined_instances_{split}.json'
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_coco_data[split], f, indent=2, ensure_ascii=False)
                print(f"Created {output_file}: {len(all_coco_data[split]['images'])} images, {len(all_coco_data[split]['annotations'])} annotations")

def main():
    parser = argparse.ArgumentParser(description='Convert CSV annotations to COCO format')
    parser.add_argument('--root', type=str, default='.', help='Dataset root directory')
    parser.add_argument('--out', type=str, default='annotations', help='Output directory')
    parser.add_argument('--categories', nargs='+', default=None, help='Categories to process (default: all)')
    parser.add_argument('--splits', nargs='+', default=['train', 'val', 'test'], help='Splits to process')
    parser.add_argument('--combined', action='store_true', help='Create combined COCO files')
    
    args = parser.parse_args()
    convert_to_coco(args.root, args.out, args.categories, args.splits, args.combined)

if __name__ == '__main__':
    main()





