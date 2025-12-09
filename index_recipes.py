#!/usr/bin/env python3
"""
Index Recipes and Images
=========================
Adds index numbers to recipe files and their corresponding images.

Renames:
- data/recipes_multilingual/adafina.json -> data/recipes_multilingual/001_adafina.json
- data/images/generated/adafina_dish.png -> data/images/generated/001_adafina_dish.png
- data/images/current/adafina/dish.png -> data/images/current/001_adafina/dish.png

Updates index.json to reflect new names.
"""

import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


def get_recipe_sort_key(recipe: dict) -> str:
    """
    Get sort key for recipe ordering.
    Uses English name if available, otherwise recipe ID.
    """
    name = recipe.get('name', {})
    if isinstance(name, dict):
        en_name = name.get('en', '')
        if en_name:
            return en_name.lower()
    return recipe.get('id', '').lower()


def load_all_recipes(recipes_dir: Path) -> List[Tuple[Path, dict]]:
    """Load all recipe files with their data."""
    recipes = []
    for recipe_file in sorted(recipes_dir.glob("*.json")):
        try:
            with open(recipe_file, 'r', encoding='utf-8') as f:
                recipe_data = json.load(f)
            recipes.append((recipe_file, recipe_data))
        except Exception as e:
            print(f"⚠️  Error loading {recipe_file.name}: {e}")
    return recipes


def generate_indexed_name(index: int, base_name: str, max_index: int = None) -> str:
    """
    Generate indexed filename.
    
    Args:
        index: 1-based index number
        base_name: Base name (e.g., "adafina")
        max_index: Maximum index (for padding calculation)
    
    Returns:
        Indexed name (e.g., "001_adafina")
    """
    if max_index is None:
        max_index = index
    
    # Calculate padding (3 digits for up to 999, 4 for 1000+)
    if max_index >= 1000:
        padding = 4
    else:
        padding = 3
    
    index_str = str(index).zfill(padding)
    return f"{index_str}_{base_name}"


def rename_recipe_file(recipe_file: Path, new_name: str) -> Path:
    """Rename a recipe file."""
    new_path = recipe_file.parent / f"{new_name}.json"
    if recipe_file != new_path:
        shutil.move(str(recipe_file), str(new_path))
        print(f"  📄 {recipe_file.name} -> {new_path.name}")
    return new_path


def rename_image_files(recipe_id: str, new_id: str, images_dir: Path) -> None:
    """
    Rename all image files for a recipe.
    
    Args:
        recipe_id: Old recipe ID
        new_id: New indexed recipe ID
        images_dir: Base images directory
    """
    generated_dir = images_dir / "generated"
    current_dir = images_dir / "current"
    
    # Rename in generated/
    old_dish = generated_dir / f"{recipe_id}_dish.png"
    new_dish = generated_dir / f"{new_id}_dish.png"
    if old_dish.exists() and old_dish != new_dish:
        shutil.move(str(old_dish), str(new_dish))
        print(f"  🖼️  {old_dish.name} -> {new_dish.name}")
    
    old_ingredients = generated_dir / f"{recipe_id}_ingredients.png"
    new_ingredients = generated_dir / f"{new_id}_ingredients.png"
    if old_ingredients.exists() and old_ingredients != new_ingredients:
        shutil.move(str(old_ingredients), str(new_ingredients))
        print(f"  🖼️  {old_ingredients.name} -> {new_ingredients.name}")
    
    # Rename in current/
    old_current_dir = current_dir / recipe_id
    new_current_dir = current_dir / new_id
    if old_current_dir.exists() and old_current_dir != new_current_dir:
        # Move entire directory
        shutil.move(str(old_current_dir), str(new_current_dir))
        print(f"  📁 {old_current_dir.name}/ -> {new_current_dir.name}/")
        
        # Rename files inside if needed
        for img_file in new_current_dir.glob("*.png"):
            # Files are already named dish.png and ingredients.png, no need to rename
            pass


def update_recipe_id_in_file(recipe_file: Path, new_id: str) -> None:
    """Update the recipe ID inside the JSON file."""
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe_data = json.load(f)
    
    recipe_data['id'] = new_id
    
    with open(recipe_file, 'w', encoding='utf-8') as f:
        json.dump(recipe_data, f, indent=2, ensure_ascii=False)


def create_new_index(recipes_dir: Path, images_dir: Path) -> Dict:
    """Create a new index with indexed recipe IDs."""
    index = {}
    generated_dir = images_dir / "generated"
    current_dir = images_dir / "current"
    
    # Get all recipe files (now with indices)
    recipe_files = sorted(recipes_dir.glob("*.json"))
    
    for recipe_file in recipe_files:
        try:
            with open(recipe_file, 'r', encoding='utf-8') as f:
                recipe = json.load(f)
            
            recipe_id = recipe.get('id', recipe_file.stem)
            
            # Extract base name (remove index prefix if present)
            if '_' in recipe_id and recipe_id[0].isdigit():
                base_name = '_'.join(recipe_id.split('_')[1:])
            else:
                base_name = recipe_id
            
            # Look for images
            dish_image = None
            ingredients_image = None
            
            # Check organized structure first
            organized_dish = current_dir / recipe_id / "dish.png"
            organized_ingredients = current_dir / recipe_id / "ingredients.png"
            
            if organized_dish.exists():
                dish_image = f"{recipe_id}/dish.png"
            elif (generated_dir / f"{recipe_id}_dish.png").exists():
                dish_image = f"{recipe_id}_dish.png"
            
            if organized_ingredients.exists():
                ingredients_image = f"{recipe_id}/ingredients.png"
            elif (generated_dir / f"{recipe_id}_ingredients.png").exists():
                ingredients_image = f"{recipe_id}_ingredients.png"
            
            image_info = {
                "recipe_id": recipe_id,
                "dish_name": recipe.get('name', {}).get('en', recipe_id) if isinstance(recipe.get('name'), dict) else str(recipe.get('name', recipe_id)),
                "dish_image": dish_image,
                "ingredients_image": ingredients_image,
                "last_updated": datetime.now().isoformat()
            }
            
            index[recipe_id] = image_info
            
        except Exception as e:
            print(f"⚠️  Error processing {recipe_file.name}: {e}")
    
    return index


def main():
    """Main indexing function."""
    print("=" * 60)
    print("📑 Recipe and Image Indexing System")
    print("=" * 60)
    print()
    
    root = Path(__file__).parent
    recipes_dir = root / "data" / "recipes_multilingual"
    images_dir = root / "data" / "images"
    
    if not recipes_dir.exists():
        print(f"❌ Recipes directory not found: {recipes_dir}")
        return
    
    # Load all recipes
    print("📋 Loading recipes...")
    recipes = load_all_recipes(recipes_dir)
    
    if not recipes:
        print("❌ No recipes found!")
        return
    
    # Sort by English name
    print("🔤 Sorting recipes by English name...")
    recipes.sort(key=lambda x: get_recipe_sort_key(x[1]))
    
    print(f"✅ Found {len(recipes)} recipes")
    print()
    
    # Create backup
    print("💾 Creating backup...")
    backup_dir = recipes_dir.parent / "recipes_multilingual_backup"
    if not backup_dir.exists():
        shutil.copytree(recipes_dir, backup_dir)
        print(f"✅ Backup created: {backup_dir}")
    else:
        print(f"⚠️  Backup already exists: {backup_dir}")
    print()
    
    # Calculate max index for padding
    max_index = len(recipes)
    
    # Rename recipes and images
    print("🔄 Renaming recipes and images...")
    print()
    
    rename_map = {}  # old_id -> new_id
    
    for index, (recipe_file, recipe_data) in enumerate(recipes, start=1):
        old_id = recipe_data.get('id', recipe_file.stem)
        
        # Extract base name (remove existing index if present)
        if '_' in old_id and old_id[0].isdigit():
            base_name = '_'.join(old_id.split('_')[1:])
        else:
            base_name = old_id
        
        # Generate new indexed name
        new_id = generate_indexed_name(index, base_name, max_index)
        rename_map[old_id] = new_id
        
        print(f"[{index}/{len(recipes)}] {old_id} -> {new_id}")
        
        # Rename recipe file
        new_recipe_file = rename_recipe_file(recipe_file, new_id)
        
        # Update ID inside JSON file
        update_recipe_id_in_file(new_recipe_file, new_id)
        
        # Rename image files
        rename_image_files(old_id, new_id, images_dir)
        print()
    
    # Create new index
    print("📇 Creating new image index...")
    new_index = create_new_index(recipes_dir, images_dir)
    
    # Save new index
    index_file = images_dir / "index.json"
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(new_index, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Index updated: {index_file}")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Indexed: {len(recipes)} recipes")
    print(f"✅ Backup: {backup_dir}")
    print(f"✅ Index file: {index_file}")
    print()
    print("✨ Indexing complete!")
    print()
    print("Example renamed files:")
    if rename_map:
        old_id, new_id = list(rename_map.items())[0]
        print(f"  Recipe: {old_id}.json -> {new_id}.json")
        print(f"  Image: {old_id}_dish.png -> {new_id}_dish.png")
        print(f"  Folder: {old_id}/ -> {new_id}/")


if __name__ == "__main__":
    main()

