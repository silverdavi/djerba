#!/usr/bin/env python3
"""
Reset Ratings for Regenerated Recipes

Resets ratings for recipes that have been regenerated (have image_prompt fields)
so they can be reviewed fresh in the image reviewer app.
"""

import json
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual")
REVIEWS_FILE = Path("image_reviewer/reviews.json")

def main():
    print("Resetting Ratings for Regenerated Recipes")
    print("=" * 60)
    print()
    
    # Load reviews
    if not REVIEWS_FILE.exists():
        print("No reviews file found. Nothing to reset.")
        return
    
    with open(REVIEWS_FILE, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    # Find recipes with image_prompt (regenerated ones)
    regenerated_ids = []
    for recipe_path in sorted(RECIPES_DIR.glob("*.json")):
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        if 'image_prompt' in recipe:
            recipe_id = recipe.get('id', recipe_path.stem)
            regenerated_ids.append(recipe_id)
    
    print(f"Found {len(regenerated_ids)} recipes with image_prompt (regenerated)")
    print()
    
    reset_count = 0
    for recipe_id in sorted(regenerated_ids):
        if recipe_id in reviews:
            old_rating = reviews[recipe_id].get('rating', 0)
            
            # Reset rating to 0, keep other fields (notes, needs_regen, is_duplicate)
            reviews[recipe_id]['rating'] = 0
            
            # Optionally clear needs_regen since we just regenerated
            # But keep it if user wants to mark for another regen
            # reviews[recipe_id]['needs_regen'] = False
            
            print(f"  ✓ Reset rating for {recipe_id} (was {old_rating})")
            reset_count += 1
    
    # Save updated reviews
    with open(REVIEWS_FILE, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)
    
    print()
    print("=" * 60)
    print(f"✓ Reset ratings for {reset_count} regenerated recipes")
    print()
    print("You can now review them fresh in the image reviewer app!")
    print()

if __name__ == "__main__":
    main()

