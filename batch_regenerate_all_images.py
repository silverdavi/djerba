#!/usr/bin/env python3
"""
Batch Regenerate All Recipe Images
===================================
Regenerates all dish images with proper category detection.
Uses 40 parallel workers for fast processing.
"""

import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple
import time

# Import the image generator
from generate_cookbook_images import CookbookImageGenerator


def process_recipe(recipe_file: Path, gen: CookbookImageGenerator) -> Tuple[str, bool, str]:
    """
    Process a single recipe and generate its dish image.
    
    Returns:
        (recipe_id, success, error_message)
    """
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get('id', recipe_file.stem)
        name = recipe.get('name', {}).get('en', recipe_id) if isinstance(recipe.get('name'), dict) else str(recipe.get('name', recipe_id))
        
        # Generate dish image only (faster, ingredients images not needed)
        gen.generate_recipe_images(
            recipe, 
            generate_dish=True, 
            generate_ingredients=False
        )
        
        return (recipe_id, True, "")
        
    except Exception as e:
        return (recipe_file.stem, False, str(e))


def main():
    """Main batch processing function."""
    print("=" * 60)
    print("🖼️  Batch Image Regeneration")
    print("=" * 60)
    print()
    
    root = Path(__file__).parent
    recipes_dir = root / "data" / "recipes_multilingual"
    
    if not recipes_dir.exists():
        print(f"❌ Recipes directory not found: {recipes_dir}")
        return
    
    # Get all recipe files
    recipe_files = sorted(recipes_dir.glob("*.json"))
    
    if not recipe_files:
        print("❌ No recipe files found!")
        return
    
    print(f"📋 Found {len(recipe_files)} recipes to process")
    print(f"⚙️  Using 40 parallel workers")
    print()
    
    # Initialize generator (shared across threads)
    gen = CookbookImageGenerator()
    
    # Process with thread pool
    start_time = time.time()
    success_count = 0
    failed = []
    
    with ThreadPoolExecutor(max_workers=40) as executor:
        # Submit all tasks
        future_to_recipe = {
            executor.submit(process_recipe, recipe_file, gen): recipe_file
            for recipe_file in recipe_files
        }
        
        # Process results as they complete
        completed = 0
        for future in as_completed(future_to_recipe):
            completed += 1
            recipe_file = future_to_recipe[future]
            
            try:
                recipe_id, success, error = future.result()
                
                if success:
                    success_count += 1
                    print(f"[{completed}/{len(recipe_files)}] ✅ {recipe_id}")
                else:
                    failed.append((recipe_id, error))
                    print(f"[{completed}/{len(recipe_files)}] ❌ {recipe_id}: {error}")
                    
            except Exception as e:
                failed.append((recipe_file.stem, str(e)))
                print(f"[{completed}/{len(recipe_files)}] ❌ {recipe_file.stem}: {e}")
    
    elapsed = time.time() - start_time
    
    # Summary
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully generated: {success_count}/{len(recipe_files)} images")
    print(f"❌ Failed: {len(failed)}")
    print(f"⏱️  Total time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
    print()
    
    if failed:
        print("Failed recipes:")
        for recipe_id, error in failed:
            print(f"  - {recipe_id}: {error}")
        print()
    
    print("✨ Batch regeneration complete!")
    print()
    print("Next steps:")
    print("  1. Run: python organize_images.py")
    print("  2. Run: python gen_book/build.py")


if __name__ == "__main__":
    main()

