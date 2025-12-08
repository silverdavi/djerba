# ReciMe to Safed Format Conversion Log

**Conversion Date:** 2025-12-08 09:34:38

## Summary

- **Recipes converted:** 36
- **Conversion failed:** 0
- **Output directory:** recipe_app_downloads/converted

## Next Steps

1. **Copy to safed_recipes for processing:**
   ```bash
   cp recipe_app_downloads/converted/*.json data/safed_recipes/
   ```

2. **Run full pipeline (veganize + translate + images):**
   ```bash
   python transform_recipes_gemini.py --start 0 --with-images
   ```

3. **Or process specific recipes:**
   ```bash
   python transform_recipes_gemini.py --single "01_recipe_name.json" --with-images
   ```

## Output Format

Each converted recipe has:
- `name_hebrew`: Recipe name
- `ingredients[]`: List of ingredients
- `instructions[]`: List of instruction steps
- `metadata`: Source information and import date
- `id`: Machine-readable identifier

## Log Entries

[2025-12-08 09:34:38] 📂 Reading recipes from: recipe_app_downloads/raw
[2025-12-08 09:34:38]   Found 36 recipe files
[2025-12-08 09:34:38]   ✓ Converted: Adafina → adafina.json
[2025-12-08 09:34:38]   ✓ Converted: Adafina - Wheat → adafina_-_wheat.json
[2025-12-08 09:34:38]   ✓ Converted: Apple crumble → apple_crumble.json
[2025-12-08 09:34:38]   ✓ Converted: Artichoke & Mushrooms → artichoke___mushrooms.json
[2025-12-08 09:34:38]   ✓ Converted: Banana Cake → banana_cake.json
[2025-12-08 09:34:38]   ✓ Converted: Biscoti Judy → biscoti_judy.json
[2025-12-08 09:34:38]   ✓ Converted: Bread → bread.json
[2025-12-08 09:34:38]   ✓ Converted: Charost → charost.json
[2025-12-08 09:34:38]   ✓ Converted: Chocolate Balls → chocolate_balls.json
[2025-12-08 09:34:38]   ✓ Converted: Chocolate Cake → chocolate_cake.json
[2025-12-08 09:34:38]   ✓ Converted: Chocolate Peanut Buddy Bars → chocolate_peanut_buddy_bars.json
[2025-12-08 09:34:38]   ✓ Converted: Chocolate peanut butter muffins → chocolate_peanut_butter_muffins.json
[2025-12-08 09:34:38]   ✓ Converted: Cholent → cholent.json
[2025-12-08 09:34:38]   ✓ Converted: Cujada → cujada.json
[2025-12-08 09:34:38]   ✓ Converted: Fish → fish.json
[2025-12-08 09:34:38]   ✓ Converted: French toast → french_toast.json
[2025-12-08 09:34:38]   ✓ Converted: Granola cookies → granola_cookies.json
[2025-12-08 09:34:38]   ✓ Converted: Honey cake Lior BenMosheh → honey_cake_lior_benmosheh.json
[2025-12-08 09:34:38]   ✓ Converted: Honey Cake Mami → honey_cake_mami.json
[2025-12-08 09:34:38]   ✓ Converted: Hot Fudge Pudding Cake → hot_fudge_pudding_cake.json
[2025-12-08 09:34:38]   ✓ Converted: Humus salad → humus_salad.json
[2025-12-08 09:34:38]   ✓ Converted: Marmuma → marmuma.json
[2025-12-08 09:34:38]   ✓ Converted: Mocha Java Cake → mocha_java_cake.json
[2025-12-08 09:34:38]   ✓ Converted: Nougat and Peanut Cake – Mor Abergil → nougat_and_peanut_cake___mor_abergil.json
[2025-12-08 09:34:38]   ✓ Converted: Olives red → olives_red.json
[2025-12-08 09:34:38]   ✓ Converted: Original Toll House® Chocolate Chip Cookies → original_toll_house__chocolate_chip_cookies.json
[2025-12-08 09:34:38]   ✓ Converted: Pancakes Efrat Shachor → pancakes_efrat_shachor.json
[2025-12-08 09:34:38]   ✓ Converted: Pancakes Soly → pancakes_soly.json
[2025-12-08 09:34:38]   ✓ Converted: Pizza → pizza.json
[2025-12-08 09:34:38]   ✓ Converted: Sfingh → sfingh.json
[2025-12-08 09:34:38]   ✓ Converted: Shepherd pie → shepherd_pie.json
[2025-12-08 09:34:38]   ✓ Converted: Shlomit Perl Dressing → shlomit_perl_dressing.json
[2025-12-08 09:34:38]   ✓ Converted: Sour dough bread Soly → sour_dough_bread_soly.json
[2025-12-08 09:34:38]   ✓ Converted: Soy Shawarma → soy_shawarma.json
[2025-12-08 09:34:38]   ✓ Converted: Vegan Caesar Dressing → vegan_caesar_dressing.json
[2025-12-08 09:34:38]   ✓ Converted: Yellow meat → yellow_meat.json
