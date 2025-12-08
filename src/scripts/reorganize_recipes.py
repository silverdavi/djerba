#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to reorganize recipes from individual markdown files 
into structured folders with processing pipeline
"""

import os
import shutil
import re
from pathlib import Path
from typing import List, Tuple

def extract_recipe_info(filename: str) -> Tuple[str, str]:
    """Extract recipe index and name from filename"""
    # Pattern: 01_מחמסה.md -> (01, מחמסה)
    match = re.match(r'(\d+)_(.+)\.md$', filename)
    if match:
        index = match.group(1)
        name = match.group(2)
        return index, name
    return None, None

def create_recipe_folder_structure(recipes_dir: Path, recipe_index: str, recipe_name: str):
    """Create the folder structure for a recipe"""
    folder_name = f"{recipe_index}_{recipe_name}"
    recipe_folder = recipes_dir / folder_name
    
    # Create main recipe folder
    recipe_folder.mkdir(exist_ok=True)
    
    # Create pipeline stage folders
    stages = [
        "1_original_hebrew",
        "2_cleaned_hebrew", 
        "3_translated_english",
        "4_enhanced_content",
        "5_final_formatted"
    ]
    
    for stage in stages:
        stage_folder = recipe_folder / stage
        stage_folder.mkdir(exist_ok=True)
    
    return recipe_folder

def reorganize_recipes():
    """Main function to reorganize recipes"""
    project_root = Path(__file__).parent.parent.parent
    recipes_dir = project_root / "recipes"
    
    if not recipes_dir.exists():
        print(f"Recipes directory not found: {recipes_dir}")
        return
    
    # Get all current recipe markdown files
    recipe_files = list(recipes_dir.glob("*.md"))
    recipe_files.sort()  # Maintain order
    
    print(f"Found {len(recipe_files)} recipe files to reorganize")
    
    # Create backup directory
    backup_dir = recipes_dir.parent / "recipes_backup"
    if not backup_dir.exists():
        print(f"Creating backup at: {backup_dir}")
        shutil.copytree(recipes_dir, backup_dir)
    
    processed = 0
    for recipe_file in recipe_files:
        try:
            # Extract recipe info
            index, name = extract_recipe_info(recipe_file.name)
            if not index or not name:
                print(f"Skipping file with unexpected format: {recipe_file.name}")
                continue
            
            print(f"Processing: {recipe_file.name} -> {index}_{name}")
            
            # Create folder structure
            recipe_folder = create_recipe_folder_structure(recipes_dir, index, name)
            
            # Move original file to 1_original_hebrew folder
            original_file_path = recipe_folder / "1_original_hebrew" / "1_original_hebrew.md"
            shutil.move(str(recipe_file), str(original_file_path))
            
            # Create pipeline metadata file
            create_pipeline_metadata(recipe_folder, index, name)
            
            processed += 1
            
        except Exception as e:
            print(f"Error processing {recipe_file.name}: {e}")
    
    print(f"\nReorganization complete! Processed {processed} recipes.")
    print(f"Original files backed up to: {backup_dir}")
    print(f"\nNew structure:")
    show_new_structure(recipes_dir)

def create_pipeline_metadata(recipe_folder: Path, index: str, name: str):
    """Create metadata file for the recipe pipeline"""
    metadata = {
        "recipe_id": f"{index}_{name}",
        "index": index,
        "name": name,
        "pipeline_status": {
            "1_original_hebrew": "completed",
            "2_cleaned_hebrew": "pending",
            "3_translated_english": "pending", 
            "4_enhanced_content": "pending",
            "5_final_formatted": "pending"
        },
        "processing_notes": []
    }
    
    import json
    metadata_file = recipe_folder / "pipeline_metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

def show_new_structure(recipes_dir: Path):
    """Show the new directory structure"""
    recipe_folders = [d for d in recipes_dir.iterdir() if d.is_dir()]
    recipe_folders.sort()
    
    for i, folder in enumerate(recipe_folders[:3]):  # Show first 3 as examples
        print(f"  {folder.name}/")
        for subfolder in sorted(folder.iterdir()):
            if subfolder.is_dir():
                print(f"    └── {subfolder.name}/")
                for file in sorted(subfolder.iterdir()):
                    print(f"        └── {file.name}")
    
    if len(recipe_folders) > 3:
        print(f"  ... and {len(recipe_folders) - 3} more recipe folders")

def check_current_structure():
    """Check current recipe directory structure"""
    project_root = Path(__file__).parent.parent.parent
    recipes_dir = project_root / "recipes"
    
    print("Current recipes directory structure:")
    if recipes_dir.exists():
        files = list(recipes_dir.glob("*"))
        files.sort()
        
        md_files = [f for f in files if f.suffix == '.md']
        folders = [f for f in files if f.is_dir()]
        
        print(f"  Markdown files: {len(md_files)}")
        print(f"  Folders: {len(folders)}")
        
        if md_files:
            print("  Sample files:")
            for file in md_files[:5]:
                print(f"    - {file.name}")
        
        return len(md_files) > 0  # True if needs reorganization
    else:
        print("  Directory not found!")
        return False

if __name__ == "__main__":
    print("Recipe Reorganization Script")
    print("=" * 50)
    
    needs_reorganization = check_current_structure()
    
    if needs_reorganization:
        print("\nDo you want to reorganize recipes into pipeline folders? (y/n): ", end="")
        response = input().lower().strip()
        
        if response in ['y', 'yes']:
            reorganize_recipes()
        else:
            print("Reorganization cancelled.")
    else:
        print("No markdown files found to reorganize.") 