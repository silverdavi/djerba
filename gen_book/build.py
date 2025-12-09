#!/usr/bin/env python3
"""
Four-Language Cookbook Builder

Reads recipe JSON files and generates:
1. Individual HTML pages for web deployment
2. Combined HTML for PDF generation
3. PDF via WeasyPrint
"""

import json
import html
from pathlib import Path
from typing import Any, Dict

# Paths
ROOT = Path(__file__).parent.parent  # Go up to RecipeDjerba root
RECIPES_DIR = ROOT / "data" / "recipes_multilingual"
IMAGES_DIR = ROOT / "data" / "images"
IMAGES_INDEX = IMAGES_DIR / "index.json"
OUTPUT_WEB = ROOT / "gen_book" / "output" / "web"
OUTPUT_PRINT = ROOT / "gen_book" / "output" / "print"
CSS_FILE = ROOT / "gen_book" / "cookbook.css"

# Load image index
_image_index_cache = None

def load_image_index() -> Dict:
    """Load the image index, caching it."""
    global _image_index_cache
    if _image_index_cache is None:
        if IMAGES_INDEX.exists():
            with open(IMAGES_INDEX, 'r', encoding='utf-8') as f:
                _image_index_cache = json.load(f)
        else:
            _image_index_cache = {}
    return _image_index_cache


def get_image_path(recipe_id: str, base_path: str = "", use_absolute: bool = False) -> str:
    """
    Get the image path for a recipe using the index system.
    Falls back to generated/ convention if index not available.
    
    Args:
        recipe_id: Recipe identifier
        base_path: Base path prefix (for relative paths)
        use_absolute: If True, return absolute path (for print/PDF)
        
    Returns:
        Image path string
    """
    index = load_image_index()
    
    # Try organized path first (current/recipe_id/dish.png)
    if recipe_id in index and index[recipe_id].get("dish_image"):
        # Check if organized file exists
        organized_path = IMAGES_DIR / "current" / recipe_id / "dish.png"
        if organized_path.exists():
            if use_absolute:
                return str(organized_path)
            else:
                # For web: relative path from base_path
                return f"{base_path}current/{recipe_id}/dish.png"
        
        # Fallback to generated/ if organized doesn't exist yet
        generated_path = IMAGES_DIR / "generated" / f"{recipe_id}_dish.png"
        if generated_path.exists():
            if use_absolute:
                return str(generated_path)
            else:
                return f"{base_path}generated/{recipe_id}_dish.png"
    
    # Fallback to generated/ convention
    if use_absolute:
        return str(IMAGES_DIR / "generated" / f"{recipe_id}_dish.png")
    return f"{base_path}generated/{recipe_id}_dish.png"

# Language configuration
LANGUAGES = ["he", "es", "ar", "en"]
LANG_LABELS = {
    "he": {"ingredients": "מצרכים", "instructions": "הוראות הכנה"},
    "es": {"ingredients": "Ingredientes", "instructions": "Instrucciones"},
    "ar": {"ingredients": "المكونات", "instructions": "طريقة التحضير"},
    "en": {"ingredients": "Ingredients", "instructions": "Instructions"},
}


def escape(text: str) -> str:
    """HTML escape text."""
    return html.escape(text)


def load_recipe(path: Path) -> dict[str, Any]:
    """Load a recipe JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_recipes() -> list[dict[str, Any]]:
    """Load all recipe JSON files from recipes directory."""
    recipes = []
    for path in sorted(RECIPES_DIR.glob("*.json")):
        recipes.append(load_recipe(path))
    return recipes


def get_title_size_class(name: str, lang: str) -> str:
    """
    Determine title size class based on name length and language.
    
    Returns:
        CSS class: "title-small", "title-medium", or "title-large"
    """
    length = len(name)
    
    # Language-specific thresholds (based on statistics)
    # Large: short names (bottom third), Medium: medium names (middle third), Small: long names (top third)
    thresholds = {
        "he": {"large": 6, "medium": 13},   # large <=6, medium 7-13, small >13
        "es": {"large": 8, "medium": 14},   # large <=8, medium 9-14, small >14
        "ar": {"large": 7, "medium": 13},   # large <=7, medium 8-13, small >13
        "en": {"large": 7, "medium": 13},   # large <=7, medium 8-13, small >13
    }
    
    threshold = thresholds.get(lang, {"large": 7, "medium": 13})
    
    if length <= threshold["large"]:
        return "title-large"
    elif length <= threshold["medium"]:
        return "title-medium"
    else:
        return "title-small"


def render_page1(recipe: dict, page_num: int) -> str:
    """Render Page 1: Title + Description + Meta footer."""
    name = recipe["name"]
    desc = recipe["description"]
    meta = recipe["meta"]
    
    # Get size classes for each language
    size_es = get_title_size_class(name["es"], "es")
    size_he = get_title_size_class(name["he"], "he")
    size_en = get_title_size_class(name["en"], "en")
    size_ar = get_title_size_class(name["ar"], "ar")
    
    return f'''
  <!-- PAGE {page_num}: NAME + DESCRIPTION -->
  <section class="page">
    <div class="page-inner">

      <div class="title-row">
        <div class="title-word lang-es {size_es}"><span>{escape(name["es"])}</span></div>
        <div class="title-word lang-he {size_he}"><span>{escape(name["he"])}</span></div>
        <div class="title-word lang-en {size_en}"><span>{escape(name["en"])}</span></div>
        <div class="title-word lang-ar {size_ar}"><span>{escape(name["ar"])}</span></div>
      </div>

      <div class="section">
        <div class="info-grid">
          <div class="info-item lang-he">
            <p>{escape(desc["he"])}</p>
          </div>
          <div class="info-item lang-es">
            <p>{escape(desc["es"])}</p>
          </div>
          <div class="info-item lang-ar">
            <p>{escape(desc["ar"])}</p>
          </div>
          <div class="info-item lang-en">
            <p>{escape(desc["en"])}</p>
          </div>
        </div>
      </div>

      <div class="meta-row meta-footer">
        <div class="meta-item">
          <span class="meta-label">Servings</span>
          <span class="meta-value">{escape(meta["servings"])}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Prep time</span>
          <span class="meta-value">{escape(meta["prep_time"])}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Cook time</span>
          <span class="meta-value">{escape(meta["cook_time"])}</span>
        </div>
        <div class="meta-item">
          <span class="meta-label">Difficulty</span>
          <span class="meta-value">{escape(meta["difficulty"])}</span>
        </div>
      </div>

      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_page2(recipe: dict, page_num: int, image_path: str) -> str:
    """Render Page 2: Full-bleed image."""
    alt_text = f'{recipe["name"]["en"]} dish'
    
    return f'''
  <!-- PAGE {page_num}: FULL-BLEED IMAGE -->
  <section class="page page--image">
    <div class="page-inner">
      <img class="hero-image" src="{image_path}" alt="{escape(alt_text)}">
      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_ingredients(ingredients: list[str]) -> str:
    """Render ingredients list."""
    items = "\n".join(f"              <li>{escape(ing)}</li>" for ing in ingredients)
    return f'''            <ul class="ingredients-list">
{items}
            </ul>'''


def render_simple_steps(steps: list[str], start_num: int) -> str:
    """Render simple steps (no variant label)."""
    steps_html = "\n".join(
        f'              <li class="step"><span class="step-num">{start_num + i}.</span>{escape(step)}</li>'
        for i, step in enumerate(steps)
    )
    
    return f'''            <ul class="steps-list">
{steps_html}
            </ul>'''


def render_variant_steps(variant: dict, lang: str, start_num: int) -> str:
    """Render steps for a variant (with variant label)."""
    variant_name = variant["name"][lang]
    steps = variant["steps"][lang]
    
    steps_html = "\n".join(
        f'              <li class="step"><span class="step-num">{start_num + i}.</span>{escape(step)}</li>'
        for i, step in enumerate(steps)
    )
    
    return f'''            <div class="variant-label">{escape(variant_name)}</div>
            <ul class="steps-list">
{steps_html}
            </ul>'''


def detect_overflow(recipe: dict, lang: str) -> str:
    """
    Detect if content is likely to overflow and return appropriate CSS class.
    Uses statistics-based thresholds (33rd and 66th percentiles).
    
    Args:
        recipe: Recipe dictionary
        lang: Language code
        
    Returns:
        CSS class name: "" (normal), "compact", or "tight"
    """
    ingredients = recipe["ingredients"][lang]
    variants = recipe.get("variants", [])
    simple_steps = recipe.get("steps", {}).get(lang, [])
    
    # Calculate total character count
    total_chars = sum(len(ing) for ing in ingredients)
    
    if variants:
        for variant in variants:
            total_chars += sum(len(step) for step in variant["steps"][lang])
            total_chars += len(variant["name"][lang])  # Variant label
    elif simple_steps:
        total_chars += sum(len(step) for step in simple_steps)
    
    # Statistics-based thresholds (33rd and 66th percentiles from actual data)
    # Normal: < 33rd percentile, Compact: 33rd-66th, Tight: > 66th
    thresholds = {
        "he": {"compact": 412, "tight": 499},  # 33rd: 412, 66th: 499
        "ar": {"compact": 402, "tight": 497},  # 33rd: 402, 66th: 497
        "es": {"compact": 521, "tight": 650},  # 33rd: 521, 66th: 650
        "en": {"compact": 465, "tight": 573},  # 33rd: 465, 66th: 573
    }
    
    threshold = thresholds.get(lang, {"compact": 465, "tight": 573})
    
    if total_chars >= threshold["tight"]:
        return "tight"
    elif total_chars >= threshold["compact"]:
        return "compact"
    else:
        return ""


def render_column(recipe: dict, lang: str) -> str:
    """Render a single language column with ingredients and instructions."""
    labels = LANG_LABELS[lang]
    ingredients = recipe["ingredients"][lang]
    
    # Detect overflow and get appropriate class
    overflow_class = detect_overflow(recipe, lang)
    column_class = f"column lang-{lang}"
    if overflow_class:
        column_class += f" {overflow_class}"
    
    # Render ingredients
    ing_html = render_ingredients(ingredients)
    
    # Render steps - handle both "variants" and simple "steps" formats
    variants = recipe.get("variants", [])
    simple_steps = recipe.get("steps", {}).get(lang, [])
    
    if variants:
        # Recipe has variants (multiple cooking methods)
        variants_html = []
        step_num = 1
        for variant in variants:
            variants_html.append(render_variant_steps(variant, lang, step_num))
            step_num += len(variant["steps"][lang])
        steps_combined = "\n\n".join(variants_html)
    elif simple_steps:
        # Recipe has simple steps (single method, no variants)
        steps_combined = render_simple_steps(simple_steps, 1)
    else:
        steps_combined = ""
    
    return f'''        <div class="{column_class}">
          <div>
            <div class="section-label">{escape(labels["ingredients"])}</div>
{ing_html}
          </div>

          <div>
            <div class="section-label">{escape(labels["instructions"])}</div>
{steps_combined}
          </div>
        </div>'''


def render_page3(recipe: dict, page_num: int) -> str:
    """Render Page 3: Spanish (left) + Hebrew (right)."""
    return f'''
  <!-- PAGE {page_num}: SPANISH + HEBREW -->
  <section class="page">
    <div class="page-inner">
      <div class="two-col">
{render_column(recipe, "es")}

{render_column(recipe, "he")}
      </div>

      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_page4(recipe: dict, page_num: int) -> str:
    """Render Page 4: English (left) + Arabic (right)."""
    return f'''
  <!-- PAGE {page_num}: ENGLISH + ARABIC -->
  <section class="page">
    <div class="page-inner">
      <div class="two-col">
{render_column(recipe, "en")}

{render_column(recipe, "ar")}
      </div>

      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_recipe(recipe: dict, start_page: int, image_path: str) -> str:
    """Render all 4 pages for a recipe."""
    pages = [
        render_page1(recipe, start_page),
        render_page2(recipe, start_page + 1, image_path),
        render_page3(recipe, start_page + 2),
        render_page4(recipe, start_page + 3),
    ]
    return "\n".join(pages)


def render_html(recipes: list[dict], css_content: str, image_base_path: str = "../images/", use_absolute: bool = False) -> str:
    """Render complete HTML document."""
    recipe_html_parts = []
    page_num = 1
    
    for recipe in recipes:
        image_path = get_image_path(recipe["id"], image_base_path, use_absolute=use_absolute)
        recipe_html_parts.append(render_recipe(recipe, page_num, image_path))
        page_num += 4  # Each recipe is 4 pages
    
    recipes_html = "\n".join(recipe_html_parts)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Four-Language Cookbook</title>

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Heebo:wght@400;600;700&family=Inter:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">

<style>
{css_content}
</style>
</head>
<body>

<div class="book">
{recipes_html}
</div>

</body>
</html>
'''


def render_single_recipe_html(recipe: dict, css_content: str, image_path: str) -> str:
    """Render HTML for a single recipe."""
    recipe_html = render_recipe(recipe, 1, image_path)
    recipe_name = recipe["name"]["en"]
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{escape(recipe_name)} – Four-Language Recipe</title>

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Heebo:wght@400;600;700&family=Inter:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&display=swap" rel="stylesheet">

<style>
{css_content}
</style>
</head>
<body>

<div class="book">
{recipe_html}
</div>

</body>
</html>
'''


def build_web(recipes: list[dict], css_content: str) -> None:
    """Build individual HTML pages for web deployment."""
    OUTPUT_WEB.mkdir(parents=True, exist_ok=True)
    
    for recipe in recipes:
        recipe_id = recipe["id"]
        image_path = get_image_path(recipe_id, "../images/generated/")
        html_content = render_single_recipe_html(recipe, css_content, image_path)
        
        output_path = OUTPUT_WEB / f"{recipe_id}.html"
        output_path.write_text(html_content, encoding="utf-8")
        print(f"  ✓ {output_path.name}")
    
    # Build index page
    build_index(recipes, css_content)


def build_index(recipes: list[dict], css_content: str) -> None:
    """Build index/table of contents page."""
    recipe_links = []
    for recipe in recipes:
        name_en = recipe["name"]["en"]
        recipe_id = recipe["id"]
        recipe_links.append(f'      <li><a href="{recipe_id}.html">{escape(name_en)}</a></li>')
    
    links_html = "\n".join(recipe_links)
    
    index_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Four-Language Cookbook</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

<style>
  :root {{
    --bg-page: #faf6f1;
    --bg-body: #e0dfda;
    --ink: #222222;
    --accent: #d9925b;
  }}
  
  body {{
    margin: 0;
    padding: 2rem;
    background: var(--bg-body);
    font-family: "Inter", system-ui, sans-serif;
    color: var(--ink);
  }}
  
  .container {{
    max-width: 600px;
    margin: 0 auto;
    background: var(--bg-page);
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }}
  
  h1 {{
    font-family: "Bona Nova", serif;
    font-size: 2.5rem;
    margin: 0 0 1.5rem;
    text-align: center;
  }}
  
  ul {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  
  li {{
    margin: 0.5rem 0;
  }}
  
  a {{
    color: var(--accent);
    text-decoration: none;
    font-size: 1.1rem;
  }}
  
  a:hover {{
    text-decoration: underline;
  }}
</style>
</head>
<body>

<div class="container">
  <h1>Cookbook</h1>
  <ul>
{links_html}
  </ul>
</div>

</body>
</html>
'''
    
    output_path = OUTPUT_WEB / "index.html"
    output_path.write_text(index_html, encoding="utf-8")
    print(f"  ✓ index.html")


def build_print(recipes: list[dict], css_content: str) -> None:
    """Build combined HTML for print/PDF."""
    OUTPUT_PRINT.mkdir(parents=True, exist_ok=True)
    
    # Use absolute paths for images in print version
    image_base_path = ""  # Will use absolute paths via use_absolute flag
    html_content = render_html(recipes, css_content, image_base_path, use_absolute=True)
    
    output_path = OUTPUT_PRINT / "full-cookbook.html"
    output_path.write_text(html_content, encoding="utf-8")
    print(f"  ✓ full-cookbook.html")


def build_pdf() -> None:
    """Generate PDF from HTML using WeasyPrint."""
    try:
        from weasyprint import HTML
    except ImportError:
        print("  ⚠ WeasyPrint not installed. Run: pip install weasyprint")
        print("    Skipping PDF generation.")
        return
    
    html_path = OUTPUT_PRINT / "full-cookbook.html"
    pdf_path = OUTPUT_PRINT / "full-cookbook.pdf"
    
    if not html_path.exists():
        print("  ⚠ full-cookbook.html not found. Build print first.")
        return
    
    print("  Generating PDF (this may take a moment)...")
    HTML(filename=str(html_path)).write_pdf(str(pdf_path))
    print(f"  ✓ full-cookbook.pdf")


def main():
    """Main build function."""
    print("Four-Language Cookbook Builder")
    print("=" * 40)
    
    # Load CSS
    css_content = CSS_FILE.read_text(encoding="utf-8")
    
    # Load recipes
    recipes = load_all_recipes()
    print(f"\nFound {len(recipes)} recipe(s)")
    
    if not recipes:
        print("No recipes found in recipes/ directory.")
        return
    
    # Build web
    print("\nBuilding web pages...")
    build_web(recipes, css_content)
    
    # Build print
    print("\nBuilding print version...")
    build_print(recipes, css_content)
    
    # Build PDF
    print("\nBuilding PDF...")
    build_pdf()
    
    print("\n" + "=" * 40)
    print("Build complete!")
    print(f"  Web:   {OUTPUT_WEB}/")
    print(f"  Print: {OUTPUT_PRINT}/")


if __name__ == "__main__":
    main()

