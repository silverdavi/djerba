#!/usr/bin/env python3
"""
Update Final Image Prompts - Round 2 Reviews
Updates image_prompt for recipes that need regeneration based on latest feedback.
"""

import json
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual")
REVIEWS_FILE = Path("image_reviewer/reviews.json")

# Updated prompts based on round 2 review feedback
FINAL_PROMPTS = {
    "002_admeshushah": """Create a photograph of Admeshushah - cooked pepper dish.

CRITICAL REQUIREMENTS:
- LESS peppers visible
- MORE WET - should be SOUP LIQUIDY (not dry)
- MORE tomatoes visible
- Soupy, liquidy consistency
- Peppers should be COOKED and SOFT

Professional food photography, natural light, cookbook quality.""",

    "004_artichoke_mushroom_stew": """Create a photograph of Artichoke and Mushroom Stew.

CRITICAL REQUIREMENTS:
- Sauce should be LESS OPAQUE (more transparent/clear)
- LESS creamy appearance
- NO carrots
- SMALLER artichokes
- YELLOW/GREEN sauce (not brown, not creamy white)
- Baby portobello mushrooms
- Minimal or no tofu

Professional food photography, natural light, cookbook quality.""",

    "012_brodo": """Create a photograph of Brodo - vegetable soup.

CRITICAL: This should be MORE SOUP than stew - liquidy, brothy!

Show:
- Light, clear or slightly colored broth
- SOUP consistency (not thick stew)
- Vegetables visible in the soup
- Traditional soup bowl
- Minimal tofu
- Liquidy appearance

Professional food photography, natural light.""",

    "013_bsisa": """Create a photograph of Bsisa - traditional semolina powder.

CRITICAL: Should NOT show visible oil - but still show the powder texture!

Show:
- Fine powder mixture in a bowl
- Golden-brown semolina powder
- Spices mixed in
- Powder texture (like flour)
- NO visible oil pools, droplets, or sheen
- Traditional serving bowl

Professional food photography, natural light.""",

    "036_granola_cookies": """Create a photograph of Granola Cookies.

CRITICAL REQUIREMENTS:
- NO almonds
- Granola should be BAKED (toasted, golden), NOT raw
- NO pumpkin seeds
- Round, rustic cookies
- Golden-brown baked color
- Visible oats and baked granola pieces

Professional food photography, warm bakery lighting.""",

    "057_marqa_zeitoun": """Create a photograph of Marqa Zeitoun - olive stew.

CRITICAL: It's ONLY OLIVES in RUNNY TOMATO SAUCE!

Show:
- GREEN olives (not black)
- RUNNY tomato sauce (not thick)
- NO potatoes
- NO carrots
- NO chickpeas
- NO lemon slice
- Simple: just olives in liquid tomato sauce
- NO meat or meat alternative

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
- NO carrots
- NO peas
- The BOTTOM is GROUNDED MEAT (not runny stew)
- Filling should look like ground meat mixture (solid, not liquidy)
- Golden-brown mashed potato top
- Top should have browned, meat-like appearance
- Served in baking dish
- Comfort food appearance

Professional food photography, warm lighting.""",

    "088_tbikhat_tmatem": """Create a photograph of Tbikhat Tmatem.

CRITICAL REQUIREMENTS:
- REMOVE lemons
- ADD one mushroom
- ADD some cubed potatoes
- Long green/red peppers should be COOKED (soft, tender)
- LESS tofu
- Rich stew appearance

Professional food photography, natural light.""",
}


def load_recipe(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_recipe(path: Path, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("Updating Final Image Prompts - Round 2")
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
    
    for recipe_id, prompt in FINAL_PROMPTS.items():
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
    print("Next step: Regenerate only these recipes with parallel workers")
    print("  python regenerate_selected_images.py")
    print()


if __name__ == "__main__":
    main()

