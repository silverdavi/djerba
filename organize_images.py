#!/usr/bin/env python3
"""
Image Organization System
=========================
Organizes recipe images with an index system and archives old images.

Creates:
- data/images/index.json - Index mapping recipe_id to image paths
- data/images/archive/ - Old images moved here
- data/images/current/ - Current active images (organized by recipe_id)
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def create_image_index(recipes_dir: Path, images_dir: Path) -> Dict:
    """
    Create an index mapping recipe IDs to their image files.
    
    Args:
        recipes_dir: Directory containing recipe JSON files
        images_dir: Directory containing generated images
        
    Returns:
        Dict mapping recipe_id -> image info
    """
    index = {}
    generated_dir = images_dir / "generated"
    
    # Get all recipe files
    recipe_files = sorted(recipes_dir.glob("*.json"))
    
    for recipe_file in recipe_files:
        try:
            with open(recipe_file, 'r', encoding='utf-8') as f:
                recipe = json.load(f)
            
            recipe_id = recipe.get('id', recipe_file.stem)
            
            # Look for dish image
            dish_image = generated_dir / f"{recipe_id}_dish.png"
            ingredients_image = generated_dir / f"{recipe_id}_ingredients.png"
            
            image_info = {
                "recipe_id": recipe_id,
                "dish_name": recipe.get('name', {}).get('en', recipe_id) if isinstance(recipe.get('name'), dict) else str(recipe.get('name', recipe_id)),
                "dish_image": f"{recipe_id}_dish.png" if dish_image.exists() else None,
                "ingredients_image": f"{recipe_id}_ingredients.png" if ingredients_image.exists() else None,
                "last_updated": datetime.now().isoformat()
            }
            
            index[recipe_id] = image_info
            
        except Exception as e:
            print(f"⚠️  Error processing {recipe_file.name}: {e}")
    
    return index


def archive_old_images(images_dir: Path, index: Dict) -> None:
    """
    Move old images (not matching current naming) to archive.
    
    Args:
        images_dir: Base images directory
        index: Current image index
    """
    generated_dir = images_dir / "generated"
    archive_dir = images_dir / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all current recipe IDs from index
    current_ids = set(index.keys())
    
    # Find images that don't match current naming convention
    all_images = list(generated_dir.glob("*.png"))
    archived_count = 0
    
    for image_path in all_images:
        image_name = image_path.name
        
        # Check if it matches current naming (recipe_id_dish.png or recipe_id_ingredients.png)
        is_current = False
        for recipe_id in current_ids:
            if image_name == f"{recipe_id}_dish.png" or image_name == f"{recipe_id}_ingredients.png":
                is_current = True
                break
        
        # Also check old naming (recipe_id.png)
        if not is_current:
            for recipe_id in current_ids:
                if image_name == f"{recipe_id}.png":
                    is_current = True
                    break
        
        # Archive if not current
        if not is_current:
            archive_path = archive_dir / image_name
            # Handle duplicates in archive
            if archive_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                archive_path = archive_dir / f"{image_path.stem}_{timestamp}{image_path.suffix}"
            
            shutil.move(str(image_path), str(archive_path))
            archived_count += 1
            print(f"📦 Archived: {image_name} -> {archive_path.name}")
    
    if archived_count > 0:
        print(f"\n✅ Archived {archived_count} old image(s)")
    else:
        print("✅ No old images to archive")


def organize_current_images(images_dir: Path, index: Dict) -> None:
    """
    Organize current images into a structured directory.
    
    Args:
        images_dir: Base images directory
        index: Current image index
    """
    generated_dir = images_dir / "generated"
    current_dir = images_dir / "current"
    current_dir.mkdir(parents=True, exist_ok=True)
    
    organized_count = 0
    
    for recipe_id, image_info in index.items():
        recipe_dir = current_dir / recipe_id
        recipe_dir.mkdir(exist_ok=True)
        
        # Move dish image if exists
        if image_info.get("dish_image"):
            source = generated_dir / image_info["dish_image"]
            if source.exists():
                dest = recipe_dir / "dish.png"
                if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
                    shutil.copy2(str(source), str(dest))
                    organized_count += 1
        
        # Move ingredients image if exists
        if image_info.get("ingredients_image"):
            source = generated_dir / image_info["ingredients_image"]
            if source.exists():
                dest = recipe_dir / "ingredients.png"
                if not dest.exists() or source.stat().st_mtime > dest.stat().st_mtime:
                    shutil.copy2(str(source), str(dest))
                    organized_count += 1
    
    print(f"✅ Organized {organized_count} image(s) into current/")


def main():
    """Main organization function."""
    print("=" * 60)
    print("📁 Image Organization System")
    print("=" * 60)
    print()
    
    root = Path(__file__).parent
    recipes_dir = root / "data" / "recipes_multilingual"
    images_dir = root / "data" / "images"
    
    if not recipes_dir.exists():
        print(f"❌ Recipes directory not found: {recipes_dir}")
        return
    
    # Create index
    print("📋 Creating image index...")
    index = create_image_index(recipes_dir, images_dir)
    
    # Save index
    index_file = images_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Index created: {len(index)} recipes")
    print(f"   Saved to: {index_file}")
    print()
    
    # Archive old images
    print("📦 Archiving old images...")
    archive_old_images(images_dir, index)
    print()
    
    # Organize current images
    print("🗂️  Organizing current images...")
    organize_current_images(images_dir, index)
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Indexed: {len(index)} recipes")
    print(f"✅ Index file: {index_file}")
    print(f"✅ Archive: {images_dir / 'archive'}")
    print(f"✅ Organized: {images_dir / 'current'}")
    print()
    print("✨ Organization complete!")
    print()
    print("Usage in build.py:")
    print("  from pathlib import Path")
    print("  import json")
    print("  index = json.load(open('data/images/index.json'))")
    print("  image_path = Path('data/images/current') / recipe_id / 'dish.png'")


if __name__ == "__main__":
    main()

