#!/usr/bin/env python3
"""
Canonize Recipes to Structured English Format

Takes Hebrew recipes from safed_recipes/ and safed_recipes_recime/
and converts them to canonical English JSON with structured ingredients.

Uses Gemini 3 Pro Preview exclusively (no fallbacks).

Input: Hebrew/English recipe JSON from source folders
Output: Canonical English JSON with structured ingredients
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
# Note: safed_recipes_recime is a duplicate subset of safed_recipes, so we only use safed_recipes
SOURCE_DIRS = [
    Path("data/safed_recipes"),
]
OUTPUT_DIR = Path("data/recipes_canonical")
DICTIONARY_FILE = Path("data/ingredients_dictionary.json")

# Create output directory
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Thread-safe helpers
_progress_lock = Lock()
_progress_count = 0
_dictionary_lock = Lock()
_ingredients_seen = set()

def vprint(*args, **kwargs):
    """Print with immediate flush for real-time output."""
    print(*args, **kwargs, flush=True)


# ============================================================================
# CANONIZATION SYSTEM PROMPT
# ============================================================================
CANONIZE_SYSTEM_PROMPT = """You are an expert culinary translator and recipe standardizer.

## YOUR TASK
Convert Hebrew/English recipes into canonical English JSON with STRUCTURED ingredients.

## CONTEXT
This is for a Djerban Jewish family cookbook. The recipes come from:
- The Silver/Cohen family from Djerba, Tunisia
- The Kadoch/Maloul families from Tangier, Morocco

Many dishes are traditional North African Jewish recipes that need to be:
1. Translated to clear English
2. Structured with proper ingredient fields
3. Quantities standardized to metric where sensible

## INGREDIENT STRUCTURE
Each ingredient MUST be a structured object:
```json
{
  "ingredient_id": "olive_oil",     // lowercase_snake_case canonical ID
  "name": "Olive oil",              // English name
  "amount": 30,                     // Numeric (null if "to taste")
  "unit": "ml",                     // Canonical unit or null
  "preparation": "chopped",         // Optional: diced, minced, etc.
  "notes": "for frying",            // Optional notes
  "is_optional": false
}
```

## UNIT RULES
- Use METRIC for weights: g, kg
- Use METRIC for large volumes: ml, L
- Keep tsp, tbsp for small measurements
- Use "unit" for countable items: "1 unit onion"
- Use null for "to taste", "as needed"

## QUANTITY INFERENCE
If the source has vague quantities, use reasonable cookbook defaults:
- "בצל" (onion) → 1 unit medium onion
- "שמן" (oil) → 30 ml (2 tbsp)
- "מלח" (salt) → to taste (null)
- "פלפל" (pepper) → to taste (null)

## HEBREW COOKING TERMS
- פפריקה = paprika (sweet unless specified חריף/hot)
- פ. שחור = black pepper
- תפו"א = potato (תפוח אדמה abbreviated)
- מחמסה = mhamsa (Israeli couscous/ptitim)
- גריסים = pearl barley / groats
- סולת = semolina

## OUTPUT FORMAT
Return ONLY valid JSON, no markdown blocks."""


CANONIZE_USER_PROMPT = """Convert this recipe to canonical English JSON.

## INPUT RECIPE:
```json
{input_recipe}
```

## REQUIRED OUTPUT STRUCTURE:
```json
{{
  "id": "recipe_id",
  "slug": "recipe-id",
  "source_file": "{source_file}",
  
  "name": "English Name",
  "name_hebrew": "שם בעברית",
  "name_origin": "Etymology of the name if known, or null",
  
  "description": "2-3 sentence description of the dish in English.",
  "cultural_context": "Notes about Djerban/Tunisian/Moroccan Jewish tradition, or null",
  "is_vegan": false,
  "vegan_adaptation_notes": null,
  
  "meta": {{
    "servings": "4-6",
    "prep_time_minutes": 15,
    "cook_time_minutes": 30,
    "total_time_minutes": 45,
    "difficulty": "easy"
  }},
  
  "ingredients": [
    {{
      "ingredient_id": "onion",
      "name": "Onion",
      "amount": 1,
      "unit": "unit",
      "size": "medium",
      "preparation": "diced",
      "notes": null,
      "is_optional": false
    }}
  ],
  
  "steps": [
    {{
      "step": 1,
      "instruction": "Clear instruction in English.",
      "time_minutes": null,
      "tips": null
    }}
  ],
  
  "variants": null,
  
  "image": {{
    "filename": "recipe_id.png",
    "prompt": null
  }},
  
  "tags": ["north-african", "tunisian"],
  "related_recipes": []
}}
```

CRITICAL:
1. Extract ALL ingredients as structured objects
2. Infer reasonable quantities if not specified
3. Translate all Hebrew to English
4. Keep the original Hebrew name in name_hebrew
5. Return ONLY valid JSON, no markdown

Return the canonical JSON:"""


def load_all_recipes():
    """Load all recipes from both source directories."""
    recipes = []
    
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            vprint(f"⚠️  Source directory not found: {source_dir}")
            continue
            
        for recipe_file in sorted(source_dir.glob("*.json")):
            try:
                with open(recipe_file, 'r', encoding='utf-8') as f:
                    recipe = json.load(f)
                    recipe['_source_file'] = str(recipe_file)
                    recipe['_source_dir'] = source_dir.name
                    recipes.append(recipe)
            except Exception as e:
                vprint(f"❌ Failed to load {recipe_file}: {e}")
    
    return recipes


def canonize_recipe(input_recipe: dict, max_retries: int = 3) -> dict:
    """Transform a single recipe to canonical English format using Gemini."""
    
    recipe_name = input_recipe.get("name_hebrew", input_recipe.get("id", "unknown"))
    source_file = input_recipe.get("_source_file", "unknown")
    
    vprint(f"  📝 Canonizing: {recipe_name}")
    
    # Remove internal fields before sending to API
    recipe_for_api = {k: v for k, v in input_recipe.items() if not k.startswith('_')}
    
    prompt = CANONIZE_USER_PROMPT.format(
        input_recipe=json.dumps(recipe_for_api, ensure_ascii=False, indent=2),
        source_file=source_file
    )
    
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=CANONIZE_SYSTEM_PROMPT
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3 + (attempt * 0.1),  # Low temp for consistency
                    max_output_tokens=8192,
                )
            )
            
            # Check for valid response
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Empty response, retrying ({attempt + 2}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    raise RuntimeError(f"Gemini returned empty response after {max_retries} attempts for {recipe_name}")
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            result = json.loads(response_text)
            
            # Track ingredients for dictionary
            with _dictionary_lock:
                for ing in result.get("ingredients", []):
                    ing_id = ing.get("ingredient_id")
                    if ing_id:
                        _ingredients_seen.add((ing_id, ing.get("name", ing_id)))
            
            vprint(f"    ✅ Canonized successfully: {result.get('id', 'unknown')}")
            return result
            
        except ValueError as e:
            if "finish_reason" in str(e) and attempt < max_retries - 1:
                vprint(f"    ⚠️  Safety filter triggered, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            elif attempt == max_retries - 1:
                raise RuntimeError(f"Safety filter blocked after {max_retries} attempts for {recipe_name}")
            raise
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  JSON parse error, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            else:
                vprint(f"    ❌ Failed to parse JSON: {e}")
                vprint(f"    Response preview: {response_text[:500]}...")
                raise RuntimeError(f"JSON parse failed after {max_retries} attempts for {recipe_name}: {e}")
    
    raise RuntimeError(f"Unexpected state in canonize_recipe for {recipe_name}")


def process_single_recipe(recipe: dict, total: int) -> dict:
    """Process a single recipe (for parallel execution)."""
    global _progress_count
    
    result = {
        "source_file": recipe.get("_source_file", "unknown"),
        "success": False,
        "output_file": None,
        "error": None
    }
    
    try:
        # Canonize
        canonical = canonize_recipe(recipe)
        
        # Generate output filename
        recipe_id = canonical.get("id", Path(recipe.get("_source_file", "unknown")).stem)
        # Ensure valid filename
        recipe_id = re.sub(r'[^\w\-]', '_', recipe_id.lower())
        
        output_file = OUTPUT_DIR / f"{recipe_id}.json"
        
        # Handle duplicates
        counter = 1
        while output_file.exists():
            output_file = OUTPUT_DIR / f"{recipe_id}_{counter}.json"
            counter += 1
        
        # Save
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(canonical, f, ensure_ascii=False, indent=2)
        
        result["success"] = True
        result["output_file"] = str(output_file)
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] Saved: {output_file.name}")
            
    except Exception as e:
        with _progress_lock:
            _progress_count += 1
            vprint(f"❌ [{_progress_count}/{total}] Failed: {recipe.get('_source_file', 'unknown')}: {e}")
        result["error"] = str(e)
    
    return result


def update_ingredients_dictionary():
    """Update the ingredients dictionary with newly seen ingredients."""
    try:
        with open(DICTIONARY_FILE, 'r', encoding='utf-8') as f:
            dictionary = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        dictionary = {"_meta": {"description": "Ingredient dictionary"}, "ingredients": {}}
    
    # Add new ingredients
    for ing_id, ing_name in _ingredients_seen:
        if ing_id not in dictionary["ingredients"]:
            dictionary["ingredients"][ing_id] = {
                "en": ing_name,
                "he": None,
                "es": None,
                "ar": None
            }
    
    # Sort ingredients
    dictionary["ingredients"] = dict(sorted(dictionary["ingredients"].items()))
    
    with open(DICTIONARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)
    
    vprint(f"📚 Updated ingredient dictionary with {len(_ingredients_seen)} ingredients")


def canonize_all(workers: int = 30, limit: int = None):
    """Canonize all recipes from both source directories."""
    global _progress_count
    _progress_count = 0
    
    # Load all recipes
    recipes = load_all_recipes()
    
    if limit:
        recipes = recipes[:limit]
    
    total = len(recipes)
    
    vprint(f"🍳 Canonizing {total} recipes to structured English...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {workers}")
    vprint(f"   Output: {OUTPUT_DIR}/")
    vprint()
    vprint("=" * 60)
    
    results = {"success": [], "failed": []}
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_recipe = {
            executor.submit(process_single_recipe, recipe, total): recipe
            for recipe in recipes
        }
        
        for future in as_completed(future_to_recipe):
            recipe = future_to_recipe[future]
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
                    "source": recipe.get("_source_file", "unknown"),
                    "error": str(e)
                })
    
    # Update dictionary
    update_ingredients_dictionary()
    
    # Summary
    vprint()
    vprint("=" * 60)
    vprint("📊 CANONIZATION SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {len(results['success'])}")
    vprint(f"❌ Failed: {len(results['failed'])}")
    
    if results["failed"]:
        vprint("\nFailed recipes:")
        for fail in results["failed"]:
            vprint(f"  - {fail['source']}: {fail['error']}")
    
    return results


def canonize_single(filename: str):
    """Canonize a single recipe by filename."""
    # Find the file
    recipe_file = None
    for source_dir in SOURCE_DIRS:
        candidate = source_dir / filename
        if candidate.exists():
            recipe_file = candidate
            break
    
    if not recipe_file:
        vprint(f"❌ File not found: {filename}")
        return None
    
    vprint(f"🍳 Canonizing single recipe: {filename}")
    vprint(f"   Model: {GEMINI_MODEL}")
    
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
            recipe['_source_file'] = str(recipe_file)
            recipe['_source_dir'] = recipe_file.parent.name
        
        canonical = canonize_recipe(recipe)
        
        recipe_id = canonical.get("id", recipe_file.stem)
        recipe_id = re.sub(r'[^\w\-]', '_', recipe_id.lower())
        output_file = OUTPUT_DIR / f"{recipe_id}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(canonical, f, ensure_ascii=False, indent=2)
        
        # Update dictionary after single recipe
        update_ingredients_dictionary()
        
        vprint(f"\n✅ Saved: {output_file}")
        vprint(f"\nPreview:")
        print(json.dumps(canonical, ensure_ascii=False, indent=2)[:2000])
        
        return canonical
        
    except Exception as e:
        vprint(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Canonize recipes to structured English format")
    parser.add_argument("--single", "-s", help="Process single recipe file")
    parser.add_argument("--limit", "-n", type=int, help="Process only N recipes")
    parser.add_argument("--workers", "-w", type=int, default=30, help="Number of parallel workers")
    parser.add_argument("--list", "-l", action="store_true", help="List available recipes")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available recipes:")
        for source_dir in SOURCE_DIRS:
            print(f"\n{source_dir}:")
            for i, f in enumerate(sorted(source_dir.glob("*.json"))):
                print(f"  {i:2d}. {f.name}")
        sys.exit(0)
    
    if args.single:
        canonize_single(args.single)
    else:
        canonize_all(workers=args.workers, limit=args.limit)

