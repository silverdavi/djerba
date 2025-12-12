#!/usr/bin/env python3
"""
Enrich Canonical Recipe Ingredients with Multiple Unit Systems

For each ingredient in canonical recipes, adds:
- metric: { value, unit } - grams (g) or milliliters (ml)
- imperial: { value, unit } - ounces (oz) or fluid ounces (fl oz)  
- volume: { value, unit } - cups, tablespoons, teaspoons
- original: { value, unit } - the original amount as specified

Uses Gemini 3 Pro Preview for intelligent unit conversion.
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

# Thread-safe helpers
_progress_lock = Lock()
_progress_count = 0

def vprint(*args, **kwargs):
    """Print with immediate flush for real-time output."""
    print(*args, **kwargs, flush=True)


# ============================================================================
# UNIT CONVERSION SYSTEM PROMPT
# ============================================================================
UNIT_CONVERSION_PROMPT = """You are an expert at cooking measurement conversions.

Given a list of recipe ingredients with their current amounts and units, convert each to 4 measurement systems:

## Measurement Systems

1. **metric**: Use grams (g) for solids, milliliters (ml) for liquids
2. **imperial**: Use ounces (oz) for solids, fluid ounces (fl oz) for liquids
3. **volume**: Use cups, tablespoons (tbsp), teaspoons (tsp) - whatever is most practical
4. **original**: Keep the original amount/unit as given

## Conversion Reference

Weight:
- 1 oz = 28.35 g
- 1 lb = 453.6 g
- 1 cup flour ≈ 120-130g
- 1 cup sugar ≈ 200g
- 1 cup rice ≈ 185g

Volume:
- 1 cup = 240 ml = 8 fl oz
- 1 tbsp = 15 ml = 0.5 fl oz
- 1 tsp = 5 ml

## Special Cases

- **Count items** (e.g., "2 onions"): Set metric/imperial/volume all to null, keep only original
- **"To taste"**: Set all measurement values to null, unit to "to_taste"
- **Small amounts** (< 1 tbsp): Use tsp for volume
- **Large amounts** (> 2 cups): Still use cups for volume

## Output Format

Return a JSON array where each item has:
```json
{
  "ingredient_id": "same as input",
  "measurements": {
    "metric": { "value": 250, "unit": "g" },
    "imperial": { "value": 8.8, "unit": "oz" },
    "volume": { "value": 2, "unit": "cups" },
    "original": { "value": 250, "unit": "g" }
  }
}
```

For count items:
```json
{
  "ingredient_id": "onion",
  "measurements": {
    "metric": null,
    "imperial": null,
    "volume": null,
    "original": { "value": 2, "unit": "unit" }
  }
}
```

For "to taste":
```json
{
  "ingredient_id": "salt",
  "measurements": {
    "metric": { "value": null, "unit": "to_taste" },
    "imperial": { "value": null, "unit": "to_taste" },
    "volume": { "value": null, "unit": "to_taste" },
    "original": { "value": null, "unit": "to_taste" }
  }
}
```

Return ONLY valid JSON array."""


def convert_ingredients(ingredients: list, recipe_name: str, max_retries: int = 5) -> list:
    """Convert ingredient units using Gemini."""
    
    vprint(f"  📐 Converting units for: {recipe_name}")
    
    # Build ingredient summary for LLM
    ingredient_summary = []
    for ing in ingredients:
        ing_info = {
            "ingredient_id": ing.get("ingredient_id"),
            "name": ing.get("name"),
            "amount": ing.get("amount"),
            "unit": ing.get("unit"),
            "notes": ing.get("notes")
        }
        ingredient_summary.append(ing_info)
    
    prompt = f"""Convert these ingredients to all 4 measurement systems:

Recipe: {recipe_name}

Ingredients:
```json
{json.dumps(ingredient_summary, indent=2, ensure_ascii=False)}
```

Return JSON array with measurements for each ingredient."""

    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=UNIT_CONVERSION_PROMPT
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=8192,
                )
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Empty response, retrying ({attempt + 2}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    raise RuntimeError(f"Empty response after {max_retries} attempts")
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            conversions = json.loads(response_text)
            
            vprint(f"    ✅ Converted {len(conversions)} ingredients")
            return conversions
            
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  JSON error, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            else:
                vprint(f"    ❌ JSON parse failed: {e}")
                raise
    
    raise RuntimeError("Unexpected state in convert_ingredients")


def enrich_recipe(recipe_path: Path, total: int) -> bool:
    """Enrich a single recipe with unit conversions."""
    global _progress_count
    
    try:
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get("id", recipe_path.stem)
        recipe_name = recipe.get("name", recipe_id)
        ingredients = recipe.get("ingredients", [])
        
        if not ingredients:
            vprint(f"  ⏭️  Skipping {recipe_id}: no ingredients")
            return True
        
        # Check if already enriched
        if ingredients and isinstance(ingredients[0].get("measurements"), dict):
            vprint(f"  ⏭️  Skipping {recipe_id}: already enriched")
            return True
        
        # Convert units
        conversions = convert_ingredients(ingredients, recipe_name)
        
        # Merge conversions back into ingredients
        conv_map = {c["ingredient_id"]: c["measurements"] for c in conversions}
        
        for ing in ingredients:
            ing_id = ing.get("ingredient_id")
            if ing_id in conv_map:
                ing["measurements"] = conv_map[ing_id]
            else:
                # Fallback: create measurements from original
                ing["measurements"] = {
                    "metric": {"value": ing.get("amount"), "unit": ing.get("unit")},
                    "imperial": None,
                    "volume": None,
                    "original": {"value": ing.get("amount"), "unit": ing.get("unit")}
                }
        
        # Save updated recipe
        with open(recipe_path, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] Enriched: {recipe_id}")
        
        return True
        
    except Exception as e:
        vprint(f"❌ Error processing {recipe_path.name}: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Enrich canonical recipes with multi-unit measurements")
    parser.add_argument("--single", type=str, help="Process single recipe by ID")
    parser.add_argument("--workers", type=int, default=30, help="Number of parallel workers")
    parser.add_argument("--force", action="store_true", help="Re-process already enriched recipes")
    args = parser.parse_args()
    
    # Get recipe files
    recipe_files = sorted(CANONICAL_DIR.glob("*.json"))
    
    if args.single:
        recipe_files = [f for f in recipe_files if args.single in f.stem]
        if not recipe_files:
            vprint(f"❌ Recipe not found: {args.single}")
            sys.exit(1)
    
    total = len(recipe_files)
    vprint(f"📐 Enriching {total} recipes with multi-unit measurements...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {args.workers}")
    vprint()
    vprint("=" * 60)
    
    # Process recipes
    failed = []
    
    if args.workers == 1 or args.single:
        for recipe_file in recipe_files:
            if not enrich_recipe(recipe_file, total):
                failed.append(recipe_file.stem)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(enrich_recipe, f, total): f 
                for f in recipe_files
            }
            for future in as_completed(futures):
                recipe_file = futures[future]
                try:
                    if not future.result():
                        failed.append(recipe_file.stem)
                except Exception as e:
                    vprint(f"❌ Exception for {recipe_file.name}: {e}")
                    failed.append(recipe_file.stem)
    
    # Summary
    vprint()
    vprint("=" * 60)
    vprint("📊 ENRICHMENT SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {total - len(failed)}")
    vprint(f"❌ Failed: {len(failed)}")
    
    if failed:
        vprint("\nFailed recipes:")
        for name in failed:
            vprint(f"  - {name}")


if __name__ == "__main__":
    main()

