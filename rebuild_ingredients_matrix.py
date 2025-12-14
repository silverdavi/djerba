#!/usr/bin/env python3
"""
Rebuild the ingredients matrix from canonical recipes.
Maps recipe ingredients to available ingredient images.
"""

import json
import csv
import re
from pathlib import Path

CANONICAL_DIR = Path("data/recipes_canonical")
INGREDIENTS_DIR = Path("data/images/ingredients/final")
OUTPUT_FILE = Path("recipes_ingredients_matrix.csv")

def normalize_ingredient_name(name: str) -> str:
    """Normalize ingredient name for matching."""
    name = name.lower()
    # Remove parenthetical content for basic matching
    name = re.sub(r'\([^)]*\)', '', name)
    name = name.strip()
    # Remove common prefixes
    for prefix in ["fresh ", "dried ", "ground ", "chopped ", "minced ", "crushed "]:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name.strip()

def get_available_ingredients():
    """Get all available ingredient image files and their normalized names."""
    ingredients = {}
    for img in INGREDIENTS_DIR.glob("*.png"):
        # Convert filename to normalized name
        # "chickpea_flour_besan.png" -> ["chickpea flour", "besan"]
        base = img.stem.replace("_", " ")
        # Split on common separators
        parts = [p.strip() for p in base.split(" or ")]
        for part in parts:
            ingredients[part] = img.name
        # Also add the full name
        ingredients[base] = img.name
        # Also add individual words from the filename
        for word in base.split():
            if len(word) > 3:
                ingredients[word] = img.name
    return ingredients

def match_ingredient_to_image(ingredient_name: str, available: dict) -> str:
    """Match an ingredient name to an available image."""
    normalized = normalize_ingredient_name(ingredient_name)
    
    # Direct match
    if normalized in available:
        return available[normalized]
    
    # Check first word (main ingredient)
    first_word = normalized.split()[0] if normalized else ""
    if first_word and len(first_word) > 3 and first_word in available:
        return available[first_word]
    
    # Partial match - check if any available ingredient is contained in the name
    for avail_name, img_file in available.items():
        if len(avail_name) > 3 and (avail_name in normalized or normalized in avail_name):
            return img_file
    
    # Try individual words
    words = normalized.split()
    for word in words:
        if len(word) > 3 and word in available:
            return available[word]
    
    return None

def main():
    available_ingredients = get_available_ingredients()
    print(f"Found {len(available_ingredients)} ingredient mappings")
    
    # Get all ingredient names from images
    all_ingredient_files = sorted(set(available_ingredients.values()))
    ingredient_columns = [f.replace(".png", "").replace("_", " ").title() for f in all_ingredient_files]
    
    print(f"Ingredient columns: {len(ingredient_columns)}")
    
    # Build matrix
    rows = []
    
    for recipe_file in sorted(CANONICAL_DIR.glob("*.json")):
        with open(recipe_file) as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get("id", recipe_file.stem)
        recipe_name = recipe.get("name", recipe_id)
        
        # Get ingredients
        ingredients = recipe.get("ingredients", [])
        matched_files = set()
        
        for ing in ingredients:
            ing_name = ing.get("name", "")
            img_file = match_ingredient_to_image(ing_name, available_ingredients)
            if img_file:
                matched_files.add(img_file)
        
        # Build row with canonical ID
        row = [recipe_id, recipe_name]
        for img_file in all_ingredient_files:
            row.append("1" if img_file in matched_files else "0")
        
        rows.append((recipe_id, row, matched_files))
        
        # Also add rows with various ID normalizations for multilingual matching
        # 1. No underscores at all
        normalized_id = recipe_id.replace("_", "")
        if normalized_id != recipe_id:
            row_normalized = [normalized_id, recipe_name]
            for img_file in all_ingredient_files:
                row_normalized.append("1" if img_file in matched_files else "0")
            rows.append((normalized_id, row_normalized, matched_files))
        
        # 2. Partial underscores (keep last underscore before final word)
        # e.g., "adafina_wheat_side_dish" -> "adafinawheatside_dish"
        parts = recipe_id.split("_")
        if len(parts) > 2:
            partial_id = "".join(parts[:-1]) + "_" + parts[-1]
            if partial_id != recipe_id and partial_id != normalized_id:
                row_partial = [partial_id, recipe_name]
                for img_file in all_ingredient_files:
                    row_partial.append("1" if img_file in matched_files else "0")
                rows.append((partial_id, row_partial, matched_files))
        
        if matched_files:
            print(f"  {recipe_id}: matched {len(matched_files)} ingredients")
    
    # Write CSV
    header = ["recipe_id", "recipe_name"] + ingredient_columns
    
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for _, row, _ in rows:
            writer.writerow(row)
    
    print(f"\n✅ Wrote {len(rows)} recipes to {OUTPUT_FILE}")
    print(f"   Columns: {len(header)}")

if __name__ == "__main__":
    main()

