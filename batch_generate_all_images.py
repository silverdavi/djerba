#!/usr/bin/env python3
"""
Batch Image Generator - Parallel Processing
============================================
Regenerates all recipe images using the research-enhanced system.
Uses 30 parallel workers for fast processing.

Usage:
    python batch_generate_all_images.py
"""

import json
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Tuple
import time

from generate_cookbook_images import CookbookImageGenerator


def generate_single_recipe(recipe_path: str) -> Tuple[str, bool, str]:
    """
    Generate image for a single recipe.
    Designed to be called in parallel.
    
    Args:
        recipe_path: Path to recipe JSON file
        
    Returns:
        Tuple of (recipe_id, success, message)
    """
    try:
        recipe_path_obj = Path(recipe_path)
        with open(recipe_path_obj, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get('id', recipe_path_obj.stem)
        name = recipe.get('name', {})
        if isinstance(name, dict):
            dish_name = name.get('en', recipe_id)
        else:
            dish_name = str(name)
        
        # Initialize generator (each process gets its own)
        gen = CookbookImageGenerator()
        
        # Generate dish image only (faster, ingredients can be done separately if needed)
        gen.generate_recipe_images(recipe, generate_dish=True, generate_ingredients=False)
        
        return (recipe_id, True, f"✅ {dish_name}")
        
    except Exception as e:
        return (recipe_path_obj.stem if 'recipe_path_obj' in locals() else recipe_path, False, f"❌ Error: {e}")


def main():
    """Main batch generation function."""
    print("=" * 60)
    print("🍳 Batch Image Generator - Research-Enhanced")
    print("=" * 60)
    print()
    
    # Get all recipe files
    recipes_dir = Path(__file__).parent / "data" / "recipes_multilingual"
    recipe_files = sorted(recipes_dir.glob("*.json"))
    
    if not recipe_files:
        print("❌ No recipe files found in data/recipes_multilingual/")
        sys.exit(1)
    
    print(f"📚 Found {len(recipe_files)} recipes")
    print(f"🚀 Starting generation with 30 parallel workers...")
    print()
    
    start_time = time.time()
    success_count = 0
    failed_count = 0
    failed_recipes = []
    
    # Use ThreadPoolExecutor for I/O-bound API calls (better for API rate limits)
    with ThreadPoolExecutor(max_workers=30) as executor:
        # Submit all tasks
        future_to_recipe = {
            executor.submit(generate_single_recipe, str(recipe_file)): recipe_file
            for recipe_file in recipe_files
        }
        
        # Process results as they complete
        completed = 0
        for future in as_completed(future_to_recipe):
            completed += 1
            recipe_id, success, message = future.result()
            
            if success:
                success_count += 1
                status = "✅"
            else:
                failed_count += 1
                failed_recipes.append((recipe_id, message))
                status = "❌"
            
            # Show progress
            print(f"[{completed}/{len(recipe_files)}] {status} {recipe_id}")
            if not success:
                print(f"         {message}")
    
    elapsed = time.time() - start_time
    
    # Summary
    print()
    print("=" * 60)
    print("📊 GENERATION SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully generated: {success_count}/{len(recipe_files)} images")
    print(f"❌ Failed: {failed_count}/{len(recipe_files)}")
    print(f"⏱️  Total time: {elapsed:.1f} seconds")
    print(f"⚡ Average: {elapsed/len(recipe_files):.1f} seconds per recipe")
    
    if failed_recipes:
        print()
        print("Failed recipes:")
        for recipe_id, error in failed_recipes:
            print(f"  - {recipe_id}: {error}")
    
    print()
    print("=" * 60)
    print("✨ Batch generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

