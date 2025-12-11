#!/usr/bin/env python3
"""
Fix Image Prompts for Cookbook

This script adds proper image_prompt fields to recipes that need them.
The prompts focus on the TRADITIONAL dish appearance, not the vegan substitutes.

Key principles:
1. Show what the dish LOOKS like traditionally
2. Tofu/seitan should NOT be visible - should look like the original
3. Focus on the final plated dish, not the substitutes
4. Dressings are NOT soups
5. Powders/ground items should look ground, not whole
"""

import json
from pathlib import Path

RECIPES_DIR = Path("data/recipes_multilingual")

# Custom image prompts for specific dish types
# These override the auto-generated prompts

DISH_CORRECTIONS = {
    # Dressings/Sauces - NOT soups!
    "015_caesar_dressing": {
        "type": "dressing",
        "prompt": """Create a photograph of Caesar Dressing - a creamy salad dressing.

THIS IS A DRESSING/SAUCE, NOT A SOUP!

Show:
- A small glass jar or ceramic bowl with creamy white-ish dressing
- Smooth, pourable consistency (like mayonnaise-based dressing)
- Perhaps a spoon showing the creamy texture
- A few capers or herbs as garnish
- Maybe a romaine lettuce leaf in background

Setting: Modern kitchen, clean aesthetic.
Professional food photography, natural soft light, 8K detail."""
    },
    
    "016_vegan_caesar": {
        "type": "dressing", 
        "prompt": """Create a photograph of Vegan Caesar Dressing.

THIS IS A DRESSING/SAUCE, NOT A SOUP!

Show:
- A small jar or bowl with creamy dressing
- Rich, thick, pourable consistency
- Creamy off-white/pale yellow color
- Perhaps drizzled over salad greens nearby

Professional food photography, natural light, cookbook quality."""
    },
    
    "074_salad_dressing": {
        "type": "dressing",
        "prompt": """Create a photograph of homemade salad dressing.

THIS IS A DRESSING, NOT A SOUP!

Show:
- A glass bottle or small jar with vinaigrette/dressing
- Clear or creamy liquid (depending on type)
- Fresh herbs visible
- Perhaps some salad greens in background

Professional food photography, natural light."""
    },
    
    "082_shlomit_dressing": {
        "type": "dressing",
        "prompt": """Create a photograph of Shlomit Dressing - a creamy Israeli-style salad dressing.

THIS IS A DRESSING, NOT A SOUP!

Show:
- Small bowl or jar with creamy dressing
- Smooth, pourable consistency
- Off-white/cream color
- Fresh and appetizing

Professional food photography, natural light."""
    },
    
    # Fish dishes - should look like fish, not tofu!
    "039_harimi": {
        "type": "fish_stew",
        "prompt": """Create a photograph of Harimi - a traditional North African spicy fish stew.

CRITICAL: This should look like a FISH STEW, not tofu!
- Show pieces that look like flaky white fish in rich red sauce
- Do NOT show obvious tofu cubes
- The protein should blend naturally into the stew

Show:
- Rich, vibrant red tomato-based sauce
- Pieces of flaky white protein in the sauce (fish-like appearance)
- Garnished with fresh cilantro/coriander
- Sliced hot peppers visible
- Served in traditional tagine or deep ceramic dish

Setting: Rustic Mediterranean kitchen with stone walls.
Professional food photography, warm lighting, 8K detail."""
    },
    
    "045_hraime": {
        "type": "fish_stew",
        "prompt": """Create a photograph of Hraime - Libyan/Tunisian spicy fish in red sauce.

CRITICAL: This should look like a FISH dish, not tofu!
- Pieces should look like flaky fish, not cubed tofu
- The protein blends into the sauce naturally

Show:
- Fiery red, spicy tomato-pepper sauce
- Pieces resembling fish fillets in the sauce
- Garnish of fresh herbs
- Served in rustic earthenware

Professional food photography, dramatic lighting, cookbook quality."""
    },
    
    # Meat stews - should look like meat stews
    "025_cholent": {
        "type": "meat_stew",
        "prompt": """Create a photograph of Cholent - traditional Jewish Sabbath stew.

This is a hearty, slow-cooked stew. Do NOT show obvious tofu.

Show:
- Dark, rich, caramelized stew
- Whole potatoes
- Beans (white/kidney beans)
- Barley grains
- Chunks of protein that look braised (not cubed tofu)
- Eggs (or leave out - just vegetables and grains)
- Served in heavy pot or deep bowl

The stew should look like it cooked overnight - deep brown color.
Professional food photography, warm cozy lighting."""
    },
    
    "029_dabikh": {
        "type": "meat_stew",
        "prompt": """Create a photograph of Dabikh - Djerban Jewish holiday stew.

Show a festive, rich stew. Protein should look like braised meat, not tofu.

Show:
- Rich brown/golden sauce
- Potatoes
- Vegetables in the stew
- Protein pieces that look braised and tender
- Traditional ceramic serving dish

Setting: Festive table setting.
Professional food photography, warm lighting."""
    },
    
    "090_tfina": {
        "type": "meat_stew",
        "prompt": """Create a photograph of Tfina (Tefina) - Tunisian Jewish Sabbath stew.

Traditional slow-cooked stew. Do NOT show obvious tofu cubes.

Show:
- Deep caramelized brown color (from overnight cooking)
- Whole potatoes, some split
- Chickpeas
- Wheat berries or barley
- Protein that looks slow-cooked and shredded (not cubed)
- Served in heavy pot

The stew should look like it was cooked for 12+ hours.
Professional food photography."""
    },
    
    # Schnitzel - should look like breaded cutlets
    "075_schnitzel": {
        "type": "breaded",
        "prompt": """Create a photograph of Schnitzel - crispy breaded cutlets.

This should look like traditional schnitzel - golden, crispy cutlets.
Do NOT show that it's made from tofu - should look like regular schnitzel.

Show:
- Golden-brown crispy breaded cutlets
- Flat, pounded thin shape (not thick cubes)
- Visible crispy breadcrumb coating
- Served on plate with lemon wedge
- Maybe some salad or fries on the side

The cutlets should look uniformly breaded and fried.
Professional food photography, appetizing golden color."""
    },
    
    # Beshisha - POWDER not grains!
    "008_beshisha": {
        "type": "powder",
        "prompt": """Create a photograph of Beshisha - traditional Djerban sweet powder.

CRITICAL: Beshisha is a FINE POWDER, not whole grains!

Show:
- Fine, golden-brown aromatic POWDER in a bowl
- The texture should be like flour or ground spices
- Perhaps some small energy balls made from the powder
- Dates nearby (as they're mixed in)
- Traditional serving bowl

Do NOT show:
- Whole grains
- Raw pellets
- Chunky pieces

The powder should look fine and aromatic.
Professional food photography, natural light."""
    },
    
    # Granola/cookies - should look like cookies
    "036_granola_cookies": {
        "type": "cookies",
        "prompt": """Create a photograph of Granola Cookies.

Show:
- Round, rustic cookies with visible oats and granola pieces
- Golden-brown baked color
- Arranged on baking sheet or plate
- Some broken to show texture

Professional food photography, warm bakery lighting."""
    },
    
    # Fricassee - stew not showing tofu
    "033_fricassee_stew": {
        "type": "stew",
        "prompt": """Create a photograph of Fricassee Stew - Tunisian style.

Show a rich vegetable and protein stew. Protein should NOT look like obvious tofu.

Show:
- Light-colored, creamy sauce
- Vegetables (potatoes, carrots, peas)
- Protein pieces that look tender and stewed
- Fresh herbs

Professional food photography, soft lighting."""
    },
    
    "035_frikaseh": {
        "type": "stew",
        "prompt": """Create a photograph of Frikaseh - Tunisian Jewish style.

Traditional fricassee with vegetables. Do not show obvious tofu.

Show:
- Creamy/light sauce
- Vegetables
- Protein pieces that blend in naturally
- Served in traditional dish

Professional food photography."""
    },
    
    # Ojja/Shakshuka - eggs replaced but should look similar
    "066_ojja_merguez": {
        "type": "egg_dish",
        "prompt": """Create a photograph of Ojja - Tunisian pepper and tomato dish.

Traditional Ojja with peppers and tomatoes. This is a vegan version.

Show:
- Rich red tomato-pepper sauce in a skillet
- Colorful peppers (red, green)
- Spicy, aromatic looking
- Served in cast iron or traditional pan
- Perhaps some crusty bread on the side

The focus should be on the flavorful sauce and peppers.
Professional food photography, vibrant colors."""
    },
    
    # Pancakes - should look like pancakes
    "068_pancakes": {
        "type": "pancakes",
        "prompt": """Create a photograph of fluffy pancakes.

Show:
- Stack of golden-brown pancakes
- Fluffy, light texture visible
- Perhaps maple syrup drizzle
- Fresh berries or fruit on top
- Butter pat melting (use vegan butter look)

Professional food photography, breakfast lighting."""
    },
    
    "084_pancakes_soly": {
        "type": "pancakes",
        "prompt": """Create a photograph of homestyle pancakes.

Show:
- Stacked fluffy pancakes
- Golden brown color
- Perhaps some fruit topping
- Syrup

Professional food photography, warm morning light."""
    },
    
    # Pizza - should look like pizza
    "072_pizza": {
        "type": "pizza",
        "prompt": """Create a photograph of homemade pizza.

Show:
- Round pizza with toppings
- Golden crispy crust
- Melted cheese (vegan cheese) - should look melted
- Colorful vegetable toppings
- Perhaps one slice pulled

Professional food photography, appetizing."""
    },
    
    # Shawarma - should look like shawarma
    "080_shawarma": {
        "type": "wrap",
        "prompt": """Create a photograph of Shawarma wrap.

This should look like traditional shawarma. Do NOT show obvious tofu.

Show:
- Pita or laffa bread wrap
- Sliced, seasoned protein (seitan/soy - but should look like shawarma meat)
- Fresh vegetables (tomato, onion, pickles)
- Tahini sauce drizzle
- Perhaps some on a plate nearby

The protein should look thinly sliced and seasoned like shawarma.
Professional food photography, Middle Eastern style."""
    },
    
    # Shepherd's Pie - should look like the classic
    "081_shepherds_pie": {
        "type": "casserole",
        "prompt": """Create a photograph of Shepherd's Pie.

Classic comfort food look. Do NOT show obvious tofu/lentils - should look traditional.

Show:
- Golden-brown mashed potato top (slightly browned peaks)
- Served in baking dish
- Perhaps one serving scooped to show layers
- Rich filling visible underneath potato

Professional food photography, comfort food style."""
    },
}

# Generic prompts for dish types without specific corrections
GENERIC_PROMPTS = {
    "soup": """Professional food photography of {name}, a traditional soup.
Show in a ceramic bowl with garnishes. Natural lighting, cookbook quality.""",
    
    "stew": """Professional food photography of {name}, a traditional stew.
Rich, hearty appearance in a ceramic dish. Natural lighting, cookbook quality.""",
    
    "bread": """Professional food photography of {name}, freshly baked bread.
Golden crust, artisan appearance. Natural lighting, bakery style.""",
    
    "dessert": """Professional food photography of {name}, a traditional dessert.
Appetizing presentation on a plate. Natural lighting, cookbook quality.""",
    
    "salad": """Professional food photography of {name}, a fresh salad.
Colorful, fresh vegetables arranged beautifully. Natural lighting.""",
}


def load_recipe(path: Path) -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_recipe(path: Path, data: dict):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_image_prompt(recipe: dict, recipe_id: str) -> bool:
    """Add image_prompt to recipe if it needs one. Returns True if modified."""
    
    # Skip if already has a custom prompt
    if 'image_prompt' in recipe:
        return False
    
    # Check if we have a specific correction for this recipe
    if recipe_id in DISH_CORRECTIONS:
        recipe['image_prompt'] = DISH_CORRECTIONS[recipe_id]['prompt']
        print(f"  ✓ Added custom prompt: {recipe_id}")
        return True
    
    return False


def main():
    print("Fixing Image Prompts for Cookbook")
    print("=" * 50)
    
    modified_count = 0
    
    for recipe_path in sorted(RECIPES_DIR.glob("*.json")):
        recipe_id = recipe_path.stem
        recipe = load_recipe(recipe_path)
        
        if add_image_prompt(recipe, recipe_id):
            save_recipe(recipe_path, recipe)
            modified_count += 1
    
    print()
    print(f"Modified {modified_count} recipes with custom image prompts.")
    print()
    print("To regenerate images, run:")
    print("  python generate_cookbook_images.py --regenerate-with-prompts")


if __name__ == "__main__":
    main()

