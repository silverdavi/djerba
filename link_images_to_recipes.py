#!/usr/bin/env python3
"""
Link Images to Canonical Recipes

Maps image directories in data/images/current/ to canonical recipes
and updates the image.filename field.
"""

import json
from pathlib import Path
from difflib import SequenceMatcher

CANONICAL_DIR = Path("data/recipes_canonical")
IMAGES_DIR = Path("data/images/current")

def similarity(a: str, b: str) -> float:
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def normalize_name(name: str) -> str:
    """Normalize a name for comparison."""
    # Remove common suffixes and prefixes
    name = name.lower()
    name = name.replace("_", " ").replace("-", " ")
    # Remove index prefix like "001_"
    parts = name.split()
    if parts and parts[0].isdigit():
        parts = parts[1:]
    return " ".join(parts)

def find_best_match(recipe_id: str, recipe_name: str, name_hebrew: str, image_dirs: list) -> tuple:
    """Find the best matching image directory for a recipe."""
    
    # Normalize recipe identifiers
    recipe_id_norm = normalize_name(recipe_id)
    recipe_name_norm = normalize_name(recipe_name) if recipe_name else ""
    
    best_match = None
    best_score = 0
    
    for img_dir in image_dirs:
        # Get just the name part (remove index)
        dir_name = img_dir.name
        dir_name_norm = normalize_name(dir_name)
        
        # Calculate similarity scores
        scores = []
        
        # Compare with recipe ID
        scores.append(similarity(recipe_id_norm, dir_name_norm))
        
        # Compare with recipe name parts
        if recipe_name_norm:
            for word in recipe_name_norm.split():
                if len(word) > 3:  # Skip short words
                    scores.append(similarity(word, dir_name_norm))
        
        # Check for exact substring match
        if recipe_id_norm in dir_name_norm or dir_name_norm in recipe_id_norm:
            scores.append(0.9)
        
        max_score = max(scores) if scores else 0
        
        if max_score > best_score:
            best_score = max_score
            best_match = img_dir
    
    return best_match, best_score

def main():
    # Get all image directories
    image_dirs = sorted([d for d in IMAGES_DIR.iterdir() if d.is_dir()])
    print(f"Found {len(image_dirs)} image directories")
    
    # Get all canonical recipes
    recipe_files = sorted([f for f in CANONICAL_DIR.glob("*.json")])
    print(f"Found {len(recipe_files)} canonical recipes")
    print()
    
    # Manual mappings for tricky cases
    manual_mappings = {
        "adamshusha": "002_admeshushah",
        "bshisha_bsisa": "008_beshisha",
        "bkaila_tunisian_stew": "010_bkaila",
        "brikot": "011_brik",
        "brodo_chicken_soup": "012_brodo",
        "charoset": "017_charoset",
        "humus_salad": "018_hummus_salad",
        "chocolate_balls": "020_chocolate_balls",
        "chocolate_cake": "021_chocolate_cake",
        "original_toll_house_chocolate_chip_cookies": "022_chocolate_chip_cookies",
        "chocolate_peanut_butter_muffins": "023_chocolate_peanut_butter_muffins",
        "cholent": "025_cholent",
        "homemade_couscous": "026_couscous",
        "vegetable_soup_for_couscous": "027_couscous_soup",
        "cujada": "028_cujada",
        "dwida": "031_dwida",
        "french_toast": "032_french_toast",
        "chicken_fricassee_stew": "033_fricassee_stew",
        "fricassee_rolls": "034_fricasse",
        "granola_cookies": "036_granola_cookies",
        "green_beans_tomato_sauce": "037_green_beans",
        "chraime_spicy_fish_stew": "045_hraime",
        "vegan_fish_chraime": "045_hraime",
        "kataa_soup": "047_ktaa",
        "kouklot_semolina_dumplings": "048_kuklot",
        "yellow_meat": "049_lham_sfar",
        "maakouda": "051_maakouda",
        "mahshi_stuffed_vegetables": "053_mahshi",
        "marmouma": "055_marmouma",
        "marmuma": "055_marmouma",
        "mhamsa": "059_mhamsa",
        "mocha_java_cake": "060_mocha_java_cake",
        "msiyar": "062_msiyer",
        "nazha_herb_omelet": "063_nazha",
        "nougat_and_peanut_cake_mor_abergil": "065_nougat_peanut_cake",
        "shakshuka_caramelized_onion_sausage": "066_ojja_merguez",
        "pancakes_efrat_shachor": "068_pancakes",
        "chocolate_peanut_buddy_bars": "070_chocolate_peanut_bars",
        "pizza": "072_pizza",
        "schnitzel": "075_schnitzel",
        "semolina_porridge": "077_semolina_porridge",
        "sfenj": "078_sfenj",
        "sfingh": "078_sfenj",
        "soy_shawarma": "080_shawarma",
        "shepherd_pie_north_african": "081_shepherds_pie",
        "shlomit_perl_dressing": "082_shlomit_dressing",
        "shmid": "083_shmid",
        "pancakes_soly": "084_pancakes_soly",
        "sour_dough_bread_soly": "085_sourdough_bread",
        "sufganiyot": "086_sufganiyot",
        "dabikh_hagim": "087_tbikha_chagim",
        "dabikh_hagim_1": "087_tbikha_chagim",
        "tbikha_tomatem": "088_tbikhat_tmatem",
        "tfina_stew": "090_tfina",
        "tirshi_pumpkin_salad": "091_tirshi",
        "adafina_wheat_side_dish": "092_wheat_berries",
        "yoyo_tunisian_doughnuts": "093_yoyo",
        "adafina": "001_adafina",
        "apple_crumble": "003_apple_crumble",
        "artichoke_mushrooms_stew": "004_artichoke_mushroom_stew",
        "banana_cake": "006_banana_cake",
        "banatage_stuffed_potato_croquettes": "007_banatage",
        "biscoti_judy": "009_biscotti",
        "bread": "041_khobz_dar",
        "binas_thick_sour_spicy_soup": "046_hsou",
        "hot_fudge_pudding_cake": "044_hot_fudge_cake",
        "honey_cake_lior_benmosheh": "042_honey_cake",
        "honey_cake_mami": "042_honey_cake",
        "vegan_caesar_dressing": "016_vegan_caesar",
        "red_stewed_olives": "057_marqa_zeitoun",
        "baked_potato_levivot": "076_assida",  # Might need adjustment
    }
    
    # Create image dir lookup by name
    img_dir_by_name = {d.name: d for d in image_dirs}
    
    matched = 0
    unmatched = []
    
    for recipe_file in recipe_files:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get("id", recipe_file.stem)
        recipe_name = recipe.get("name", "")
        name_hebrew = recipe.get("name_hebrew", "")
        
        # Check manual mapping first
        if recipe_id in manual_mappings:
            img_dir_name = manual_mappings[recipe_id]
            if img_dir_name in img_dir_by_name:
                img_dir = img_dir_by_name[img_dir_name]
                # Find image file
                img_file = img_dir / "dish.png"
                if img_file.exists():
                    relative_path = f"images/current/{img_dir.name}/dish.png"
                    recipe["image"] = {
                        "filename": relative_path,
                        "prompt": recipe.get("image", {}).get("prompt")
                    }
                    with open(recipe_file, 'w', encoding='utf-8') as f:
                        json.dump(recipe, f, ensure_ascii=False, indent=2)
                    print(f"✅ {recipe_id} → {img_dir.name}/dish.png")
                    matched += 1
                    continue
        
        # Try automatic matching
        best_match, score = find_best_match(recipe_id, recipe_name, name_hebrew, image_dirs)
        
        if best_match and score >= 0.6:
            img_file = best_match / "dish.png"
            if img_file.exists():
                relative_path = f"images/current/{best_match.name}/dish.png"
                recipe["image"] = {
                    "filename": relative_path,
                    "prompt": recipe.get("image", {}).get("prompt")
                }
                with open(recipe_file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, ensure_ascii=False, indent=2)
                print(f"✅ {recipe_id} → {best_match.name}/dish.png (score: {score:.2f})")
                matched += 1
            else:
                unmatched.append((recipe_id, f"No dish.png in {best_match.name}"))
        else:
            unmatched.append((recipe_id, f"Best match: {best_match.name if best_match else 'None'} (score: {score:.2f})"))
    
    print()
    print("=" * 60)
    print(f"✅ Matched: {matched}")
    print(f"❌ Unmatched: {len(unmatched)}")
    
    if unmatched:
        print("\nUnmatched recipes:")
        for recipe_id, reason in unmatched:
            print(f"  - {recipe_id}: {reason}")

if __name__ == "__main__":
    main()

