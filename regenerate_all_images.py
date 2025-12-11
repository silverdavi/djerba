#!/usr/bin/env python3
"""
Regenerate All Images with Custom Prompts - PARALLEL VERSION

This script finds all recipes with image_prompt fields and regenerates their images
using 30 parallel workers for fast processing.
"""

import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from generate_cookbook_images import CookbookImageGenerator

RECIPES_DIR = Path("data/recipes_multilingual")
NUM_WORKERS = 30

def generate_single_recipe(recipe_path: Path, recipe_data: dict) -> tuple:
    """
    Generate image for a single recipe.
    Designed to be called in parallel.
    
    Returns:
        Tuple of (recipe_id, success, message)
    """
    try:
        recipe_id = recipe_data.get('id', recipe_path.stem)
        dish_name = recipe_data.get('name', {}).get('en', recipe_id)
        
        # Initialize generator (each thread gets its own)
        gen = CookbookImageGenerator()
        
        # Generate dish image only
        results = gen.generate_recipe_images(
            recipe_data,
            generate_dish=True,
            generate_ingredients=False
        )
        
        if 'dish' in results:
            return (recipe_id, True, f"✓ Generated: {dish_name}")
        else:
            return (recipe_id, False, "No dish image generated")
            
    except Exception as e:
        recipe_id = recipe_data.get('id', recipe_path.stem) if 'recipe_data' in locals() else recipe_path.stem
        return (recipe_id, False, f"Error: {e}")

def main():
    print("Regenerating Images for Recipes with Custom Prompts")
    print("=" * 60)
    print()
    
    # Find all recipes with image_prompt
    recipes_to_regenerate = []
    for recipe_path in sorted(RECIPES_DIR.glob("*.json")):
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        if 'image_prompt' in recipe:
            recipes_to_regenerate.append((recipe_path, recipe))
    
    print(f"Found {len(recipes_to_regenerate)} recipes with custom image_prompt")
    print(f"🚀 Starting generation with {NUM_WORKERS} parallel workers...")
    print()
    
    if not recipes_to_regenerate:
        print("No recipes found with image_prompt fields.")
        return
    
    start_time = time.time()
    success_count = 0
    error_count = 0
    failed_recipes = []
    
    # Process in parallel with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Submit all tasks
        future_to_recipe = {
            executor.submit(generate_single_recipe, recipe_path, recipe_data): recipe_path
            for recipe_path, recipe_data in recipes_to_regenerate
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
                error_count += 1
                failed_recipes.append((recipe_id, message))
                status = "❌"
            
            print(f"[{completed}/{len(recipes_to_regenerate)}] {status} {recipe_id}")
            if not success:
                print(f"         {message}")
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 60)
    print(f"✓ Successfully regenerated: {success_count}")
    if error_count > 0:
        print(f"⚠️  Errors: {error_count}")
        for recipe_id, error in failed_recipes:
            print(f"  - {recipe_id}: {error}")
    print(f"⏱️  Total time: {elapsed:.1f} seconds")
    print()


if __name__ == "__main__":
    main()

