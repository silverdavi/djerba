#!/usr/bin/env python3
"""
Fix All Image Prompts for Cookbook - Based on User Reviews

This script adds custom image_prompt fields to all 42 recipes that need regeneration
based on the comprehensive review feedback.
"""

import json
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual")

# Custom image prompts for all recipes needing regeneration
# Based on user review feedback
IMAGE_PROMPTS = {
    "001_adafina": """Create a photograph of Adafina - traditional Jewish Sabbath stew.

CRITICAL REQUIREMENTS:
- Show in a HEAVY POT (not a bowl) - traditional cooking vessel
- Potatoes should be CUBED and PEELED (not whole unpeeled)
- DEEPER BROWN COLOR - from slow overnight cooking with caramelized sugar
- Rich, dark caramelized stew appearance
- Chickpeas visible
- Wheat berry pouch visible
- Protein should look braised and integrated (NOT obvious tofu cubes)

Setting: Traditional kitchen, heavy pot on stove or table.
Professional food photography, warm lighting, 8K detail, photorealistic.""",

    "002_admeshushah": """Create a photograph of Admeshushah - cooked pepper dish.

CRITICAL: Peppers must be COOKED and SOFT, not raw!

Show:
- Soft, cooked peppers (red and/or green)
- Peppers should look tender and stewed
- Rich sauce/gravy
- Traditional serving dish

Professional food photography, natural light, cookbook quality.""",

    "003_apple_crumble": """Create a photograph of Apple Crumble.

CRITICAL: This is a CAKE - show it in a CAKE PAN, not a bowl!

Show:
- Apple crumble baked in a round or square cake pan
- Golden-brown crumble topping
- Visible apple filling
- Perhaps a slice cut to show layers
- Cake pan visible (not just the dish)

Professional food photography, bakery style, warm lighting.""",

    "004_artichoke_mushroom_stew": """Create a photograph of Artichoke and Mushroom Stew.

CRITICAL REQUIREMENTS:
- SMALLER baby portobello mushrooms (not large)
- MORE mushrooms visible
- LESS tofu (minimal or none visible)
- Artichoke hearts visible
- Rich stew appearance

Professional food photography, natural light, cookbook quality.""",

    "010_bkaila": """Create a photograph of Bkaila - traditional spinach stew.

CRITICAL: LESS TOFU - focus on the vegetables and sauce!

Show:
- Rich green spinach stew
- Minimal or no visible tofu
- Traditional serving dish
- Herbs and spices visible

Professional food photography, natural light.""",

    "011_brik": """Create a photograph of Brik - Tunisian savory pastry.

CRITICAL REQUIREMENTS:
- Shape: HALF-CIRCLE (folded circle), NOT a triangle!
- NO powdered sugar - this is SAVORY, not sweet!
- Golden-brown crispy pastry
- Filling visible at the edges
- Traditional appearance

Professional food photography, appetizing golden color.""",

    "012_brodo": """Create a photograph of Brodo - vegetable stew.

CRITICAL REQUIREMENTS:
- LESS tofu
- Vegetables should be MORE COOKED (soft, tender)
- Rich stew appearance
- Traditional serving dish

Professional food photography, natural light.""",

    "025_cholent": """Create a photograph of Cholent - Sabbath stew.

CRITICAL REQUIREMENTS:
- Potatoes should be PEELED (not unpeeled)
- Instead of eggs, show SMALL MUSHROOMS
- Dark, rich, caramelized stew
- Beans and barley visible
- Protein looks braised (not obvious tofu)

Professional food photography, warm cozy lighting.""",

    "026_couscous": """Create a photograph of Couscous - traditional semolina dish.

CRITICAL REQUIREMENTS:
- SMALLER grains (coarse semolina, not large pearls)
- NO water visible - should be fluffy, dry grains
- Light, fluffy texture
- Served in traditional couscous bowl
- Perhaps with vegetables on the side

Professional food photography, natural light, cookbook quality.""",

    "027_couscous_soup": """Create a photograph of Couscous Soup.

CRITICAL: LESS tofu - focus on the soup and vegetables!

Show:
- Light soup with couscous grains
- Vegetables visible
- Minimal tofu
- Traditional soup bowl

Professional food photography, natural light.""",

    "029_dabikh": """Create a photograph of Dabikh - holiday stew.

CRITICAL: Remove any TEXT overlay - just the dish!

Show:
- Rich, festive stew
- Potatoes and vegetables
- Protein looks braised
- Traditional ceramic dish
- NO text, NO labels, NO writing

Professional food photography, warm lighting.""",

    "034_fricasse": """Create a photograph of Fricasse - Tunisian filled bun.

CRITICAL: This is NOT a burrito! It's a HALF-CUT BUN filled with ingredients!

Show:
- Round bun cut in HALF (like a sandwich bun)
- Filling visible inside the bun
- Fried/golden bun exterior
- Served as individual filled buns

Professional food photography, appetizing.""",

    "035_frikaseh": """Create a photograph of Frikaseh - fried filled bun.

CRITICAL: This is a FRIED FILLED BUN, not a stew!

Show:
- Golden-brown fried bun
- Cut open to show filling
- Crispy exterior
- Filling visible (vegetables, etc.)
- Individual bun presentation

Professional food photography, appetizing golden color.""",

    "037_green_beans": """Create a photograph of Green Bean Stew.

CRITICAL: NO pastry! This is a STEW of green beans in red sauce!

Show:
- Green beans in rich red tomato sauce
- Stew consistency
- Traditional serving dish
- NO pastry, NO bread, NO baked goods

Professional food photography, natural light.""",

    "040_hita": """Create a photograph of Hita.

CRITICAL: Should be DRIER, not soupy!

Show:
- Drier consistency (not watery)
- Traditional appearance
- Served in appropriate dish

Professional food photography, natural light.""",

    "046_hsou": """Create a photograph of Hsou - semolina soup.

CRITICAL: This is a LIGHT RED SOUP with semolina, NOT cakes!

Show:
- Light red/broth-colored soup
- Semolina grains visible in the soup
- Soup consistency
- Traditional soup bowl
- NO cakes, NO baked goods

Professional food photography, natural light.""",

    "047_ktaa": """Create a photograph of Ktaa - soup with torn dough.

CRITICAL: This is a SOUP with pieces of torn dough cooked in it!

Show:
- Red soup (onions, paprika, etc.)
- Pieces of torn hand-made dough visible in the soup
- Soup consistency
- Traditional soup bowl
- Dough pieces should look hand-torn and cooked

Professional food photography, natural light.""",

    "048_kuklot": """Create a photograph of Kuklot - semolina spheres.

CRITICAL: Just round gray spheres - NOT in soup!

Show:
- Round gray semolina spheres
- Made from semolina and spices
- Individual spheres on a plate
- NO soup, NO liquid
- Simple presentation

Professional food photography, natural light.""",

    "050_loubia_khadra": """Create a photograph of Loubia Khadra - green bean stew.

CRITICAL REQUIREMENTS:
- NO sesame seeds
- NO uncooked peppers
- Cooked green beans in sauce
- Traditional stew appearance

Professional food photography, natural light.""",

    "051_maakouda": """Create a photograph of Maakouda - potato fritter.

CRITICAL: Potatoes should be MORE INTEGRATED (not chunky pieces)!

Show:
- Well-integrated potato mixture
- Golden-brown fritter
- Smooth, cohesive texture
- Traditional appearance

Professional food photography, appetizing golden color.""",

    "053_mahshi": """Create a photograph of Mahshi - stuffed vegetables.

CRITICAL: These are COOKED STUFFED VEGETABLES, not tofu with rice stew!

Show:
- Whole vegetables (zucchini, peppers, etc.) stuffed and cooked
- Vegetables should look cooked and tender
- Stuffing visible at the ends
- Traditional presentation
- NO tofu chunks, NO rice stew appearance

Professional food photography, natural light.""",

    "055_marmouma": """Create a photograph of Marmouma.

CRITICAL: NO raw peppers!

Show:
- Cooked dish
- All ingredients cooked (peppers should be soft)
- Traditional appearance
- NO raw vegetables

Professional food photography, natural light.""",

    "057_marqa_zeitoun": """Create a photograph of Marqa Zeitoun - olive stew.

CRITICAL: This is PITTED OLIVES COOKED IN RED SAUCE, not a green dish!

Show:
- Pitted olives in rich red tomato sauce
- Red sauce dominant (not green)
- NO meat or meat alternative needed
- Traditional serving dish
- Simple, traditional appearance

Professional food photography, natural light.""",

    "058_marqat_gannariya": """Create a photograph of Marqat Gannariya - artichoke stew.

CRITICAL REQUIREMENTS:
- NO tofu
- SMALLER artichokes
- SMALLER baby mushrooms
- Color is correct (keep the color)
- Rich stew appearance

Professional food photography, natural light.""",

    "059_mhamsa": """Create a photograph of Mhamsa - pearl pasta dish.

CRITICAL: LESS unrelated vegetables - focus on the mhamsa!

Show:
- Pearl pasta (mhamsa) as the main focus
- Minimal vegetables (only what's in the recipe)
- Traditional appearance
- Served in appropriate dish

Professional food photography, natural light.""",

    "069_pastel": """Create a photograph of Pastel.

CRITICAL REQUIREMENTS:
- NO tofu visible!
- TOP should be CRISP MASHED POTATO
- Golden-brown crispy potato top
- Baked appearance
- Traditional casserole dish

Professional food photography, appetizing golden color.""",

    "072_pizza": """Create a photograph of Pizza.

CRITICAL REQUIREMENTS:
- THICK crust (like focaccia)
- OPEN TOP (not covered)
- Green olives visible
- Focaccia-style appearance
- Rustic, thick pizza

Professional food photography, appetizing.""",

    "073_bkila": """Create a photograph of Bkila.

CRITICAL: NO need for tofu - focus on vegetables!

Show:
- Vegetable stew
- NO tofu
- Traditional appearance
- Rich sauce

Professional food photography, natural light.""",

    "074_salad_dressing": """Create a photograph of Salad Dressing.

CRITICAL: This is a DRESSING, NOT a cake!

Show:
- Small jar or bowl with dressing
- Liquid/pourable consistency
- Fresh appearance
- Perhaps some salad greens nearby
- NO cake, NO baked goods

Professional food photography, natural light.""",

    "080_shawarma": """Create a photograph of Shawarma.

CRITICAL: This should be DRY SPICED SHAWARMA, NOT a stew!

Show:
- Thinly sliced, spiced protein
- DRY appearance (not saucy)
- Served on plate or in wrap
- Spices visible
- Traditional shawarma look
- NO stew, NO sauce

Professional food photography, appetizing.""",

    "081_shepherds_pie": """Create a photograph of Shepherd's Pie.

CRITICAL: Top should look like BROWNED MEAT, not cookie crumble!

Show:
- Golden-brown mashed potato top
- Top should have browned, meat-like appearance (from browning)
- Served in baking dish
- Rich filling visible
- Comfort food appearance

Professional food photography, warm lighting.""",

    "082_shlomit_dressing": """Create a photograph of Shlomit Dressing.

CRITICAL: Should be YELLOWISH color!

Show:
- Creamy dressing in small bowl/jar
- YELLOWISH color (not white, not brown)
- Smooth, pourable consistency
- Fresh appearance

Professional food photography, natural light.""",

    "083_shmid": """Create a photograph of Shmid - soup.

CRITICAL: This is eaten as a SOUP - no weird spoon on vegetables!

Show:
- Soup in a bowl
- Vegetables in the soup
- Soup consistency
- Traditional presentation
- NO spoons, NO utensils in the image
- Just the soup in a bowl

Professional food photography, natural light.""",

    "087_tbikha_chagim": """Create a photograph of Tbikha Chagim.

CRITICAL REQUIREMENTS:
- LESS tofu (too much visible)
- Herbs should be COOKED (not raw dill)
- A bit MORE WATERY (soupier consistency)
- Traditional stew appearance

Professional food photography, natural light.""",

    "088_tbikhat_tmatem": """Create a photograph of Tbikhat Tmatem.

CRITICAL REQUIREMENTS:
- Long green/red peppers should be COOKED (soft, tender)
- LESS tofu
- Rich stew appearance

Professional food photography, natural light.""",

    "090_tfina": """Create a photograph of Tfina - Sabbath stew.

CRITICAL REQUIREMENTS:
- LESS tofu
- MORE DARK COLOR (deeper brown from slow cooking)
- Rich, caramelized appearance
- Traditional pot or serving dish

Professional food photography, warm lighting.""",

    "091_tirshi": """Create a photograph of Tirshi - dip.

CRITICAL REQUIREMENTS:
- This is JUST A DIP - no potatoes or other additions!
- Show in a DIP BOWL (small, shallow), NOT a soup bowl
- Dip consistency
- Simple presentation
- NO soup bowl, NO large bowl

Professional food photography, natural light.""",

    "093_yoyo": """Create a photograph of Yoyo - sweet pastry.

CRITICAL: NO powdered sugar! It's SUGAR SYRUP glaze!

Show:
- Pastry with SHINY SUGAR SYRUP glaze
- Glossy, syrupy appearance
- NO powdered sugar
- Traditional sweet pastry look

Professional food photography, appetizing.""",
}


def load_recipe(path: Path) -> dict:
    """Load a recipe JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_recipe(path: Path, data: dict):
    """Save a recipe JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    print("Fixing All Image Prompts Based on Reviews")
    print("=" * 60)
    print()
    
    modified_count = 0
    not_found = []
    
    for recipe_id, prompt in IMAGE_PROMPTS.items():
        recipe_path = RECIPES_DIR / f"{recipe_id}.json"
        
        if not recipe_path.exists():
            not_found.append(recipe_id)
            print(f"  ⚠️  Recipe not found: {recipe_id}")
            continue
        
        recipe = load_recipe(recipe_path)
        
        # Add or update the image_prompt
        recipe['image_prompt'] = prompt
        save_recipe(recipe_path, recipe)
        
        print(f"  ✓ Updated: {recipe_id}")
        modified_count += 1
    
    print()
    print("=" * 60)
    print(f"✓ Modified {modified_count} recipes with custom image prompts")
    
    if not_found:
        print(f"⚠️  {len(not_found)} recipes not found: {', '.join(not_found)}")
    
    print()
    print("Next step: Regenerate images")
    print("  python generate_cookbook_images.py --regenerate-with-prompts")
    print()


if __name__ == "__main__":
    main()

