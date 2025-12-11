#!/usr/bin/env python3
"""
Remove Duplicate Recipes
Moves duplicate recipes and their images to archive folders.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
RECIPES_DIR = ROOT / "data" / "recipes_multilingual"
IMAGES_DIR = ROOT / "data" / "images" / "current"
REVIEWS_FILE = ROOT / "image_reviewer" / "reviews.json"
ARCHIVE_RECIPES = ROOT / "data" / "recipes_duplicates"
ARCHIVE_IMAGES = ROOT / "data" / "images" / "archive"

def load_reviews():
    if REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, 'r') as f:
            return json.load(f)
    return {}

def main():
    print("Removing Duplicate Recipes")
    print("=" * 50)
    print()
    
    reviews = load_reviews()
    duplicates = [k for k, v in reviews.items() if v.get('is_duplicate')]
    
    if not duplicates:
        print("No duplicates found to remove.")
        return
    
    print(f"Found {len(duplicates)} duplicates to remove:")
    for dup in sorted(duplicates):
        print(f"  - {dup}")
    print()
    
    # Create archive directories
    ARCHIVE_RECIPES.mkdir(exist_ok=True)
    ARCHIVE_IMAGES.mkdir(exist_ok=True)
    
    removed_recipes = []
    removed_images = []
    errors = []
    
    for recipe_id in sorted(duplicates):
        print(f"Processing: {recipe_id}")
        
        # Move recipe JSON
        recipe_path = RECIPES_DIR / f"{recipe_id}.json"
        if recipe_path.exists():
            try:
                archive_path = ARCHIVE_RECIPES / f"{recipe_id}.json"
                shutil.move(str(recipe_path), str(archive_path))
                removed_recipes.append(recipe_id)
                print(f"  ✓ Moved recipe JSON")
            except Exception as e:
                errors.append(f"{recipe_id} (recipe): {e}")
                print(f"  ❌ Error moving recipe: {e}")
        else:
            print(f"  ⚠️  Recipe JSON not found")
        
        # Move image folder
        image_path = IMAGES_DIR / recipe_id
        if image_path.exists():
            try:
                archive_image_path = ARCHIVE_IMAGES / recipe_id
                if archive_image_path.exists():
                    shutil.rmtree(str(archive_image_path))
                shutil.move(str(image_path), str(archive_image_path))
                removed_images.append(recipe_id)
                print(f"  ✓ Moved image folder")
            except Exception as e:
                errors.append(f"{recipe_id} (images): {e}")
                print(f"  ❌ Error moving images: {e}")
        else:
            print(f"  ⚠️  Image folder not found")
        
        print()
    
    print("=" * 50)
    print(f"✓ Removed {len(removed_recipes)} recipe JSONs")
    print(f"✓ Removed {len(removed_images)} image folders")
    
    if errors:
        print(f"\n⚠️  {len(errors)} errors:")
        for err in errors:
            print(f"  - {err}")
    
    print()
    print("Duplicates have been archived to:")
    print(f"  Recipes: {ARCHIVE_RECIPES}")
    print(f"  Images: {ARCHIVE_IMAGES}")

if __name__ == "__main__":
    main()

