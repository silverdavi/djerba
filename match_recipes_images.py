#!/usr/bin/env python3
"""
Match multilingual recipes with existing images.
Creates an index showing which recipes have images and which are missing.
"""

import json
import os
import re
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual_v2")
IMAGES_DIR = Path("data/images/current")
CANONICAL_DIR = Path("data/recipes_canonical")

# Manual overrides for tricky matches
MANUAL_MATCHES = {
    "artichokemushroomsstew": "004_artichoke_mushroom_stew",
    "shepherdpienorth_african": "081_shepherds_pie",
    "humus_salad": "018_hummus_salad",
    "hotfudgepudding_cake": "044_hot_fudge_cake",
    "nougatandpeanutcakemor_abergil": "065_nougat_peanut_cake",
    "chocolatepeanutbuddy_bars": "070_chocolate_peanut_bars",
    "veganfishchraime": "045_hraime",  # same image works
    "redstewedolives": "057_marqa_zeitoun",
    "dabikh_hagim": "087_tbikha_chagim",
    "tbikha_tomatem": "088_tbikhat_tmatem",
    "vegetablesoupfor_couscous": "027_couscous_soup",
    "yellow_meat": "049_lham_sfar",
    "greenbeanstomato_sauce": "050_loubia_khadra",
    "sfingh": "078_sfenj",  # duplicate
    "marmuma": "055_marmouma",  # duplicate
    "shlomitperldressing": "082_shlomit_dressing",
    "shakshukacaramelizedonion_sausage": "066_ojja_merguez",
    "binasthicksourspicysoup": "046_hsou",  # duplicate recipe
    "shlomit_perl_dressing": "074_salad_dressing",
    "adafinawheatside_dish": "092_wheat_berries",
}

# Explicitly exclude wrong matches
EXCLUDE_MATCHES = {
    "bakedpotatolevivot": ["076_assida"],  # Levivot != Assida
}

def normalize_name(name):
    """Normalize a name for matching."""
    name = name.lower()
    name = re.sub(r'[_\-\s]+', '', name)
    # Remove numbers at start
    name = re.sub(r'^\d+', '', name)
    return name

def get_recipe_info():
    """Get all recipes with their current image paths."""
    recipes = []
    for f in sorted(RECIPES_DIR.glob("*.json")):
        with open(f) as fp:
            data = json.load(fp)
        
        # Also check canonical for Hebrew name
        canonical_path = CANONICAL_DIR / f"{f.stem}.json"
        hebrew_name = ""
        if canonical_path.exists():
            with open(canonical_path) as cp:
                cdata = json.load(cp)
                hebrew_name = cdata.get("name_hebrew", "")
        
        recipes.append({
            "file": f.stem,
            "name_en": data.get("name", {}).get("en", ""),
            "name_he": data.get("name", {}).get("he", hebrew_name),
            "current_image": data.get("image", ""),
            "id": data.get("id", "")
        })
    return recipes

def get_image_folders():
    """Get all image folders with their indices."""
    folders = []
    for d in sorted(IMAGES_DIR.iterdir()):
        if d.is_dir():
            # Parse index and name
            name = d.name
            parts = name.split("_", 1)
            if len(parts) == 2 and parts[0].isdigit():
                idx = int(parts[0])
                folder_name = parts[1]
            else:
                idx = 0
                folder_name = name
            
            # Check if dish.png exists
            has_dish = (d / "dish.png").exists()
            
            folders.append({
                "folder": d.name,
                "index": idx,
                "name": folder_name,
                "normalized": normalize_name(folder_name),
                "has_dish": has_dish,
                "path": f"images/current/{d.name}/dish.png"
            })
    return folders

def match_recipes_to_images(recipes, images):
    """Match recipes to images using fuzzy matching."""
    matches = []
    unmatched_recipes = []
    used_images = set()
    
    # Create lookup for images
    image_by_folder = {img["folder"]: img for img in images}
    image_by_normalized = {img["normalized"]: img for img in images}
    
    for recipe in recipes:
        matched_image = None
        match_method = None
        
        # 1. Check manual overrides first
        if recipe["file"] in MANUAL_MATCHES:
            folder = MANUAL_MATCHES[recipe["file"]]
            if folder in image_by_folder:
                matched_image = image_by_folder[folder]
                match_method = "manual"
        
        # 2. Check current image path (but respect exclusions)
        if not matched_image:
            current = recipe.get("current_image", "")
            if current:
                excluded = EXCLUDE_MATCHES.get(recipe["file"], [])
                for img in images:
                    if img["folder"] in current and img["folder"] not in excluded:
                        matched_image = img
                        match_method = "current_path"
                        break
        
        # 3. Try normalized name match
        if not matched_image:
            recipe_normalized = normalize_name(recipe["file"])
            if recipe_normalized in image_by_normalized:
                matched_image = image_by_normalized[recipe_normalized]
                match_method = "normalized"
        
        # 4. Try partial match
        if not matched_image:
            recipe_normalized = normalize_name(recipe["file"])
            for img in images:
                if (img["normalized"] in recipe_normalized or 
                    recipe_normalized in img["normalized"]):
                    matched_image = img
                    match_method = "partial"
                    break
        
        if matched_image:
            matches.append({
                "recipe": recipe,
                "image": matched_image,
                "method": match_method
            })
            used_images.add(matched_image["folder"])
        else:
            unmatched_recipes.append(recipe)
    
    # Find unused images
    unmatched_images = [img for img in images if img["folder"] not in used_images]
    
    return matches, unmatched_recipes, unmatched_images

def main():
    print("=" * 80)
    print("RECIPE-IMAGE MATCHING INDEX")
    print("=" * 80)
    
    recipes = get_recipe_info()
    images = get_image_folders()
    
    print(f"\n📋 Total multilingual recipes: {len(recipes)}")
    print(f"🖼️  Total image folders: {len(images)}")
    
    matches, unmatched_recipes, unmatched_images = match_recipes_to_images(recipes, images)
    
    print(f"\n✅ Matched: {len(matches)}")
    print(f"❌ Recipes without images: {len(unmatched_recipes)}")
    print(f"🖼️  Unused images: {len(unmatched_images)}")
    
    # Print matched recipes
    print("\n" + "=" * 80)
    print("MATCHED RECIPES")
    print("=" * 80)
    print(f"{'#':<4} {'Recipe File':<45} {'Image Folder':<30} {'Method':<12}")
    print("-" * 91)
    for i, m in enumerate(sorted(matches, key=lambda x: x['recipe']['file']), 1):
        print(f"{i:<4} {m['recipe']['file']:<45} {m['image']['folder']:<30} {m['method']:<12}")
    
    # Print unmatched recipes
    if unmatched_recipes:
        print("\n" + "=" * 80)
        print("❌ RECIPES WITHOUT IMAGES (need generation)")
        print("=" * 80)
        print(f"{'#':<4} {'Recipe File':<40} {'English Name':<40}")
        print("-" * 84)
        for i, r in enumerate(unmatched_recipes, 1):
            print(f"{i:<4} {r['file']:<40} {r['name_en'][:38]:<40}")
    
    # Print unused images
    if unmatched_images:
        print("\n" + "=" * 80)
        print("🖼️  UNUSED IMAGES (no matching recipe)")
        print("=" * 80)
        for img in unmatched_images:
            print(f"  {img['folder']}")
    
    # Save to JSON for reference
    output = {
        "summary": {
            "total_recipes": len(recipes),
            "total_images": len(images),
            "matched": len(matches),
            "recipes_without_images": len(unmatched_recipes),
            "unused_images": len(unmatched_images)
        },
        "matches": [{"recipe": m["recipe"]["file"], "image": m["image"]["folder"], "method": m["method"]} 
                    for m in sorted(matches, key=lambda x: x['recipe']['file'])],
        "unmatched_recipes": [{"file": r["file"], "name_en": r["name_en"], "name_he": r["name_he"]} 
                              for r in unmatched_recipes],
        "unused_images": [img["folder"] for img in unmatched_images]
    }
    
    with open("recipe_image_index.json", "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Index saved to: recipe_image_index.json")

if __name__ == "__main__":
    main()
