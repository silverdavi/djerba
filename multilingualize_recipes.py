#!/usr/bin/env python3
"""
Multilingualize Canonical Recipes

Takes structured English canonical recipes from data/recipes_canonical/
and generates 4-language versions for the cookbook.

Uses Gemini 3 Pro Preview exclusively (no fallbacks).

Input: Canonical English JSON with structured ingredients
Output: Multilingual JSON (Hebrew, English, Spanish, Arabic)
"""

import os
import sys
import json
import time
import re
from pathlib import Path
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

load_dotenv()

import google.generativeai as genai

# ============================================================================
# CONFIGURATION - NEVER CHANGE MODEL
# ============================================================================
GEMINI_MODEL = "gemini-3-pro-preview"
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Paths
CANONICAL_DIR = Path("data/recipes_canonical")
OUTPUT_DIR = Path("data/recipes_multilingual_v2")
DICTIONARY_FILE = Path("data/ingredients_dictionary.json")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Thread-safe helpers
_progress_lock = Lock()
_progress_count = 0

def vprint(*args, **kwargs):
    """Print with immediate flush for real-time output."""
    print(*args, **kwargs, flush=True)


def load_ingredients_dictionary():
    """Load the ingredients dictionary for translation reference."""
    try:
        with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("ingredients", {})
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


# ============================================================================
# MULTILINGUALIZATION SYSTEM PROMPT
# ============================================================================
MULTILINGUAL_SYSTEM_PROMPT = """You are an expert translator for a Djerban Jewish family cookbook.
You translate recipes from English to 4 languages: Hebrew, Arabic (Tunisian Derja), Spanish, and English.

## OUTPUT FOR HTML - CRITICAL FORMATTING RULES
1. NO MARKDOWN SYMBOLS - no asterisks (*), no underscores (_), no hashtags (#)
2. Plain text only - this goes directly into HTML
3. Use quotation marks ("") for foreign words if emphasis needed, NOT italics

## FAMILY HERITAGE CONTEXT
This cookbook preserves recipes from the Silver family:
- David's side: Cohen family from Djerba, Tunisia (Tunisian-Djerban Jewish tradition)
- Enny's side: Kadoch and Maloul families from Tangier, Morocco (Moroccan Jewish tradition)

## DISH NAME RULES - VERY IMPORTANT

### Traditional/Cultural Names (ALWAYS TRANSLITERATE):
These names MUST be transliterated in all languages, never translated:
- Mhamsa, Adafina, Banatage, Bkaila, Brodo, Brikot, Chraime/Hraime
- Dwida, Tfina, Yoyo, Sfenj, Mahshi, Ma'akouda, Tirshi, Msiyar
- Adamshusha, Nazha, Kouklot, Cujada, Bshisha, Shakshuka
- Example: "Banatage" stays "Banatage" in Spanish, NOT "croquetas"

### International Names (USE TARGET LANGUAGE):
- "Pancakes" → Hebrew: פנקייק, Spanish: Panqueques (NOT tortitas), Arabic: بانكيك
- "Chocolate Cake" → Hebrew: עוגת שוקולד, Spanish: Pastel de Chocolate, Arabic: كيكة شوكولاتة
- "Pizza" stays "Pizza" in all languages

## ARABIC - TUNISIAN DERJA RULES

Use Tunisian Derja (Judeo-Arabic) vocabulary, NOT Modern Standard Arabic:
- Egg = عظمة (adma) NOT بيضة (beyda)
- Pot = طنجرة (tanjra)
- Cup = كأس (kes)
- Tablespoon = مغرفة (maghrfa)
- To cook = نطيّب (ntayyeb)
- To fry = نقلي (nqli)
- To sauté = نفوّح (nfawwah)
- Broth/sauce = مرقة (marga)
- Potato = بطاطا (batata)
- Tomato = طماطم (tmatem)
- Onion = بصل (bsal)

## INGREDIENTS FORMAT - USE THE MEASUREMENTS FIELD

Each ingredient has a "measurements" object with 4 unit systems:
- metric: { value, unit } - grams (g), milliliters (ml)
- imperial: { value, unit } - ounces (oz), fluid ounces (fl oz)
- volume: { value, unit } - cups, tbsp, tsp
- original: { value, unit } - the original amount

**Use these unit systems by locale:**
- Hebrew: Use METRIC (g, ml) - e.g., "250 גרם קמח"
- Spanish: Use METRIC (g, ml) - e.g., "250 g de harina"
- Arabic: Use VOLUME (cups/tbsp) - Tunisian style - e.g., "2 كيسان فرينة"
- English: Use VOLUME (cups/tbsp) for baking, METRIC or IMPERIAL for cooking

**Format examples:**
- Hebrew: "250 גרם קמח, 3 כפות שמן"
- Spanish: "250 g de harina, 3 cucharadas de aceite"
- Arabic: "2 كيسان فرينة، 3 مغارف زيت"
- English: "2 cups flour, 3 tbsp oil"

**For count items (onions, eggs):** Use the original value
- Hebrew: "2 בצלים, קצוצים"
- Arabic: "2 بصلات، مقصوصين" or "2 عظمات" (for eggs)

**For "to taste" (unit is "to_taste" or null):**
- Hebrew: "מלח לפי הטעם"
- Arabic: "ملح حسب الذوق"
- Spanish: "Sal al gusto"
- English: "Salt to taste"

## DESCRIPTION
Use the intro_paragraph from the canonical recipe and translate it.
Keep it 40-60 words. Include etymology naturally (no asterisks for emphasis).

Return ONLY valid JSON."""


def strip_markdown(text: str) -> str:
    """Remove markdown formatting from text."""
    if not isinstance(text, str):
        return text
    # Remove bold/italic asterisks
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
    # Remove underscore emphasis
    text = re.sub(r'_{1,2}([^_]+)_{1,2}', r'\1', text)
    # Remove backticks
    text = re.sub(r'`([^`]+)`', r'\1', text)
    return text


def strip_markdown_from_result(data: dict) -> dict:
    """Recursively strip markdown from all string values in result."""
    if isinstance(data, dict):
        return {k: strip_markdown_from_result(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [strip_markdown_from_result(item) for item in data]
    elif isinstance(data, str):
        return strip_markdown(data)
    return data


MULTILINGUAL_USER_PROMPT = """Translate this canonical recipe to 4 languages for an HTML cookbook.

## CANONICAL RECIPE:
```json
{canonical_recipe}
```

## CRITICAL: USE THE measurements FIELD FOR EACH INGREDIENT

Each ingredient has a "measurements" object. Use the RIGHT unit system for each language:
- Hebrew: measurements.metric (e.g., 250 גרם, 45 מ"ל)
- Spanish: measurements.metric (e.g., 250 g, 45 ml)
- Arabic: measurements.volume (e.g., 2 كيسان, 3 مغارف) - Tunisian style
- English: measurements.volume (e.g., 2 cups, 3 tbsp)

For count items (where metric/imperial/volume are null), use measurements.original.

## OUTPUT STRUCTURE (follow exactly):
```json
{{
  "id": "{recipe_id}",
  "image": "{image_path}",
  "meta": {{
    "servings": "{servings}",
    "prep_time": "{prep_time}",
    "cook_time": "{cook_time}",
    "difficulty": "{difficulty}"
  }},
  "name": {{
    "he": "Hebrew name (use name_hebrew from source)",
    "es": "Spanish name",
    "ar": "Arabic name (Tunisian transliteration for cultural dishes)",
    "en": "English name"
  }},
  "description": {{
    "he": "Hebrew description (translate intro_paragraph, NO markdown)",
    "es": "Spanish description (NO markdown)",
    "ar": "Tunisian Derja description (NO markdown)",
    "en": "English description (intro_paragraph, NO markdown)"
  }},
  "ingredients": {{
    "he": ["250 גרם קמח, מנופה", "45 מ\"ל שמן", "2 בצלים, קצוצים"],
    "es": ["250 g de harina, tamizada", "45 ml de aceite", "2 cebollas, picadas"],
    "ar": ["2 كيسان فرينة، منخولة", "3 مغارف زيت", "2 بصلات، مقصوصين"],
    "en": ["2 cups flour, sifted", "3 tbsp oil", "2 onions, diced"]
  }},
  "steps": {{
    "he": ["step 1 in Hebrew", "step 2..."],
    "es": ["step 1 in Spanish", "step 2..."],
    "ar": ["step 1 in Tunisian Arabic", "step 2..."],
    "en": ["step 1 in English", "step 2..."]
  }}
}}
```

CRITICAL RULES:
1. NO MARKDOWN - no asterisks, no underscores, plain text only
2. Use name_hebrew for Hebrew name
3. Cultural dish names = transliteration (Banatage, not croquetas)
4. Arabic = Tunisian Derja (adma not beyda for egg, عظمة not بيضة)
5. Spanish: pancakes = panqueques (not tortitas)
6. Use intro_paragraph for description
7. INGREDIENTS: Use measurements.metric for Hebrew/Spanish, measurements.volume for Arabic/English
8. Return ONLY valid JSON

Translate now:"""


def multilingualize_recipe(canonical: dict, max_retries: int = 5) -> dict:
    """Transform a canonical recipe to multilingual format using Gemini."""
    
    recipe_id = canonical.get("id", "unknown")
    recipe_name = canonical.get("name", recipe_id)
    
    # Extract meta info
    meta = canonical.get("meta", {})
    servings = meta.get("servings", "4-6")
    prep_time = f"{meta.get('prep_time_minutes', 15)} min"
    cook_time = f"{meta.get('cook_time_minutes', 30)} min"
    difficulty = meta.get("difficulty", "medium").capitalize()
    
    # Get image path
    image_info = canonical.get("image", {})
    image_path = image_info.get("filename", f"{recipe_id}.png")
    
    vprint(f"  🌍 Translating: {recipe_name}")
    
    prompt = MULTILINGUAL_USER_PROMPT.format(
        canonical_recipe=json.dumps(canonical, ensure_ascii=False, indent=2),
        recipe_id=recipe_id,
        image_path=image_path,
        servings=servings,
        prep_time=prep_time,
        cook_time=cook_time,
        difficulty=difficulty
    )
    
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=MULTILINGUAL_SYSTEM_PROMPT
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.4 + (attempt * 0.1),
                    max_output_tokens=16384,
                )
            )
            
            # Check for valid response
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Empty response, retrying ({attempt + 2}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    raise RuntimeError(f"Gemini returned empty response after {max_retries} attempts for {recipe_id}")
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            result = json.loads(response_text)
            
            # Post-process: strip any markdown that slipped through
            result = strip_markdown_from_result(result)
            
            # Preserve image_prompt from canonical if exists
            if canonical.get("image", {}).get("prompt"):
                result["image_prompt"] = canonical["image"]["prompt"]
            
            vprint(f"    ✅ Translated successfully")
            return result
            
        except ValueError as e:
            if "finish_reason" in str(e) and attempt < max_retries - 1:
                vprint(f"    ⚠️  Safety filter triggered, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            elif attempt == max_retries - 1:
                raise RuntimeError(f"Safety filter blocked after {max_retries} attempts for {recipe_id}")
            raise
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  JSON parse error, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            else:
                vprint(f"    ❌ Failed to parse JSON: {e}")
                vprint(f"    Response preview: {response_text[:500]}...")
                raise RuntimeError(f"JSON parse failed after {max_retries} attempts for {recipe_id}: {e}")
    
    raise RuntimeError(f"Unexpected state in multilingualize_recipe for {recipe_id}")


def process_single_recipe(canonical_file: Path, total: int) -> dict:
    """Process a single recipe (for parallel execution)."""
    global _progress_count
    
    result = {
        "source_file": str(canonical_file),
        "success": False,
        "output_file": None,
        "error": None
    }
    
    try:
        # Load canonical recipe
        with open(canonical_file, 'r', encoding='utf-8') as f:
            canonical = json.load(f)
        
        # Multilingualize
        multilingual = multilingualize_recipe(canonical)
        
        # Generate output filename (use same ID)
        recipe_id = multilingual.get("id", canonical_file.stem)
        output_file = OUTPUT_DIR / f"{recipe_id}.json"
        
        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(multilingual, f, ensure_ascii=False, indent=2)
        
        result["success"] = True
        result["output_file"] = str(output_file)
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] Saved: {output_file.name}")
            
    except Exception as e:
        with _progress_lock:
            _progress_count += 1
            vprint(f"❌ [{_progress_count}/{total}] Failed: {canonical_file.name}: {e}")
        result["error"] = str(e)
    
    return result


def multilingualize_all(workers: int = 30, limit: int = None):
    """Multilingualize all canonical recipes."""
    global _progress_count
    _progress_count = 0
    
    # Get all canonical recipe files (exclude SCHEMA.md)
    canonical_files = sorted([f for f in CANONICAL_DIR.glob("*.json")])
    
    if limit:
        canonical_files = canonical_files[:limit]
    
    total = len(canonical_files)
    
    vprint(f"🌍 Multilingualizing {total} recipes to 4 languages...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {workers}")
    vprint(f"   Output: {OUTPUT_DIR}/")
    vprint()
    vprint("=" * 60)
    
    results = {"success": [], "failed": []}
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_file = {
            executor.submit(process_single_recipe, f, total): f
            for f in canonical_files
        }
        
        for future in as_completed(future_to_file):
            canonical_file = future_to_file[future]
            try:
                result = future.result()
                if result["success"]:
                    results["success"].append(result["output_file"])
                else:
                    results["failed"].append({
                        "source": result["source_file"],
                        "error": result["error"]
                    })
            except Exception as e:
                vprint(f"❌ Exception: {e}")
                results["failed"].append({
                    "source": str(canonical_file),
                    "error": str(e)
                })
    
    # Summary
    vprint()
    vprint("=" * 60)
    vprint("📊 MULTILINGUALIZATION SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {len(results['success'])}")
    vprint(f"❌ Failed: {len(results['failed'])}")
    
    if results["failed"]:
        vprint("\nFailed recipes:")
        for fail in results["failed"]:
            vprint(f"  - {fail['source']}: {fail['error']}")
    
    return results


def multilingualize_single(recipe_id: str):
    """Multilingualize a single recipe by ID."""
    canonical_file = CANONICAL_DIR / f"{recipe_id}.json"
    
    if not canonical_file.exists():
        vprint(f"❌ File not found: {canonical_file}")
        return None
    
    vprint(f"🌍 Multilingualizing single recipe: {recipe_id}")
    vprint(f"   Model: {GEMINI_MODEL}")
    
    try:
        with open(canonical_file, 'r', encoding='utf-8') as f:
            canonical = json.load(f)
        
        multilingual = multilingualize_recipe(canonical)
        
        output_file = OUTPUT_DIR / f"{recipe_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(multilingual, f, ensure_ascii=False, indent=2)
        
        vprint(f"\n✅ Saved: {output_file}")
        vprint(f"\nPreview:")
        print(json.dumps(multilingual, ensure_ascii=False, indent=2)[:3000])
        
        return multilingual
        
    except Exception as e:
        vprint(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Multilingualize canonical recipes")
    parser.add_argument("--single", "-s", help="Process single recipe by ID (e.g., 'mhamsa')")
    parser.add_argument("--limit", "-n", type=int, help="Process only N recipes")
    parser.add_argument("--workers", "-w", type=int, default=30, help="Number of parallel workers")
    parser.add_argument("--list", "-l", action="store_true", help="List available canonical recipes")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available canonical recipes:")
        for i, f in enumerate(sorted(CANONICAL_DIR.glob("*.json"))):
            print(f"  {i:2d}. {f.stem}")
        sys.exit(0)
    
    if args.single:
        multilingualize_single(args.single)
    else:
        multilingualize_all(workers=args.workers, limit=args.limit)

