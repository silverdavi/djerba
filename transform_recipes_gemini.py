#!/usr/bin/env python3
"""
Transform Safed Recipes to Comprehensive Multilingual Format
Uses Gemini 3 Pro to generate rich, culturally-aware recipe JSON files
Optionally generates cookbook images using Gemini 3 Pro Image

Input: Simple Hebrew recipe JSON from data/safed_recipes/
Output: Comprehensive 4-language JSON + PNG images
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai

# Configure Gemini
GEMINI_MODEL = "gemini-3-pro-preview"
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Paths
SAFED_RECIPES_DIR = Path("data/safed_recipes")
RECIPE_RESEARCH_DIR = Path("data/recipe_research")
OUTPUT_DIR = Path("data/recipes_multilingual")
IMAGES_DIR = Path("data/images/generated")

# Create output directories
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# VEGANIZATION PROMPT - Transform Hebrew recipe to vegan BEFORE translation
# ============================================================================
VEGAN_SYSTEM_PROMPT = """אתה מומחה לבישול טבעוני ולהתאמת מתכונים מסורתיים לגרסאות טבעוניות.
המשימה שלך היא להמיר מתכון עברי למתכון טבעוני תוך שמירה על הטעם והמרקם המסורתי.

כללי ההמרה:

1. **בשר** (עוף, בקר, כבש, דגים):
   - בשר טחון → סויה מפוררת / טופו מפורר
   - נתחי בשר → סייטן / טמפה / טופו מוצק
   - נקניקיות → נקניקיות טבעוניות (סויה)
   - דגים → טופו מעושן / "דגים" מאצות

2. **ביצים** - לפי השימוש:
   - בעוגות/מאפים מתוקים → רסק תפוחים (3 כפות = ביצה) או בננה מועכת
   - במרנג/קצפת → אקווה פאבה (מי חומוס מהפחית)
   - בקישים/פשטידות/פריקסה → קמח חומוס מעורבב במים (3 כפות קמח + 3 כפות מים = ביצה)
   - בקציצות/קבב → קמח חומוס או פשתן טחון
   - בציפוי לטיגון → קמח חומוס + מים

3. **מוצרי חלב**:
   - חמאה → שמן קוקוס / מרגרינה טבעונית
   - שמנת → שמנת קוקוס / שמנת שקדים
   - גבינה → גבינה טבעונית (קשיו/שקדים)

4. **מרק בשר/עוף**:
   - מרק ירקות עשיר + שמרי בירה תזונתיים

שמור על אותו מבנה JSON. החזר רק את ה-JSON המעודכן."""

VEGAN_USER_PROMPT = """המר את המתכון הבא לגרסה טבעונית מלאה.
שמור על כל שאר המידע (שם, הוראות הכנה כלליות) אבל עדכן את:
1. רשימת המצרכים - החלף מוצרים מן החי בתחליפים טבעוניים
2. הוראות ההכנה - עדכן אם יש שינוי בטכניקת הבישול

המתכון המקורי:
```json
{recipe_json}
```

החזר רק JSON תקין, ללא markdown."""

# Image generator (lazy loaded)
_image_generator = None


def veganize_recipe(input_recipe: dict, max_retries: int = 3) -> dict:
    """Transform a Hebrew recipe to vegan version (Step 1)."""
    
    recipe_name = input_recipe.get("name_hebrew", input_recipe.get("id", "unknown"))
    print(f"  🌱 Veganizing: {recipe_name}")
    
    prompt = VEGAN_USER_PROMPT.format(
        recipe_json=json.dumps(input_recipe, ensure_ascii=False, indent=2)
    )
    
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=VEGAN_SYSTEM_PROMPT
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.5 + (attempt * 0.1),  # Slightly vary temperature on retry
                    max_output_tokens=4096,
                )
            )
            
            # Check if response has valid content
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    print(f"    ⚠️  Empty response, retrying ({attempt + 2}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    # If all retries fail, return original recipe (already vegan enough or skip veganization)
                    print(f"    ⚠️  Could not veganize, using original recipe")
                    return input_recipe
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            result = json.loads(response_text)
            print(f"    ✅ Veganized successfully")
            return result
            
        except ValueError as e:
            if "finish_reason" in str(e) and attempt < max_retries - 1:
                print(f"    ⚠️  Safety filter triggered, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            elif attempt == max_retries - 1:
                print(f"    ⚠️  Could not veganize (safety filter), using original recipe")
                return input_recipe
            raise
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"    ⚠️  JSON parse error, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            else:
                print(f"    ⚠️  Could not parse veganized recipe, using original")
                return input_recipe
    
    return input_recipe


def get_image_generator():
    """Lazy load the image generator."""
    global _image_generator
    if _image_generator is None:
        from generate_cookbook_images import CookbookImageGenerator
        _image_generator = CookbookImageGenerator(output_dir=str(IMAGES_DIR))
    return _image_generator


def generate_recipe_images(recipe_data: dict) -> dict:
    """Generate dish image for a recipe (vegan version)."""
    gen = get_image_generator()
    
    recipe_id = recipe_data.get('id', 'unknown')
    name = recipe_data.get('name', {})
    description = recipe_data.get('description', {})
    
    dish_name = name.get('en', recipe_id) if isinstance(name, dict) else str(name)
    dish_desc = description.get('en', '') if isinstance(description, dict) else str(description)
    
    # Add vegan context to description
    vegan_desc = f"Vegan version of {dish_desc}" if dish_desc else f"Vegan {dish_name}"
    
    results = {}
    
    # Generate dish image
    try:
        dish_path = IMAGES_DIR / f"{recipe_id}.png"
        result = gen.generate_dish_image(
            dish_name=dish_name,
            description=vegan_desc,
            output_path=str(dish_path),
            additional_styling="Plant-based, vegan dish with no animal products visible"
        )
        results['dish'] = str(result)
        print(f"    🖼️  Image saved: {recipe_id}.png")
    except Exception as e:
        print(f"    ⚠️  Image generation failed: {e}")
        results['error'] = str(e)
    
    return results

# System prompt for recipe transformation
SYSTEM_PROMPT = """You are an expert translator for a VEGAN Tunisian-Djerban Jewish cookbook. You translate recipes into 4 languages: Hebrew, Arabic (Tunisian Derja), Spanish, and English.

NOTE: All recipes have already been veganized (plant-based substitutes for meat, eggs, dairy). Translate the vegan ingredients accurately.

CRITICAL RULES - THIS IS FOR A PRINTED COOKBOOK WITH LIMITED SPACE:

1. **DISH NAMES MUST BE SHORT** - Just the dish name, nothing else:
   - Hebrew: "מחמסה" (NOT "מחמסה - פתיתים תוניסאיים")
   - English: "Mhamsa" (NOT "Mhamsa (Traditional Tunisian Pearl Pasta)")
   - Spanish: "La Mhamsa" or "Mhamsa" (article optional)
   - Arabic: "المحمصة" (the traditional name)

2. **ID must be simple**: lowercase English transliteration (e.g., "mhamsa", "harimi", "couscous")

3. **Description**: 2-3 sentences max. Include what the dish is, how it's served, and etymology of name.

4. **Ingredients**: Keep concise. "1 בצל קטן" not "1 בצל קטן, קצוץ דק"

5. **Steps**: Clear and practical, 3-6 steps typically.

6. **Arabic**: Use Tunisian Derja dialect - words like مرقة، طنجرة، نفوّح، كأس، مغرفة، etc.

FOLLOW THE EXACT STRUCTURE OF THE TEMPLATE. No extra fields, no verbose names."""

USER_PROMPT_TEMPLATE = """Transform this Hebrew recipe to match EXACTLY this template format:

## TEMPLATE (mhamsa.json) - FOLLOW THIS EXACTLY:
```json
{{
  "id": "mhamsa",
  "image": "mhamsa.png",
  "meta": {{
    "servings": "3–4",
    "prep_time": "10 min",
    "cook_time": "20 min",
    "difficulty": "Easy"
  }},
  "name": {{
    "he": "מחמסה",
    "es": "La Mhamsa",
    "ar": "المحمصة",
    "en": "Mhamsa"
  }},
  "description": {{
    "he": "מחמסה היא מנה ביתית, אהובה על ילדים, הנפוצה בגירסה יבשה או מרקית, ולעיתים בתוספת פרוסות נקניקייה בתבשיל היבש או המרקי האדום; היא מוכנה תוך פחות מרבע שעה. השם נגזר מהמילה הערבית \"מַחַמַּצַה\" (קלויה), ומתייחס לשיטה המסורתית של קליית פתיתי הסולת כדי לשמרם ולהעמיק את טעמם האגוזי.",
    "es": "...",
    "ar": "...",
    "en": "..."
  }},
  "ingredients": {{
    "he": ["1 בצל קטן", "1 כוס מחמסה (פתיתים)", "1 כף פפריקה מתוקה", "..."],
    "es": ["1 cebolla pequeña", "1 taza de Mhamsa (cuscús israelí / perlas de pasta)", "..."],
    "ar": ["1 بصلة صغيرة", "1 كأس محمصة (بركوكش / بتيتيم)", "..."],
    "en": ["1 small onion", "1 cup Mhamsa (Israeli couscous / pearl pasta)", "..."]
  }},
  "steps": {{
    "he": ["מטגנים בצל קטן עד שהוא נהיה שקוף.", "..."],
    "es": ["Sofreír una cebolla pequeña hasta que esté transparente.", "..."],
    "ar": ["قلّي بصلة صغيرة في الزيت حتى تذبل وتصبح شفافة.", "..."],
    "en": ["Sauté a small onion until transparent.", "..."]
  }}
}}
```

## IF RECIPE HAS VARIANTS (like dry vs sauce version), replace "steps" with:
```json
"variants": [
  {{
    "name": {{"he": "מחמסה יבשה", "es": "Mhamsa seca", "ar": "للمحمصة الشايحة (الجافة)", "en": "Dry Mhamsa"}},
    "steps": {{"he": [...], "es": [...], "ar": [...], "en": [...]}}
  }}
]
```

## INPUT RECIPE TO TRANSFORM:
```json
{input_recipe}
```

{history_context}

## CRITICAL RULES:
1. **NAME = JUST THE DISH NAME** - "חרימי" not "חרימי (תבשיל דגים)"
2. **ID = simple lowercase** - "harimi" not "harimi_fish_stew"  
3. **Description = 2-3 sentences** - what it is + etymology/origin
4. **Ingredients = concise** - quantities but no extra prep notes
5. **Arabic = Tunisian Derja** - use طنجرة، مرقة، كأس، نفوّح، etc.

Return ONLY valid JSON, no markdown blocks.
"""

def load_history_for_recipe(recipe_name_hebrew: str) -> str:
    """Load research history file if available."""
    # Try various filename patterns
    patterns = [
        f"{recipe_name_hebrew}_history.md",
        f"*{recipe_name_hebrew}*_history.md",
    ]
    
    # Also try English transliterations
    transliterations = {
        "מחמסה": "mahmessa",
        "קוסקוס": "couscous",
        "טפינה": "tefina",
        "בריקות": "brik",
        "חרימי": "harimi",
        "שקשוקה": "shakshuka",
        "יויו": "yoyo",
        "בשישה": "beshisha",
        "בקילה": "bikila",
        "מרמומה": "marmouma",
        "שמיד": "shmid",
        "קטעה": "kta'a",
        "שפינגות": "shpingeot",
        "ברודו": "brodo",
        "פריקסה": "frikaseh",
        "סופגניות": "sufganiyot",
        "לביבות": "potato_latkes",
        "דווידה": "davidah",
        "מחשי": "mahshi",
        "מעקוד": "maqoud",
        "אדמשושה": "admeshushah",
        "תירשי": "tirshi",
        "קוקלות": "kuklot",
        "שניצל": "chicken_schnitzel",
    }
    
    # Check for direct match
    for file in RECIPE_RESEARCH_DIR.glob("*_history.md"):
        name_lower = recipe_name_hebrew.lower()
        file_stem = file.stem.lower()
        
        if name_lower in file_stem:
            return file.read_text(encoding='utf-8')
        
        # Check transliteration
        if name_lower in transliterations:
            trans = transliterations[name_lower]
            if trans in file_stem:
                return file.read_text(encoding='utf-8')
    
    return ""


def transform_recipe(input_recipe: dict) -> dict:
    """Transform a single recipe: Veganize first, then translate to 4 languages."""
    
    recipe_name = input_recipe.get("name_hebrew", input_recipe.get("id", "unknown"))
    print(f"  Processing: {recipe_name}")
    
    # STEP 1: Veganize the Hebrew recipe
    vegan_recipe = veganize_recipe(input_recipe)
    
    # Small delay between API calls
    time.sleep(1)
    
    # STEP 2: Translate to 4 languages
    print(f"  🌍 Translating to 4 languages...")
    
    # Load history context if available
    history = load_history_for_recipe(recipe_name)
    history_context = ""
    if history:
        history_context = f"""## HISTORICAL/CULTURAL RESEARCH (use this for the description):
```markdown
{history}
```
"""
        print(f"    📚 Found historical research")
    else:
        print(f"    ⚠️  No historical research found - will generate from culinary knowledge")
    
    # Build the prompt with VEGAN recipe
    prompt = USER_PROMPT_TEMPLATE.format(
        input_recipe=json.dumps(vegan_recipe, ensure_ascii=False, indent=2),
        history_context=history_context
    )
    
    # Call Gemini
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=SYSTEM_PROMPT
    )
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            max_output_tokens=8192,
        )
    )
    
    # Parse the response
    response_text = response.text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
        response_text = re.sub(r'\n?```$', '', response_text)
    
    try:
        result = json.loads(response_text)
        return result
    except json.JSONDecodeError as e:
        print(f"    ❌ JSON parse error: {e}")
        print(f"    Response preview: {response_text[:500]}...")
        raise


def process_all_recipes(start_from: int = 0, limit: int = None, with_images: bool = False):
    """Process all recipes in the safed_recipes directory."""
    
    # Get all recipe files sorted
    recipe_files = sorted(SAFED_RECIPES_DIR.glob("*.json"))
    
    if limit:
        recipe_files = recipe_files[start_from:start_from + limit]
    else:
        recipe_files = recipe_files[start_from:]
    
    print(f"🍳 Processing {len(recipe_files)} recipes...")
    print(f"   Model: {GEMINI_MODEL}")
    print(f"   Output: {OUTPUT_DIR}/")
    if with_images:
        print(f"   Images: {IMAGES_DIR}/")
    print()
    
    results = {
        "success": [],
        "failed": [],
        "images": []
    }
    
    for i, recipe_file in enumerate(recipe_files, 1):
        print(f"\n[{i}/{len(recipe_files)}] Processing: {recipe_file.name}")
        
        try:
            # Load input recipe
            with open(recipe_file, 'r', encoding='utf-8') as f:
                input_recipe = json.load(f)
            
            # Transform
            output_recipe = transform_recipe(input_recipe)
            
            # Generate output filename
            recipe_id = output_recipe.get("id", recipe_file.stem)
            output_file = OUTPUT_DIR / f"{recipe_id}.json"
            
            # Save JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_recipe, f, ensure_ascii=False, indent=2)
            
            print(f"    ✅ Saved: {output_file.name}")
            results["success"].append(recipe_file.name)
            
            # Generate image if requested
            if with_images:
                img_result = generate_recipe_images(output_recipe)
                if 'dish' in img_result:
                    results["images"].append(recipe_id)
            
            # Rate limiting - be nice to the API
            if i < len(recipe_files):
                time.sleep(2)
                
        except Exception as e:
            print(f"    ❌ Failed: {e}")
            results["failed"].append({
                "file": recipe_file.name,
                "error": str(e)
            })
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TRANSFORMATION SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Recipes: {len(results['success'])}")
    if with_images:
        print(f"🖼️  Images: {len(results['images'])}")
    print(f"❌ Failed: {len(results['failed'])}")
    
    if results["failed"]:
        print("\nFailed recipes:")
        for fail in results["failed"]:
            print(f"  - {fail['file']}: {fail['error']}")
    
    return results


def process_single_recipe(filename: str, with_images: bool = False):
    """Process a single recipe by filename."""
    recipe_file = SAFED_RECIPES_DIR / filename
    
    if not recipe_file.exists():
        print(f"❌ File not found: {recipe_file}")
        return None
    
    print(f"🍳 Processing single recipe: {filename}")
    print(f"   Model: {GEMINI_MODEL}")
    if with_images:
        print(f"   Images: {IMAGES_DIR}/")
    
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            input_recipe = json.load(f)
        
        output_recipe = transform_recipe(input_recipe)
        
        recipe_id = output_recipe.get("id", recipe_file.stem)
        output_file = OUTPUT_DIR / f"{recipe_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_recipe, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ Saved: {output_file}")
        
        # Generate image if requested
        if with_images:
            generate_recipe_images(output_recipe)
        
        print(f"\nPreview of output:")
        print(json.dumps(output_recipe, ensure_ascii=False, indent=2)[:2000])
        
        return output_recipe
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Transform Safed recipes to multilingual format")
    parser.add_argument("--single", "-s", help="Process single recipe file (e.g., '00_מחמסה.json')")
    parser.add_argument("--start", type=int, default=0, help="Start from recipe index N")
    parser.add_argument("--limit", "-n", type=int, help="Process only N recipes")
    parser.add_argument("--list", "-l", action="store_true", help="List available recipes")
    parser.add_argument("--with-images", "-i", action="store_true", help="Also generate dish images")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available recipes:")
        for i, f in enumerate(sorted(SAFED_RECIPES_DIR.glob("*.json"))):
            print(f"  {i:2d}. {f.name}")
        sys.exit(0)
    
    if args.single:
        process_single_recipe(args.single, with_images=args.with_images)
    else:
        process_all_recipes(start_from=args.start, limit=args.limit, with_images=args.with_images)

