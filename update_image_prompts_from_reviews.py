#!/usr/bin/env python3
"""
Update Image Prompts Based on Latest Reviews
Reads reviews.json and updates image_prompt fields for recipes needing regeneration.
"""

import json
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual")
REVIEWS_FILE = Path("image_reviewer/reviews.json")

# Updated prompts based on latest review feedback
UPDATED_PROMPTS = {
    "002_admeshushah": """Create a photograph of Admeshushah - cooked pepper dish.

CRITICAL REQUIREMENTS:
- LESS peppers visible
- MORE WET (saucy/steamy appearance)
- MORE tomatoes visible
- Peppers should be COOKED and SOFT
- Rich, saucy appearance

Professional food photography, natural light, cookbook quality.""",

    "004_artichoke_mushroom_stew": """Create a photograph of Artichoke and Mushroom Stew.

CRITICAL REQUIREMENTS:
- NO carrots
- SMALLER artichokes
- YELLOW/GREEN sauce (not brown!)
- Baby portobello mushrooms
- Minimal or no tofu
- Light, fresh colored sauce

Professional food photography, natural light, cookbook quality.""",

    "012_brodo": """Create a photograph of Brodo - vegetable soup.

CRITICAL: This should be MORE SOUP than stew - liquidy, brothy appearance!

Show:
- Light, clear or slightly colored broth
- Vegetables visible in the soup
- Soup consistency (not thick stew)
- Traditional soup bowl
- Minimal tofu

Professional food photography, natural light.""",

    "013_bsisa": """Create a photograph of Bsisa - traditional semolina powder.

CRITICAL: Should NOT show visible oil - it's a powder mixture!

Show:
- Fine powder mixture in a bowl
- Golden-brown semolina powder
- Spices mixed in
- Powder texture (like flour)
- NO visible oil pools or droplets
- Traditional serving bowl

Professional food photography, natural light.""",

    "027_couscous_soup": """Create a photograph of Couscous Soup.

CRITICAL REQUIREMENTS:
- Focus on the SOUP with VEGETABLES prominently visible
- Couscous grains should be in the BACKGROUND (not the main focus)
- Rich soup with vegetables (carrots, zucchini, etc.)
- Soup consistency
- Minimal tofu

Professional food photography, natural light.""",

    "029_dabikh": """Create a photograph of Dabikh - holiday stew.

CRITICAL REQUIREMENTS:
- LESS brown color
- MORE GREENS visible (green onion leaves, dill)
- Fresh green herbs prominent
- NO raisins
- Lighter, fresher appearance
- Traditional serving dish

Professional food photography, natural light.""",

    "034_fricasse": """Create a photograph of Fricasse - Tunisian filled bun.

CRITICAL: This is NOT a burrito! It's a HALF-CUT BUN filled with ingredients!

Show:
- Round bun cut in HALF (like a sandwich bun)
- Filling visible inside the bun
- Fried/golden bun exterior
- Served as individual filled buns
- NOT wrapped like a burrito

Professional food photography, appetizing.""",

    "036_granola_cookies": """Create a photograph of Granola Cookies.

CRITICAL REQUIREMENTS:
- Granola should be BAKED (toasted, golden), NOT raw
- NO pumpkin seeds
- Round, rustic cookies
- Golden-brown baked color
- Visible oats and baked granola pieces

Professional food photography, warm bakery lighting.""",

    "048_kuklot": """Create a photograph of Kuklot - semolina spheres.

CRITICAL: They are NOT gray-gray! They should be BROWNISH LIGHT balls!

Show:
- Round BROWNISH-LIGHT colored semolina spheres
- Made from semolina with oil and spices
- Light brown/tan color (not gray)
- Individual spheres on a plate
- NO soup, NO liquid

Professional food photography, natural light.""",

    "053_mahshi": """Create a photograph of Mahshi - stuffed vegetables.

CRITICAL REQUIREMENTS:
- Vegetables need to be MORE COOKED (soft, tender)
- In LIGHT RED SAUCE (not dark)
- Whole vegetables (zucchini, peppers) stuffed and cooked
- Stuffing visible at the ends
- Light tomato-based sauce

Professional food photography, natural light.""",

    "055_marmouma": """Create a photograph of Marmouma.

CRITICAL REQUIREMENTS:
- RED PEPPERS should be SLICED (not whole)
- Tomatoes, garlic, and sliced peppers
- Cooked for many hours with paprika and kosher salt
- Rich, stewed appearance
- All ingredients well-cooked and integrated

Professional food photography, natural light.""",

    "057_marqa_zeitoun": """Create a photograph of Marqa Zeitoun - olive stew.

CRITICAL REQUIREMENTS:
- OLIVES should be GREEN (not black)
- NO lemon slice
- Pitted green olives in red sauce
- Simple, traditional appearance
- NO meat or meat alternative

Professional food photography, natural light.""",

    "059_mhamsa": """Create a photograph of Mhamsa - pearl pasta dish.

CRITICAL: NO meat! Just the PTITIM (pearl pasta)!

Show:
- Pearl pasta (mhamsa/ptitim) as the main focus
- NO meat, NO protein visible
- Just the pasta with sauce/seasoning
- Traditional appearance
- Served in appropriate dish

Professional food photography, natural light.""",

    "069_pastel": """Create a photograph of Pastel.

CRITICAL REQUIREMENTS:
- NO eggs visible
- NO olives
- TOP should be CRISP MASHED POTATO
- Golden-brown crispy potato top
- Baked appearance
- Traditional casserole dish

Professional food photography, appetizing golden color.""",

    "081_shepherds_pie": """Create a photograph of Shepherd's Pie.

CRITICAL REQUIREMENTS:
- NO peas and carrots
- Golden-brown mashed potato top
- Top should have browned, meat-like appearance
- Rich filling visible underneath
- Served in baking dish
- Comfort food appearance

Professional food photography, warm lighting.""",

    "083_shmid": """Create a photograph of Shmid - semolina soup.

CRITICAL: NO vegetables! It's just a SOUPY/STEW of semolina!

Show:
- Semolina cooked in paprika, oil, and water
- Soupy/stew consistency
- Rich red-orange color from paprika
- NO vegetables visible
- Simple, traditional soup
- Soup bowl

Professional food photography, natural light.""",

    "087_tbikha_chagim": """Create a photograph of Tbikha Chagim.

CRITICAL: The color should be a TINY BIT GREENER!

Show:
- Stew with slightly greenish tint
- Herbs should be COOKED (not raw)
- A bit more watery (soupier consistency)
- Traditional stew appearance
- Less tofu

Professional food photography, natural light.""",

    "093_yoyo": """Create a photograph of Yoyo - sweet pastry.

CRITICAL: They should have a HOLE in the center!

Show:
- Round pastries with HOLE in the center (like donuts)
- SHINY SUGAR SYRUP glaze (not powdered sugar)
- Glossy, syrupy appearance
- Traditional sweet pastry look

Professional food photography, appetizing."""
}


def load_recipe(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_recipe(path: Path, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("Updating Image Prompts from Reviews")
    print("=" * 60)
    print()
    
    # Load reviews to see what needs updating
    if REVIEWS_FILE.exists():
        with open(REVIEWS_FILE, 'r') as f:
            reviews = json.load(f)
    else:
        reviews = {}
    
    modified_count = 0
    not_found = []
    
    for recipe_id, prompt in UPDATED_PROMPTS.items():
        recipe_path = RECIPES_DIR / f"{recipe_id}.json"
        
        if not recipe_path.exists():
            not_found.append(recipe_id)
            print(f"  ⚠️  Recipe not found: {recipe_id}")
            continue
        
        recipe = load_recipe(recipe_path)
        
        # Update the image_prompt
        recipe['image_prompt'] = prompt
        save_recipe(recipe_path, recipe)
        
        # Show review notes if available
        review_notes = reviews.get(recipe_id, {}).get('notes', '')
        if review_notes:
            print(f"  ✓ Updated: {recipe_id}")
            print(f"    Notes: {review_notes[:60]}...")
        else:
            print(f"  ✓ Updated: {recipe_id}")
        
        modified_count += 1
    
    print()
    print("=" * 60)
    print(f"✓ Updated {modified_count} recipes with new image prompts")
    
    if not_found:
        print(f"⚠️  {len(not_found)} recipes not found: {', '.join(not_found)}")
    
    print()
    print("Next step: Regenerate images")
    print("  python regenerate_all_images.py")
    print()


if __name__ == "__main__":
    main()

