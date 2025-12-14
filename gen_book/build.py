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
import csv
import random
from pathlib import Path
from typing import Any, Dict, List

# Paths
ROOT = Path(__file__).parent.parent  # Go up to RecipeDjerba root
RECIPES_DIR = ROOT / "data" / "recipes_multilingual_v2"
IMAGES_DIR = ROOT / "data" / "images"
IMAGES_INDEX = IMAGES_DIR / "index.json"
INGREDIENTS_DIR = IMAGES_DIR / "ingredients" / "final"
INGREDIENTS_MATRIX = ROOT / "recipes_ingredients_matrix.csv"
OUTPUT_WEB = ROOT / "gen_book" / "output" / "web"
OUTPUT_PRINT = ROOT / "gen_book" / "output" / "print"
OUTPUT_FLIPBOOK = ROOT / "gen_book" / "flipbook"
CSS_FILE = ROOT / "gen_book" / "cookbook.css"

# Load image index
_image_index_cache = None
_ingredients_matrix_cache = None
_ingredient_name_to_file = None

def load_ingredients_matrix() -> Dict[str, List[str]]:
    """Load the ingredients matrix and return dict of recipe_id -> list of ingredient image filenames."""
    global _ingredients_matrix_cache, _ingredient_name_to_file
    
    if _ingredients_matrix_cache is not None:
        return _ingredients_matrix_cache
    
    _ingredients_matrix_cache = {}
    
    if not INGREDIENTS_MATRIX.exists():
        return _ingredients_matrix_cache
    
    # Create mapping from ingredient column names to image filenames
    # E.g., "Chickpeas" -> "chickpeas.png"
    def name_to_filename(name: str) -> str:
        """Convert ingredient column name to image filename."""
        # Remove parentheses content and clean up
        import re
        # "Flour (All-purpose, Bread, Whole Wheat)" -> "flour_all_purpose_bread_whole_wheat"
        cleaned = name.lower()
        cleaned = cleaned.replace(" / ", "_")
        cleaned = cleaned.replace("/", "_")
        cleaned = cleaned.replace(" ", "_")
        cleaned = cleaned.replace(",", "")
        cleaned = cleaned.replace("(", "")
        cleaned = cleaned.replace(")", "")
        cleaned = cleaned.replace("-", "_")
        cleaned = re.sub(r'_+', '_', cleaned)  # Multiple underscores to single
        cleaned = cleaned.strip('_')
        return f"{cleaned}.png"
    
    with open(INGREDIENTS_MATRIX, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        ingredient_names = header[2:]  # Skip recipe_id, recipe_name
        
        # Build name to file mapping
        _ingredient_name_to_file = {
            name: name_to_filename(name) 
            for name in ingredient_names
        }
        
        for row in reader:
            recipe_id = row[0]
            recipe_ingredients = []
            for i, val in enumerate(row[2:]):
                if val == '1':
                    img_file = _ingredient_name_to_file[ingredient_names[i]]
                    img_path = INGREDIENTS_DIR / img_file
                    if img_path.exists():
                        recipe_ingredients.append(str(img_path))
            _ingredients_matrix_cache[recipe_id] = recipe_ingredients
    
    return _ingredients_matrix_cache


def render_page_decorations(recipe_id: str, page_variant: str, use_absolute: bool = False) -> str:
    """
    Render decorative ingredient icons for a page.
    Each ingredient appears ONCE, with smart grid-based positioning.
    Both page 3 and page 4 use IDENTICAL positions (same seed).
    
    Args:
        recipe_id: Recipe identifier
        page_variant: 'hs' for Hebrew/Spanish page, 'ae' for Arabic/English page
        use_absolute: If True, use absolute file paths
        
    Returns:
        HTML string with positioned ingredient icons
    """
    ingredients_map = load_ingredients_matrix()
    ingredient_paths = ingredients_map.get(recipe_id, [])
    
    if not ingredient_paths:
        return ""
    
    # SAME seed for both pages - positions will be identical
    random.seed(hash(recipe_id))
    
    # Pre-planned grid positions for optimal spacing:
    # Empty areas: Top-right (50-100% x, 0-35% y) and Bottom-left (0-45% x, 65-95% y)
    #
    # Grid layout (6 slots total, 3 per area):
    # 
    #  Top-right area (above RTL column):
    #    [1]----[2]----[3]
    #       \       /
    #        -------
    #
    #  Bottom-left area (below LTR column):
    #        -------
    #       /       \
    #    [4]----[5]----[6]
    #
    grid_positions = [
        # Top-right area - 3 positions in a gentle arc
        (0.55, 0.06),   # Position 1: left side of top-right
        (0.73, 0.14),   # Position 2: center of top-right  
        (0.88, 0.04),   # Position 3: right side of top-right
        # Bottom-left area - 3 positions in a gentle arc
        (0.04, 0.72),   # Position 4: top of bottom-left
        (0.20, 0.82),   # Position 5: center of bottom-left
        (0.08, 0.92),   # Position 6: bottom of bottom-left
    ]
    
    # Select ingredients (deterministic for this recipe)
    num_icons = min(len(ingredient_paths), len(grid_positions))
    shuffled_ingredients = ingredient_paths.copy()
    random.shuffle(shuffled_ingredients)
    selected = shuffled_ingredients[:num_icons]
    
    # Assign ingredients to grid positions (1:1 mapping)
    icons_html = []
    for i, img_path in enumerate(selected):
        pos = grid_positions[i]
        left_pct = pos[0] * 100
        top_pct = pos[1] * 100
        
        # Subtle random transformations (deterministic per recipe)
        rotation = random.randint(-20, 20)
        skew_x = random.randint(-6, 6)
        skew_y = random.randint(-4, 4)
        scale = random.uniform(0.85, 1.15)
        
        # Use relative or absolute path
        if use_absolute:
            src = f"file://{img_path}"
        else:
            src = img_path
        
        transform = f"rotate({rotation}deg) skewX({skew_x}deg) skewY({skew_y}deg) scale({scale})"
        
        icons_html.append(f'''<img class="corner-ingredient" 
             src="{src}" 
             alt="" 
             style="left: {left_pct:.1f}%; top: {top_pct:.1f}%; transform: {transform};">''')
    
    return "\n        ".join(icons_html)


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


def get_image_path(recipe: dict, base_path: str = "", use_absolute: bool = False) -> str:
    """
    Get the image path for a recipe.
    
    Args:
        recipe: Recipe dict (may contain 'image' key with path)
        base_path: Base path prefix (for relative paths)
        use_absolute: If True, return absolute path (for print/PDF)
        
    Returns:
        Image path string
    """
    recipe_id = recipe.get("id", "unknown")
    
    # First, check if recipe has embedded image path (new v2 format)
    if "image" in recipe and recipe["image"]:
        embedded_path = recipe["image"]
        # Handle paths like "images/current/059_mhamsa/dish.png"
        if embedded_path.startswith("images/"):
            # Convert to absolute path from IMAGES_DIR
            relative_part = embedded_path.replace("images/", "", 1)
            abs_path = IMAGES_DIR / relative_part
            if abs_path.exists():
                if use_absolute:
                    return str(abs_path)
                else:
                    return f"{base_path}{relative_part}"
    
    # Try index-based lookup
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
    """Load all recipe JSON files from recipes directory, sorted by index."""
    recipes = []
    for path in RECIPES_DIR.glob("*.json"):
        recipes.append(load_recipe(path))
    # Sort by index field (default to 999 if missing)
    recipes.sort(key=lambda r: r.get("index", 999))
    return recipes


def get_title_size_class(name: str, lang: str) -> str:
    """
    Determine title size class based on name length and language.
    
    Returns:
        CSS class: "title-small", "title-medium", or "title-large"
    """
    length = len(name)
    
    # Language-specific thresholds - lowered to avoid overflow
    # Large: very short names, Medium: short names, Small: anything longer
    thresholds = {
        "he": {"large": 5, "medium": 9},    # more aggressive sizing
        "es": {"large": 6, "medium": 11},   # Spanish tends to be longer
        "ar": {"large": 5, "medium": 9},    
        "en": {"large": 6, "medium": 11},   
    }
    
    threshold = thresholds.get(lang, {"large": 7, "medium": 13})
    
    if length <= threshold["large"]:
        return "title-large"
    elif length <= threshold["medium"]:
        return "title-medium"
    else:
        return "title-small"


def render_title_page_ingredients(use_absolute: bool = False) -> str:
    """
    Render ALL ingredient images spread across the title page background.
    Uses a grid-based system to ensure no overlap.
    Each ingredient has random size, rotation, and slight position jitter.
    """
    # Get all ingredient image files
    ingredient_files = []
    if INGREDIENTS_DIR.exists():
        ingredient_files = sorted([f for f in INGREDIENTS_DIR.glob("*.png")])
    
    if not ingredient_files:
        return ""
    
    # Seed for reproducibility
    random.seed(42)
    
    # Create a grid layout for ~96 ingredients on an 8x8 inch page
    # Use a 10x10 grid = 100 cells, each ~0.8in
    grid_cols = 10
    grid_rows = 10
    cell_size = 0.8  # inches
    
    # Shuffle ingredients
    shuffled = ingredient_files.copy()
    random.shuffle(shuffled)
    
    icons_html = []
    
    for idx, img_path in enumerate(shuffled[:96]):  # Max 96 ingredients
        # Grid position
        row = idx // grid_cols
        col = idx % grid_cols
        
        # Base position (center of cell)
        base_left = col * cell_size + cell_size / 2
        base_top = row * cell_size + cell_size / 2
        
        # Random jitter within cell (keep inside cell bounds)
        jitter_x = random.uniform(-0.15, 0.15)
        jitter_y = random.uniform(-0.15, 0.15)
        
        left = base_left + jitter_x
        top = base_top + jitter_y
        
        # Random size (vary between 0.5 and 0.7 inches)
        size = random.uniform(0.5, 0.7)
        
        # Random rotation
        rotation = random.randint(-30, 30)
        
        # Random slight scale variation
        scale = random.uniform(0.9, 1.1)
        
        # Use absolute or relative path
        if use_absolute:
            src = f"file://{img_path}"
        else:
            src = str(img_path)
        
        transform = f"rotate({rotation}deg) scale({scale})"
        
        icons_html.append(f'''<img class="title-ingredient" 
             src="{src}" 
             alt=""
             style="left: {left:.2f}in; top: {top:.2f}in; width: {size:.2f}in; height: {size:.2f}in; transform: {transform};">''')
    
    return "\n        ".join(icons_html)


def render_front_matter(use_absolute: bool = False) -> str:
    """Render title page, copyright page, introduction (2 pages), and blank page."""
    
    # Generate ingredient background for title page
    ingredients_bg = render_title_page_ingredients(use_absolute)
    
    # Page 1: Title page - all four languages
    title_page = f'''
  <!-- TITLE PAGE -->
  <section class="page page--title">
    <div class="title-ingredients-bg">
        {ingredients_bg}
    </div>
    <div class="page-inner title-page-inner">
      <div class="title-page-content">
        <div class="book-titles">
          <div class="book-title-row">
            <span class="book-title book-title-he">מטבח מצפון</span>
            <span class="book-title book-title-ar">مطبخ بالأصل</span>
          </div>
          <div class="book-title-row">
            <span class="book-title book-title-en">Oriented Kitchen</span>
            <span class="book-title book-title-es">Cocina con Conciencia</span>
          </div>
        </div>
        
        <div class="book-subtitle-block">
          <div class="book-subtitle">Plant-Based Recipes from Djerba &amp; Tangier</div>
          <div class="book-subtitle">Recetas a Base de Plantas de Djerba y Tánger</div>
          <div class="book-subtitle book-subtitle-he">מתכונים מבוססי צמחים מג׳רבה וטנג׳יר</div>
          <div class="book-subtitle book-subtitle-ar">وصفات نباتية من جربة وطنجة</div>
        </div>
        
        <div class="title-divider"></div>
        
        <div class="family-lines">
          <div class="family-line">Cohen-Trabelsi · כהן-טרבלסי · كوهين-طرابلسي</div>
          <div class="family-origin">Djerba, Tunisia · ג׳רבה, תוניסיה · جربة، تونس</div>
        </div>
        <div class="family-lines">
          <div class="family-line">Kadoch-Muyal · קדוש-מויאל · قدوش-مويال</div>
          <div class="family-origin">Tangier, Morocco · טנג׳יר, מרוקו · طنجة، المغرب</div>
        </div>
        
        <div class="title-divider"></div>
        
        <div class="authors">David &amp; Enny Silver</div>
      </div>
    </div>
  </section>
'''
    
    # Page 2: Copyright page - centered, all languages
    copyright_page = '''
  <!-- COPYRIGHT PAGE -->
  <section class="page page--copyright">
    <div class="page-inner copyright-inner">
      <div class="copyright-content">
        <p class="copyright-text">© 2025 David Silver &amp; Enny Silver</p>
        <p class="copyright-text">Poughkeepsie, NY</p>
        <p class="copyright-text copyright-edition">First Edition · מהדורה ראשונה · Primera Edición · الطبعة الأولى</p>
        
        <div class="copyright-divider"></div>
        
        <p class="copyright-note">Preserving family traditions through plant-based cooking</p>
        <p class="copyright-note">לשמר את מסורת המשפחה דרך מטבח מבוסס צמחים</p>
        <p class="copyright-note">Preservando tradiciones familiares a través de la cocina vegetal</p>
        <p class="copyright-note copyright-note-ar">نحافظو على تقاليد العايلة من خلال الطبخ النباتي</p>
      </div>
    </div>
  </section>
'''
    
    # Page 3: Introduction - English (left) & Hebrew (right)
    intro_page_1 = '''
  <!-- INTRODUCTION PAGE 1: ENGLISH & HEBREW -->
  <section class="page page--intro">
    <div class="page-inner intro-inner">
      <div class="intro-title">Introduction · הקדמה</div>
      
      <div class="intro-columns">
        <div class="intro-col intro-text-en">
          <p>This cookbook preserves recipes from two North African Jewish family lines: the <strong>Cohen-Trabelsi</strong> family from the island of Djerba, Tunisia, and the <strong>Kadoch-Muyal</strong> family from Tangier, Morocco.</p>
          
          <p>Djerba's Jewish community was one of the oldest continuous Jewish settlements in the world. The recipes passed down through Ruth Cohen-Trabelsi carry the distinct flavors of Tunisian Jewish cooking—the slow-cooked Shabbat stews, the spiced fish dishes, the semolina-based sweets.</p>
          
          <p>Tangier's Jewish community thrived for centuries as a crossroads of cultures. The recipes from the Kadoch-Muyal family reflect Moroccan Jewish cuisine shaped by Andalusian heritage—the fragrant tagines, the flaky pastries, the preserved lemons and olives of the port city.</p>
          
          <p>All recipes have been adapted for plant-based cooking while preserving their authentic character. Each dish name includes its etymology—tracing roots through Arabic, Berber, Hebrew, and the Judeo-Arabic dialects of our grandparents.</p>
          
          <p>The book is presented in four languages: Hebrew, English, Spanish, and Maghrebi Arabic—reflecting the diaspora that scattered these communities, and the languages in which these recipes were shared, remembered, and written down.</p>
        </div>
        
        <div class="intro-col intro-text-he">
          <p>ספר בישול זה משמר מתכונים משני קווי משפחה יהודיים צפון-אפריקאיים: משפחת <strong>כהן-טרבלסי</strong> מהאי ג׳רבה שבתוניסיה, ומשפחת <strong>קדוש-מויאל</strong> מטנג׳יר שבמרוקו.</p>
          
          <p>הקהילה היהודית בג׳רבה הייתה אחת ההתיישבויות היהודיות הרציפות העתיקות בעולם. המתכונים שעברו דרך רות כהן-טרבלסי נושאים את הטעמים המיוחדים של הבישול היהודי-תוניסאי—התבשילים האיטיים של שבת, מנות הדגים המתובלות, והממתקים מבוססי הסולת.</p>
          
          <p>הקהילה היהודית בטנג׳יר פרחה במשך מאות שנים כצומת תרבויות. המתכונים ממשפחת קדוש-מויאל משקפים את המטבח היהודי-מרוקאי שעוצב על ידי המורשת האנדלוסית—הטאג׳ינים המבושמים, המאפים הפריכים, הלימונים והזיתים הכבושים של עיר הנמל.</p>
          
          <p>כל המתכונים הותאמו למטבח מבוסס צמחים תוך שמירה על אופיים המקורי. כל שם מנה כולל את האטימולוגיה שלו—מעקב אחר השורשים בערבית, ברברית, עברית, והניבים היהודיים-ערביים של סבינו.</p>
          
          <p>הספר מוגש בארבע שפות: עברית, אנגלית, ספרדית, וערבית מגרבית—המשקפות את התפוצות שפיזרו קהילות אלה, ואת השפות שבהן המתכונים שותפו, נזכרו ונכתבו.</p>
        </div>
      </div>
      
      <div class="page-num">iii</div>
    </div>
  </section>
'''
    
    # Page 4: Introduction - Spanish (left) & Arabic (right, Maghrebi dialect)
    intro_page_2 = '''
  <!-- INTRODUCTION PAGE 2: SPANISH & ARABIC -->
  <section class="page page--intro">
    <div class="page-inner intro-inner">
      <div class="intro-title">Introducción · مقدمة</div>
      
      <div class="intro-columns">
        <div class="intro-col intro-text-es">
          <p>Este libro de cocina preserva recetas de dos líneas familiares judías del norte de África: la familia <strong>Cohen-Trabelsi</strong> de la isla de Djerba, Túnez, y la familia <strong>Kadoch-Muyal</strong> de Tánger, Marruecos.</p>
          
          <p>La comunidad judía de Djerba fue uno de los asentamientos judíos continuos más antiguos del mundo. Las recetas transmitidas a través de Ruth Cohen-Trabelsi llevan los sabores distintivos de la cocina judía tunecina—los guisos lentos del Shabat, los platos de pescado especiados, los dulces a base de sémola.</p>
          
          <p>La comunidad judía de Tánger floreció durante siglos como cruce de culturas. Las recetas de la familia Kadoch-Muyal reflejan la cocina judía marroquí moldeada por la herencia andaluza—los aromáticos tagines, las hojaldradas pastillas, los limones y aceitunas en conserva de la ciudad portuaria.</p>
          
          <p>Todas las recetas han sido adaptadas para la cocina basada en plantas, preservando su carácter auténtico. Cada nombre de plato incluye su etimología—rastreando raíces a través del árabe, bereber, hebreo y los dialectos judeo-árabes de nuestros abuelos.</p>
          
          <p>El libro se presenta en cuatro idiomas: hebreo, inglés, español y árabe magrebí—reflejando la diáspora que dispersó estas comunidades, y los idiomas en los que estas recetas fueron compartidas, recordadas y escritas.</p>
        </div>
        
        <div class="intro-col intro-text-ar">
          <p>الكتاب هذا يحفظ وصفات من زوز عايلات يهود من شمال أفريقيا: عايلة <strong>كوهين-طرابلسي</strong> من جزيرة جربة في تونس، وعايلة <strong>قدوش-مويال</strong> من طنجة في المغرب.</p>
          
          <p>اليهود في جربة كانوا من أقدم الجماعات اليهودية في العالم. الوصفات اللي وصلتنا من روث كوهين-طرابلسي فيها نكهات المطبخ اليهودي التونسي—الطبيخ البطيء متاع السبت، أطباق الحوت المتبّلة، والحلويات اللي أساسها السميد.</p>
          
          <p>اليهود في طنجة عاشوا مئات السنين في ملتقى الثقافات. وصفات عايلة قدوش-مويال فيها نكهات المطبخ اليهودي المغربي متاع الأندلس—الطواجن المعطّرة، والبسطيلة المورّقة، والليمون والزيتون المخلّل متاع المرسى.</p>
          
          <p>كل الوصفات تبدّلت للطبخ النباتي وبقات على أصلها. كل اسم طبق فيه أصله—نتبّعو الجذور في العربية والأمازيغية والعبرية ولهجات أجدادنا.</p>
          
          <p>الكتاب مكتوب بأربع لغات: العبرية والإنجليزية والإسبانية والعربية المغاربية—يعكسو التفرّق اللي صار لهالجماعات، واللغات اللي فيها الوصفات اتشاركت واتذكرت واتكتبت.</p>
        </div>
      </div>
      
      <div class="page-num">iv</div>
    </div>
  </section>
'''
    
    # Page 5: Blank (so recipes start on right-hand page)
    blank_page = '''
  <!-- BLANK PAGE -->
  <section class="page page--blank">
    <div class="page-inner"></div>
  </section>
'''
    
    # Page 5: Vegan Substitutions Guide - English & Hebrew
    vegan_page_1 = '''
  <!-- VEGAN SUBSTITUTIONS PAGE 1: ENGLISH & HEBREW -->
  <section class="page page--intro">
    <div class="page-inner intro-inner">
      <div class="intro-title">Vegan Substitutions · תחליפים טבעוניים</div>
      
      <div class="intro-columns">
        <div class="intro-col intro-text-en">
          <p><strong>For Eggs:</strong></p>
          <p><em>Ground flax + water</em> — Mix 1 tbsp ground flax with 3 tbsp water, let sit 5 minutes. Best for baking where eggs add volume and binding.</p>
          <p><em>Applesauce</em> — Use ¼ cup per egg in cookies and cakes where egg is just another moisture source.</p>
          <p><em>Firm tofu</em> — Crumble to replace hard-boiled eggs in salads and pies. Add kala namak (black salt) for eggy sulfur flavor.</p>
          
          <p><strong>For Meat & Poultry:</strong></p>
          <p><em>TVP (Textured Vegetable Protein)</em> — Soak in hot broth. Works for any chicken or meat dish in any size pieces.</p>
          <p><em>Seitan</em> — Wheat gluten with a chewy, meaty texture. Best for stews and roasts.</p>
          <p><em>Mushrooms</em> — Lion's mane for chicken thighs, king oyster for steaks, maitake for pulled meat. Mycelium-based products for liver.</p>
          
          <p><strong>For Fish:</strong></p>
          <p><em>Tofu + seaweed</em> — Crumbled tofu with nori or wakame for fish-like appearance and ocean flavor.</p>
          <p><em>Yuba (tofu skin)</em> — Layered and marinated for a stringy texture similar to fish or intestine dishes.</p>
        </div>
        
        <div class="intro-col intro-text-he">
          <p><strong>תחליפי ביצים:</strong></p>
          <p><em>פשתן טחון + מים</em> — לערבב כף פשתן טחון עם 3 כפות מים, להשהות 5 דקות. מתאים לאפייה שבה הביצים מוסיפות נפח וקישור.</p>
          <p><em>רסק תפוחים</em> — להשתמש ברבע כוס לכל ביצה בעוגיות ועוגות שבהן הביצה היא רק עוד מקור לחות.</p>
          <p><em>טופו מוצק</em> — לפורר להחלפת ביצים קשות בסלטים ופשטידות. להוסיף קאלה נמק (מלח שחור) לטעם גופרתי של ביצה.</p>
          
          <p><strong>תחליפי בשר ועוף:</strong></p>
          <p><em>TVP (חלבון סויה מרקם)</em> — להשרות במרק חם. מתאים לכל מנת עוף או בשר בכל גודל חתיכות.</p>
          <p><em>סייטן</em> — גלוטן חיטה עם מרקם לעיס ובשרי. הכי טוב לתבשילים וצלי.</p>
          <p><em>פטריות</em> — ראש אריה לירכי עוף, מלך צדפות לסטייקים, מאיטאקה לבשר קרוע. מוצרי מיצליום לכבד.</p>
          
          <p><strong>תחליפי דגים:</strong></p>
          <p><em>טופו + אצות</em> — טופו מפורר עם נורי או וואקאמה למראה דגי וטעם אוקיינוס.</p>
          <p><em>יובה (קרום טופו)</em> — שכבות מתובלות למרקם גידי דומה לדגים.</p>
        </div>
      </div>
      
      <div class="page-num">v</div>
    </div>
  </section>
'''
    
    # Page 6: Vegan Substitutions Guide - Spanish & Arabic
    vegan_page_2 = '''
  <!-- VEGAN SUBSTITUTIONS PAGE 2: SPANISH & ARABIC -->
  <section class="page page--intro">
    <div class="page-inner intro-inner">
      <div class="intro-title">Sustitutos Veganos · البدائل النباتية</div>
      
      <div class="intro-columns">
        <div class="intro-col intro-text-es">
          <p><strong>Para Huevos:</strong></p>
          <p><em>Linaza molida + agua</em> — Mezcle 1 cda de linaza molida con 3 cdas de agua, deje reposar 5 minutos. Ideal para horneados donde los huevos agregan volumen.</p>
          <p><em>Puré de manzana</em> — Use ¼ taza por huevo en galletas y pasteles donde el huevo es solo humedad.</p>
          <p><em>Tofu firme</em> — Desmenuce para reemplazar huevos duros en ensaladas. Agregue kala namak para sabor a huevo.</p>
          
          <p><strong>Para Carne y Pollo:</strong></p>
          <p><em>Proteína de soja texturizada</em> — Remoje en caldo caliente. Funciona para cualquier plato de pollo o carne.</p>
          <p><em>Seitán</em> — Gluten de trigo con textura masticable y carnosa. Ideal para guisos y asados.</p>
          <p><em>Hongos</em> — Melena de león para muslos, champiñones rey para filetes, maitake para carne deshebrada.</p>
          
          <p><strong>Para Pescado:</strong></p>
          <p><em>Tofu + algas</em> — Tofu desmenuzado con nori para apariencia y sabor oceánico.</p>
          <p><em>Yuba (piel de tofu)</em> — En capas y marinada para textura fibrosa similar al pescado.</p>
        </div>
        
        <div class="intro-col intro-text-ar">
          <p><strong>بدائل البيض:</strong></p>
          <p><em>بذور الكتان المطحونة + ماء</em> — اخلط ملعقة كتان مطحون مع 3 ملاعق ماء، اتركها 5 دقائق. مثالي للخبز.</p>
          <p><em>صلصة التفاح</em> — استخدم ربع كوب لكل بيضة في الكعك والبسكويت.</p>
          <p><em>التوفو المتماسك</em> — فتتها لتحل محل البيض المسلوق في السلطات. أضف كالا نمك لنكهة البيض.</p>
          
          <p><strong>بدائل اللحوم والدجاج:</strong></p>
          <p><em>بروتين الصويا المركب</em> — انقعه في مرق ساخن. يعمل لأي طبق لحم أو دجاج.</p>
          <p><em>السيتان</em> — جلوتين القمح بقوام لحمي ومطاطي. الأفضل للطواجن.</p>
          <p><em>الفطر</em> — عرف الأسد لأفخاذ الدجاج، ملك المحار للستيك، مايتاكي للحم المبشور.</p>
          
          <p><strong>بدائل السمك:</strong></p>
          <p><em>التوفو + الأعشاب البحرية</em> — توفو مفتت مع نوري لمظهر ونكهة البحر.</p>
          <p><em>اليوبا (جلد التوفو)</em> — طبقات متبلة لقوام ليفي يشبه السمك.</p>
        </div>
      </div>
      
      <div class="page-num">vi</div>
    </div>
  </section>
'''
    
    return title_page + copyright_page + intro_page_1 + intro_page_2 + vegan_page_1 + vegan_page_2 + blank_page


def render_table_of_contents(recipes: list[dict]) -> str:
    """Render table of contents pages - quad-lingual."""
    # 30 per page (15 rows of 2 columns) - ensures no overflow
    recipes_per_page = 30
    
    toc_pages = []
    
    for page_idx in range(0, len(recipes), recipes_per_page):
        page_recipes = recipes[page_idx:page_idx + recipes_per_page]
        is_first_page = (page_idx == 0)
        
        # Build recipe list items - quad-lingual
        items_html = ""
        for i, recipe in enumerate(page_recipes):
            chapter_num = page_idx + i + 1
            name_en = recipe["name"]["en"]
            name_he = recipe["name"].get("he", "")
            name_es = recipe["name"].get("es", "")
            name_ar = recipe["name"].get("ar", "")
            
            items_html += f'''
          <div class="toc-item">
            <span class="toc-num">{chapter_num}.</span>
            <div class="toc-names">
              <span class="toc-name toc-name-en">{escape(name_en)}</span>
              <span class="toc-name toc-name-he">{escape(name_he)}</span>
              <span class="toc-name toc-name-es">{escape(name_es)}</span>
              <span class="toc-name toc-name-ar">{escape(name_ar)}</span>
            </div>
          </div>'''
        
        # Create page with header only on first page
        header = '<div class="toc-title">Contents · תוכן עניינים · Contenido · فهرس</div>' if is_first_page else ''
        
        toc_page = f'''
  <!-- TABLE OF CONTENTS PAGE -->
  <section class="page page--toc">
    <div class="page-inner toc-inner">
      {header}
      <div class="toc-list">
        {items_html}
      </div>
    </div>
  </section>
'''
        toc_pages.append(toc_page)
    
    return "".join(toc_pages)


def render_page1(recipe: dict, page_num: int, chapter_index: int = 1) -> str:
    """Render Page 1: Title + Description + Meta footer with chapter number."""
    name = recipe["name"]
    desc = recipe["description"]
    meta = recipe["meta"]
    
    # Get size classes for each language
    size_es = get_title_size_class(name["es"], "es")
    size_he = get_title_size_class(name["he"], "he")
    size_en = get_title_size_class(name["en"], "en")
    size_ar = get_title_size_class(name["ar"], "ar")
    
    return f'''
  <!-- PAGE {page_num}: NAME + DESCRIPTION (Chapter {chapter_index}) -->
  <section class="page">
    <div class="page-inner">

      <div class="title-block">
        <div class="title-row">
          <div class="title-word lang-es {size_es}"><span>{escape(name["es"])}</span></div>
          <div class="title-word lang-he {size_he}"><span>{escape(name["he"])}</span></div>
        </div>
        <div class="chapter-number"><span>{chapter_index}</span></div>
        <div class="title-row">
          <div class="title-word lang-en {size_en}"><span>{escape(name["en"])}</span></div>
          <div class="title-word lang-ar {size_ar}"><span>{escape(name["ar"])}</span></div>
        </div>
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


def get_content_length(recipe: dict, lang: str) -> int:
    """Calculate total content length for a recipe in a given language."""
    ingredients = recipe["ingredients"][lang]
    variants = recipe.get("variants", [])
    simple_steps = recipe.get("steps", {}).get(lang, [])
    
    # Calculate total character count
    total_chars = sum(len(ing) for ing in ingredients)
    
    # Count number of items too (each item takes a line)
    num_items = len(ingredients)
    
    if variants:
        for variant in variants:
            total_chars += sum(len(step) for step in variant["steps"][lang])
            total_chars += len(variant["name"][lang])
            num_items += len(variant["steps"][lang]) + 1  # +1 for variant label
    elif simple_steps:
        total_chars += sum(len(step) for step in simple_steps)
        num_items += len(simple_steps)
    
    # Weight by both character count and number of lines
    # Each line takes vertical space regardless of length
    weighted_score = total_chars + (num_items * 30)  # ~30 chars per line equivalent
    
    return weighted_score


def calculate_adaptive_style(recipe: dict, lang: str) -> str:
    """
    Calculate adaptive inline styles based on content length.
    Returns CSS style string with appropriate font-size and line-height.
    
    Uses smooth interpolation between min and max font sizes.
    """
    content_length = get_content_length(recipe, lang)
    
    # Define thresholds - content length to font size mapping
    # Short content (< 400 weighted chars) -> largest font (0.85rem)
    # Long content (> 1000 weighted chars) -> smallest font (0.68rem)
    min_content = 400
    max_content = 1000
    max_font = 0.85   # rem - for short recipes
    min_font = 0.68   # rem - for very long recipes
    
    # Calculate font size with smooth interpolation
    if content_length <= min_content:
        font_size = max_font
    elif content_length >= max_content:
        font_size = min_font
    else:
        # Linear interpolation
        ratio = (content_length - min_content) / (max_content - min_content)
        font_size = max_font - ratio * (max_font - min_font)
    
    # Line height scales inversely with font size (smaller fonts need less line height)
    # Range: 1.35 (for 0.78rem) to 1.2 (for 0.58rem)
    line_height = 1.35 - ((max_font - font_size) / (max_font - min_font)) * 0.15
    
    return f"font-size: {font_size:.3f}rem; line-height: {line_height:.2f};"


def render_column(recipe: dict, lang: str) -> str:
    """Render a single language column with ingredients and instructions."""
    labels = LANG_LABELS[lang]
    ingredients = recipe["ingredients"][lang]
    
    # Calculate adaptive styles based on content length
    adaptive_style = calculate_adaptive_style(recipe, lang)
    column_class = f"column lang-{lang}"
    
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
    
    return f'''        <div class="{column_class}" style="{adaptive_style}">
          <div>
            <div class="section-label">{escape(labels["ingredients"])}</div>
{ing_html}
          </div>

          <div>
            <div class="section-label">{escape(labels["instructions"])}</div>
{steps_combined}
          </div>
        </div>'''


def render_page3(recipe: dict, page_num: int, use_absolute: bool = False) -> str:
    """Render Page 3: Spanish (left) + Hebrew (right)."""
    recipe_id = recipe.get("id", "")
    decorations = render_page_decorations(recipe_id, "hs", use_absolute)
    
    return f'''
  <!-- PAGE {page_num}: SPANISH (left) + HEBREW (right) -->
  <section class="page">
    <div class="page-inner">
      <div class="corner-decorations">
        {decorations}
      </div>
      <div class="two-col">
{render_column(recipe, "es")}

{render_column(recipe, "he")}
      </div>

      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_page4(recipe: dict, page_num: int, use_absolute: bool = False) -> str:
    """Render Page 4: English (left) + Arabic (right)."""
    recipe_id = recipe.get("id", "")
    decorations = render_page_decorations(recipe_id, "ae", use_absolute)
    
    return f'''
  <!-- PAGE {page_num}: ENGLISH (left) + ARABIC (right) -->
  <section class="page">
    <div class="page-inner">
      <div class="corner-decorations">
        {decorations}
      </div>
      <div class="two-col">
{render_column(recipe, "en")}

{render_column(recipe, "ar")}
      </div>

      <div class="page-num">{page_num}</div>
    </div>
  </section>
'''


def render_recipe(recipe: dict, start_page: int, image_path: str, use_absolute: bool = False, chapter_index: int = 1) -> str:
    """Render all 4 pages for a recipe."""
    pages = [
        render_page1(recipe, start_page, chapter_index),
        render_page2(recipe, start_page + 1, image_path),
        render_page3(recipe, start_page + 2, use_absolute),
        render_page4(recipe, start_page + 3, use_absolute),
    ]
    return "\n".join(pages)


def render_html(recipes: list[dict], css_content: str, image_base_path: str = "../images/", use_absolute: bool = False) -> str:
    """Render complete HTML document."""
    # Render front matter (title, copyright, intro, blank)
    front_matter = render_front_matter(use_absolute=use_absolute)
    
    # Render table of contents
    toc = render_table_of_contents(recipes)
    
    recipe_html_parts = []
    page_num = 1  # Recipes start at page 1 (front matter uses roman numerals)
    
    for chapter_index, recipe in enumerate(recipes, start=1):
        image_path = get_image_path(recipe, image_base_path, use_absolute=use_absolute)
        recipe_html_parts.append(render_recipe(recipe, page_num, image_path, use_absolute, chapter_index))
        page_num += 4  # Each recipe is 4 pages
    
    recipes_html = front_matter + toc + "\n".join(recipe_html_parts)
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Four-Language Cookbook</title>

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Heebo:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">

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


def render_single_recipe_html(recipe: dict, css_content: str, image_path: str, chapter_index: int = 1) -> str:
    """Render HTML for a single recipe."""
    recipe_html = render_recipe(recipe, 1, image_path, chapter_index=chapter_index)
    recipe_name = recipe["name"]["en"]
    
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{escape(recipe_name)} – Four-Language Recipe</title>

<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Heebo:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">

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


def build_front_matter_pages(css_content: str) -> None:
    """Build individual front matter HTML pages for web deployment."""
    front_matter_html = render_front_matter(use_absolute=False)
    
    # Parse the front matter HTML to extract individual pages
    # The front matter contains 5 section.page elements
    import re
    
    # Split by section tags
    sections = re.findall(r'<section class="page[^"]*"[^>]*>.*?</section>', front_matter_html, re.DOTALL)
    
    page_names = ['_title', '_copyright', '_intro1', '_intro2', '_blank']
    page_titles = ['Silver Cooks', 'Copyright', 'Introduction', 'Introduction', '']
    
    for i, (section, name, title) in enumerate(zip(sections, page_names, page_titles)):
        if name == '_blank':
            continue  # Skip blank page for web
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title} – Silver Cooks</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Heebo:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600;700&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">

<style>
{css_content}
</style>
</head>
<body>

<div class="book">
{section}
</div>

</body>
</html>
'''
        output_path = OUTPUT_WEB / f"{name}.html"
        output_path.write_text(html_content, encoding="utf-8")
        print(f"  ✓ {name}.html")


def build_web(recipes: list[dict], css_content: str) -> None:
    """Build individual HTML pages for web deployment."""
    OUTPUT_WEB.mkdir(parents=True, exist_ok=True)
    
    # Build front matter pages first
    print("  Building front matter...")
    build_front_matter_pages(css_content)
    
    print("  Building recipe pages...")
    for i, recipe in enumerate(recipes, 1):
        recipe_id = recipe["id"]
        image_path = get_image_path(recipe, "../images/")
        html_content = render_single_recipe_html(recipe, css_content, image_path, chapter_index=i)
        
        output_path = OUTPUT_WEB / f"{recipe_id}.html"
        output_path.write_text(html_content, encoding="utf-8")
        if i % 10 == 0 or i == len(recipes):
            print(f"  [{i}/{len(recipes)}] ✓ {output_path.name}")
    
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
<link href="https://fonts.googleapis.com/css2?family=Bona+Nova:wght@400;700&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Sora:wght@400;600;700&display=swap" rel="stylesheet">

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


def build_pdf(num_recipes: int = 0) -> None:
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
    if num_recipes > 0:
        print(f"    Processing {num_recipes} recipes ({num_recipes * 4} pages)...")
        print("    (WeasyPrint is working, please wait...)")
    import sys
    sys.stdout.flush()  # Force output
    
    try:
        HTML(filename=str(html_path)).write_pdf(str(pdf_path))
        print(f"  ✓ full-cookbook.pdf ({pdf_path.stat().st_size / 1024 / 1024:.1f} MB)")
    except Exception as e:
        print(f"  ❌ PDF generation failed: {e}")
        raise


def build_flipbook_index(recipes: list[dict]) -> None:
    """Build search index JSON for flipbook."""
    OUTPUT_FLIPBOOK.mkdir(parents=True, exist_ok=True)
    
    search_data = {
        "recipes": []
    }
    
    for recipe in recipes:
        recipe_entry = {
            "id": recipe["id"],
            "names": recipe["name"],
            "ingredients": []
        }
        
        # Collect all ingredients (use English for search)
        if "ingredients" in recipe and "en" in recipe["ingredients"]:
            recipe_entry["ingredients"] = recipe["ingredients"]["en"]
        
        search_data["recipes"].append(recipe_entry)
    
    # Write search index
    index_path = OUTPUT_FLIPBOOK / "search-index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(search_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ search-index.json ({len(recipes)} recipes indexed)")


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
    build_pdf(len(recipes))
    
    # Build flipbook search index
    print("\nBuilding flipbook search index...")
    build_flipbook_index(recipes)
    
    print("\n" + "=" * 40)
    print("Build complete!")
    print(f"  Web:      {OUTPUT_WEB}/")
    print(f"  Print:    {OUTPUT_PRINT}/")
    print(f"  Flipbook: {OUTPUT_FLIPBOOK}/")


if __name__ == "__main__":
    import sys
    web_only = "--web-only" in sys.argv
    
    print("Four-Language Cookbook Builder")
    print("=" * 40)
    
    css_content = CSS_FILE.read_text(encoding="utf-8")
    recipes = load_all_recipes()
    print(f"\nFound {len(recipes)} recipe(s)")
    
    if not recipes:
        print("No recipes found.")
        sys.exit(1)
    
    print("\nBuilding web pages...")
    build_web(recipes, css_content)
    
    if not web_only:
        print("\nBuilding print version...")
        build_print(recipes, css_content)
        print("\nBuilding PDF...")
        build_pdf(len(recipes))
    
    print("\nBuilding flipbook search index...")
    build_flipbook_index(recipes)
    
    print("\n" + "=" * 40)
    print("Build complete!")

