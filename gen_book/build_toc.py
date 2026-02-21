#!/usr/bin/env python3
"""
Build TOC only - for quick iteration on table of contents design.
Outputs: gen_book/output/toc_preview.html
"""

import json
from pathlib import Path
from html import escape

ROOT = Path(__file__).parent.parent
RECIPES_DIR = ROOT / "data" / "recipes_multilingual_v2"
CSS_FILE = ROOT / "gen_book" / "cookbook.css"
OUTPUT = ROOT / "gen_book" / "output" / "toc_preview.html"

# Recipe categories for grouping
CATEGORIES = {
    "Stews & Mains": [
        "adafina", "tfina_stew", "cholent", "bkailatunisianstew",
        "chraimespicyfish_stew", "veganfishchraime", "dabikh_hagim",
        "tbikha_tomatem", "ciceritos", "lentechalentilstew",
        "potachewhitebean_stew", "greenbeanstomato_sauce",
        "redstewedolives", "yellow_meat", "artichokemushroomsstew",
        "chickenfricasseestew", "red_sauce_meatballs",
        "shakshukacaramelizedonion_sausage", "umami_mushrooms",
    ],
    "Soups": [
        "brodochickensoup", "binasthicksourspicysoup", "dwida",
        "kataa_soup", "vegetablesoupfor_couscous", "greenpeasoup",
    ],
    "Couscous, Pasta & Grains": [
        "homemade_couscous", "mhamsa", "lintriya", "kugel",
        "adafinawheatside_dish", "semolina_porridge", "shmid",
        "bshisha_bsisa", "veganfriedrice",
    ],
    "Breads & Pastry": [
        "bread", "fricassee_rolls", "brikot", "burekasthreeways",
        "sfenj", "sfingh", "mufleta", "cashew_cannelloni",
    ],
    "Eggs, Omelets & Salads": [
        "cujada", "nazhaherbomelet", "adamshusha", "maakouda",
        "veganeggsalad", "humus_salad", "shlomittomatosalad",
        "marmouma", "tirshipumpkinsalad", "msiyar", "charoset",
        "vegancaesardressing", "shlomitperldressing",
    ],
    "Stuffed & Shaped": [
        "mahshistuffedvegetables", "banatagestuffedpotato_croquettes",
        "kouklotsemolinadumplings", "bakedpotatolevivot", "kishke",
        "shepherdpienorth_african",
    ],
    "Main Dishes - Modern": [
        "soy_shawarma", "schnitzel", "pizza",
    ],
    "Cakes & Sweets": [
        "chocolate_cake", "honeycakemami", "honeycakelior_benmosheh",
        "mochajavacake", "hotfudgepudding_cake", "apple_crumble",
        "banana_cake", "nougatandpeanutcakemor_abergil",
        "dolce_de_leche_biscuits", "yeast_cake",
        "yoyotunisiandoughnuts", "sufganiyot",
    ],
    "Cookies, Bars & Snacks": [
        "biscoti_judy", "granola_cookies",
        "originaltollhousechocolatechip_cookies",
        "chocolatepeanutbuddy_bars", "chocolatepeanutbutter_muffins",
        "chocolate_balls",
    ],
    "Breakfast & Basics": [
        "pancakes_soly", "pancakesefratshachor", "french_toast",
        "sourdoughbread_soly", "spice_mixes",
    ],
}

def load_recipes():
    recipes = {}
    for f in sorted(RECIPES_DIR.glob("*.json")):
        with open(f, 'r', encoding='utf-8') as fh:
            r = json.load(fh)
            recipes[r['id']] = r
    return recipes

def render_toc(recipes):
    """Render grouped TOC pages."""
    
    # Assign chapter numbers in category order
    chapter_num = 1
    categorized = []
    used_ids = set()
    
    for cat_name, ids in CATEGORIES.items():
        cat_recipes = []
        for rid in ids:
            if rid in recipes:
                cat_recipes.append((chapter_num, recipes[rid]))
                used_ids.add(rid)
                chapter_num += 1
        if cat_recipes:
            categorized.append((cat_name, cat_recipes))
    
    # Any uncategorized recipes
    uncategorized = []
    for rid, r in recipes.items():
        if rid not in used_ids:
            uncategorized.append((chapter_num, r))
            chapter_num += 1
    if uncategorized:
        categorized.append(("Other", uncategorized))
    
    # Build pages with controlled breaks
    # Each 8x8 page has ~0.5in padding top/bottom + header on first page
    # Usable height: ~7in. Each entry is 0.42in. Category header ~0.3in.
    # With 2-column layout: ~16 entries per column = ~32 entries per page
    # First page less due to header (~28 entries)
    
    MAX_FIRST_PAGE = 24  # Fewer due to header
    MAX_PER_PAGE = 28
    
    # Flatten all entries with category markers
    flat_entries = []
    for cat_name, cat_recipes in categorized:
        flat_entries.append(("category", cat_name, None, None))
        for num, recipe in cat_recipes:
            flat_entries.append(("recipe", num, recipe, cat_name))
    
    # Split into pages
    pages = []
    current_page = []
    current_count = 0
    is_first = True
    max_for_page = MAX_FIRST_PAGE
    
    for entry in flat_entries:
        entry_cost = 1 if entry[0] == "recipe" else 0.7  # categories take less space
        
        # Check if adding this entry would overflow
        if current_count + entry_cost > max_for_page:
            pages.append((is_first, current_page))
            current_page = []
            current_count = 0
            is_first = False
            max_for_page = MAX_PER_PAGE
            
            # If we just broke mid-category, re-add the category header
            if entry[0] == "recipe":
                current_page.append(("category", entry[3] + " (cont.)", None, None))
                current_count += 0.7
        
        current_page.append(entry)
        current_count += entry_cost
    
    if current_page:
        pages.append((is_first, current_page))
    
    # Render pages
    toc_html = ""
    for page_idx, (is_first_page, page_entries) in enumerate(pages):
        header = '''<div class="toc-header">
    <h1>Contents</h1>
    <div class="toc-subtitle">תוכן עניינים · Contenido · فهرس</div>
  </div>''' if is_first_page else ''
        
        items_html = ""
        current_cat_open = False
        
        for entry in page_entries:
            if entry[0] == "category":
                if current_cat_open:
                    items_html += "\n          </div>\n        </div>"
                items_html += f'''
        <div class="toc-category">
          <div class="toc-category-name">{escape(entry[1])}</div>
          <div class="toc-category-items">'''
                current_cat_open = True
            else:
                _, num, recipe, _ = entry
                n = recipe["name"]
                page = 7 + (num - 1) * 4 + 1
                
                items_html += f'''
            <div class="toc-entry">
              <span class="toc-num">{num}</span>
              <div class="toc-entry-names">
                <div class="toc-line-1">
                  <span class="toc-en">{escape(n["en"])}</span>
                  <span class="toc-he">{escape(n.get("he",""))}</span>
                </div>
                <div class="toc-line-2">
                  <span class="toc-es">{escape(n.get("es",""))}</span>
                  <span class="toc-ar">{escape(n.get("ar",""))}</span>
                </div>
              </div>
              <span class="toc-page">{page}</span>
            </div>'''
        
        if current_cat_open:
            items_html += "\n          </div>\n        </div>"
        
        toc_html += f'''
  <section class="page page--toc">
    <div class="page-inner toc-page-inner">
      {header}
      <div class="toc-body">
        {items_html}
      </div>
    </div>
  </section>
'''
    
    return toc_html

def main():
    recipes = load_recipes()
    print(f"Loaded {len(recipes)} recipes")
    
    toc_content = render_toc(recipes)
    
    # Check for uncategorized
    all_categorized = set()
    for ids in CATEGORIES.values():
        all_categorized.update(ids)
    missing = set(recipes.keys()) - all_categorized
    if missing:
        print(f"⚠ Uncategorized: {missing}")
    
    css = CSS_FILE.read_text(encoding='utf-8')
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TOC Preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Heebo:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">
<style>
{css}

/* ============================================
   TABLE OF CONTENTS - GROUPED (PAGED)
   ============================================ */

.toc-page-inner {{
  padding: 0.4in 0.5in;
  width: 100%;
  height: 100%;
  overflow: hidden;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}}

.toc-header {{
  text-align: center;
  padding-bottom: 0.25in;
  flex-shrink: 0;
}}

.toc-header h1 {{
  font-family: var(--font-title);
  font-size: 2rem;
  color: var(--accent);
  margin: 0 0 0.08in;
  letter-spacing: 0.05em;
}}

.toc-header .toc-subtitle {{
  font-size: 0.85rem;
  color: var(--muted);
  letter-spacing: 0.1em;
}}

.toc-body {{
  flex: 1;
  columns: 2;
  column-gap: 0.35in;
  overflow: hidden;
}}

.toc-category {{
  break-inside: avoid;
  margin-bottom: 0.15in;
}}

.toc-category-name {{
  font-family: var(--font-title);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  border-bottom: 1px solid var(--accent-soft);
  padding-bottom: 0.03in;
  margin-bottom: 0.06in;
}}

.toc-category-items {{
  margin-bottom: 0.1in;
}}

.toc-entry {{
  display: flex;
  align-items: baseline;
  gap: 0.06in;
  padding: 0.02in 0;
  line-height: 1.3;
  min-height: 0.38in;
}}

.toc-num {{
  font-size: 0.55rem;
  color: var(--muted);
  min-width: 0.18in;
  text-align: right;
  flex-shrink: 0;
}}

.toc-entry-names {{
  flex: 1;
  min-width: 0;
}}

.toc-line-1 {{
  display: flex;
  justify-content: space-between;
  gap: 0.08in;
}}

.toc-en {{
  font-family: "Sora", sans-serif;
  font-size: 0.65rem;
  font-weight: 600;
  color: var(--ink);
}}

.toc-he {{
  font-family: "Heebo", sans-serif;
  font-size: 0.65rem;
  direction: rtl;
  color: var(--ink);
  text-align: right;
}}

.toc-line-2 {{
  display: flex;
  justify-content: space-between;
  gap: 0.08in;
  margin-top: 0.01in;
}}

.toc-es {{
  font-family: "Fraunces", serif;
  font-size: 0.55rem;
  color: var(--muted);
}}

.toc-ar {{
  font-family: "Noto Naskh Arabic", sans-serif;
  font-size: 0.55rem;
  direction: rtl;
  color: var(--muted);
  text-align: right;
}}

.toc-page {{
  font-size: 0.55rem;
  color: var(--muted);
  flex-shrink: 0;
  min-width: 0.18in;
  text-align: right;
}}

@media print {{
  .page--toc {{
    page-break-after: always;
    overflow: hidden;
  }}
}}

</style>
</head>
<body style="background: #e0dfda; padding: 2rem;">

<div class="book">
{toc_content}
</div>

</body>
</html>'''
    
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(html, encoding='utf-8')
    print(f"✓ Written to {OUTPUT}")

if __name__ == "__main__":
    main()
