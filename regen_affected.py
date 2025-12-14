#!/usr/bin/env python3
"""Regenerate multilingual versions for affected recipes."""
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

AFFECTED = [
    "adafina", "adafina_wheat_side_dish", "artichoke_mushrooms_stew", 
    "baked_potato_levivot", "banana_cake", "biscoti_judy", "cholent", 
    "chraime_spicy_fish_stew", "ciceritos", "honey_cake_mami", 
    "mocha_java_cake", "original_toll_house_chocolate_chip_cookies",
    "pancakes_soly", "pancakes_efrat_shachor", "potache_white_bean_stew",
    "sfingh", "shlomit_tomato_salad", "tbikha_tomatem", "marmouma",
    "vegan_caesar_dressing", "vegetable_soup_for_couscous"
]

def process_recipe(recipe_id):
    result = subprocess.run(
        ["python", "multilingualize_recipes.py", "--single", recipe_id],
        capture_output=True, text=True
    )
    return recipe_id, result.returncode == 0, result.stderr[:200] if result.returncode != 0 else ""

print(f"Processing {len(AFFECTED)} recipes...")
with ThreadPoolExecutor(max_workers=30) as ex:
    futures = {ex.submit(process_recipe, r): r for r in AFFECTED}
    for future in as_completed(futures):
        rid, ok, err = future.result()
        print(f"{'✅' if ok else '❌'} {rid}" + (f" - {err}" if err else ""))

print("Done!")
