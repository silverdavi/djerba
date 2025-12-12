#!/usr/bin/env python3
"""
Veganize Canonical Recipes

Takes canonical recipes and:
1. Replaces non-vegan ingredients with plant-based alternatives
2. Updates descriptions to note substitutions ("traditionally with X, here with Y")
3. Generates detailed image prompts following cookbook image rules
4. Rewrites intro paragraphs (40-50 words, no em dashes, connected to title)

Uses Gemini 3 Pro Preview exclusively.

Vegan Substitution Rules:
- Eggs in baking → applesauce, flax egg, or aquafaba
- Eggs as main → tofu scramble or chickpea flour omelet
- Fish → tofu + nori seaweed, chickpea "tuna", hearts of palm
- Meat (beef/lamb) → seitan, TVP, or mushrooms
- Chicken → firm tofu, soy curls, or seitan
- Dairy milk → oat/almond/soy milk
- Butter → vegan margarine or coconut oil
- Cream → coconut cream or cashew cream
- Cheese → nutritional yeast or vegan cheese
- Honey → maple syrup or date syrup (silan)
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
    print(*args, **kwargs, flush=True)


# ============================================================================
# VEGAN SUBSTITUTION RULES
# ============================================================================
VEGAN_SUBSTITUTIONS = {
    # Eggs
    "egg": {
        "baking": "flax egg (1 tbsp ground flax + 3 tbsp water) or applesauce",
        "binding": "aquafaba (chickpea water) or mashed banana",
        "main_dish": "firm tofu (crumbled or sliced)",
        "omelet": "chickpea flour batter (besan)",
    },
    # Fish
    "fish": "firm tofu marinated with nori seaweed for ocean flavor",
    "tuna": "mashed chickpeas with nori and capers (chickpea 'tuna')",
    "salmon": "marinated carrots or beet-cured tofu",
    "sardines": "marinated jackfruit with nori",
    # Meat
    "beef": "seitan or TVP (textured vegetable protein)",
    "lamb": "seitan seasoned with cumin and coriander",
    "ground_meat": "TVP crumbles, lentils, or mushroom-walnut mix",
    "meat": "seitan or firm tofu",
    # Poultry
    "chicken": "firm tofu, soy curls, or seitan",
    "chicken_breast": "sliced firm tofu or seitan cutlets",
    "ground_chicken": "crumbled firm tofu or TVP",
    # Dairy
    "milk": "oat milk, almond milk, or soy milk",
    "cream": "coconut cream or cashew cream",
    "butter": "vegan margarine or coconut oil",
    "cheese": "nutritional yeast or vegan cheese",
    "yogurt": "coconut or soy yogurt",
    # Other
    "honey": "maple syrup, date syrup (silan), or agave",
}


# ============================================================================
# VEGANIZATION SYSTEM PROMPT
# ============================================================================
VEGANIZE_SYSTEM_PROMPT = """You are an expert vegan chef specializing in adapting traditional recipes.
You transform recipes to be 100% plant-based while maintaining authentic flavors and textures.

## VEGAN SUBSTITUTION RULES

### Eggs
- In baking (cakes, cookies): Use flax egg, applesauce, or mashed banana
- For binding: Use aquafaba (chickpea water)
- As main dish (omelets, scrambles): Use firm tofu or chickpea flour batter
- Whole eggs in stews: Use small whole potatoes or tofu cubes

### Fish & Seafood
- White fish: Firm tofu marinated with nori seaweed
- Tuna: Mashed chickpeas with nori and capers
- Salmon: Marinated carrots or beet-cured tofu
- Fish patties: Chickpea-based patties with kelp powder

### Meat
- Beef/lamb chunks: Seitan pieces
- Ground meat: TVP crumbles, lentils, or mushroom-walnut mix
- Chicken: Firm tofu, soy curls, or seitan
- Slow-cooked meat: Jackfruit or seitan

### Dairy
- Milk: Oat, almond, or soy milk
- Cream: Coconut cream or cashew cream
- Butter: Vegan margarine or coconut oil
- Cheese: Nutritional yeast or vegan cheese

### Other
- Honey: Maple syrup, date syrup (silan), or agave
- Bone broth: Vegetable broth with miso

## OUTPUT FORMAT
Return valid JSON with the veganized recipe data."""


VEGANIZE_USER_PROMPT = """Veganize this recipe and enhance it for cookbook production.

## ORIGINAL RECIPE:
```json
{recipe_json}
```

## TASKS:

### 1. VEGANIZE INGREDIENTS
- Identify any non-vegan ingredients (meat, fish, eggs, dairy, honey)
- Replace with appropriate vegan alternatives
- Update the ingredient list with substitutions
- Keep quantities proportional

### 2. UPDATE DESCRIPTION
If the recipe was adapted, update the description to note this naturally:
- Bad: "This recipe uses tofu instead of fish"
- Good: "Traditionally made with white fish, this vegan version uses firm tofu marinated with nori for authentic ocean flavor"

### 3. REWRITE INTRO PARAGRAPH
Create a new intro_paragraph that:
- Is EXACTLY 40-50 words (count carefully!)
- Connects the dish NAME to its etymology/origin
- NO em dashes (use commas or periods instead)
- Mentions if it's a vegan adaptation of a traditional dish
- Is engaging and informative

### 4. GENERATE IMAGE PROMPT
Create a detailed image_generation_prompt following these rules:
- Describe the finished dish appearance in detail
- Specify colors, textures, and presentation
- Note that all proteins are PLANT-BASED (seitan, tofu, etc.)
- Include serving vessel (bowl, plate, etc.)
- Mention the Safed house setting (early 1900s stone kitchen)
- 150-200 words, very detailed

## OUTPUT FORMAT:
```json
{{
  "is_vegan": true,
  "was_veganized": true/false,
  "vegan_substitutions": [
    {{"original": "fish", "replacement": "tofu with nori", "notes": "for ocean flavor"}}
  ],
  "ingredients": [/* updated ingredient list */],
  "intro_paragraph": "40-50 word paragraph...",
  "image_generation_prompt": "Detailed 150-200 word prompt..."
}}
```

Return ONLY valid JSON."""


def veganize_recipe(canonical: dict, max_retries: int = 5) -> dict:
    """Veganize a canonical recipe using Gemini."""
    
    recipe_id = canonical.get("id", "unknown")
    recipe_name = canonical.get("name", recipe_id)
    
    vprint(f"  🌱 Veganizing: {recipe_name}")
    
    prompt = VEGANIZE_USER_PROMPT.format(
        recipe_json=json.dumps(canonical, ensure_ascii=False, indent=2)
    )
    
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=VEGANIZE_SYSTEM_PROMPT
    )
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.3 + (attempt * 0.1),
                    max_output_tokens=16384,
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
            
            # Remove markdown code blocks
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            result = json.loads(response_text)
            
            # Post-process: remove em dashes from intro_paragraph
            if "intro_paragraph" in result:
                result["intro_paragraph"] = result["intro_paragraph"].replace("—", ", ").replace("–", ", ")
            
            vprint(f"    ✅ Veganized successfully")
            return result
            
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  JSON error, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            else:
                vprint(f"    ❌ JSON parse failed: {e}")
                raise
    
    raise RuntimeError("Unexpected state in veganize_recipe")


def process_recipe(recipe_path: Path, total: int) -> bool:
    """Process a single recipe."""
    global _progress_count
    
    try:
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get("id", recipe_path.stem)
        
        # Check if already veganized
        if recipe.get("veganization_complete"):
            vprint(f"  ⏭️  Skipping {recipe_id}: already veganized")
            with _progress_lock:
                _progress_count += 1
            return True
        
        # Veganize
        updates = veganize_recipe(recipe)
        
        # Merge updates into recipe
        recipe["is_vegan"] = updates.get("is_vegan", True)
        recipe["was_veganized"] = updates.get("was_veganized", False)
        recipe["vegan_substitutions"] = updates.get("vegan_substitutions", [])
        
        # Update ingredients if provided
        if "ingredients" in updates and updates["ingredients"]:
            recipe["ingredients"] = updates["ingredients"]
        
        # Update intro paragraph
        if "intro_paragraph" in updates:
            recipe["intro_paragraph"] = updates["intro_paragraph"]
        
        # Add image generation prompt
        if "image_generation_prompt" in updates:
            if "image" not in recipe:
                recipe["image"] = {}
            recipe["image"]["generation_prompt"] = updates["image_generation_prompt"]
        
        # Mark as complete
        recipe["veganization_complete"] = True
        
        # Save
        with open(recipe_path, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] Saved: {recipe_id}")
        
        return True
        
    except Exception as e:
        vprint(f"❌ Error processing {recipe_path.name}: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Veganize canonical recipes")
    parser.add_argument("--single", type=str, help="Process single recipe by ID")
    parser.add_argument("--workers", type=int, default=50, help="Number of parallel workers")
    parser.add_argument("--force", action="store_true", help="Re-process already veganized recipes")
    args = parser.parse_args()
    
    # Get recipe files
    recipe_files = sorted(CANONICAL_DIR.glob("*.json"))
    recipe_files = [f for f in recipe_files if f.name != "SCHEMA.md"]
    
    if args.single:
        recipe_files = [f for f in recipe_files if args.single in f.stem]
        if not recipe_files:
            vprint(f"❌ Recipe not found: {args.single}")
            sys.exit(1)
    
    if args.force:
        # Clear veganization flags
        for f in recipe_files:
            try:
                with open(f, 'r', encoding='utf-8') as fp:
                    recipe = json.load(fp)
                if "veganization_complete" in recipe:
                    del recipe["veganization_complete"]
                    with open(f, 'w', encoding='utf-8') as fp:
                        json.dump(recipe, fp, ensure_ascii=False, indent=2)
            except:
                pass
    
    total = len(recipe_files)
    vprint(f"🌱 Veganizing {total} recipes...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {args.workers}")
    vprint()
    vprint("=" * 60)
    
    failed = []
    
    if args.workers == 1 or args.single:
        for recipe_file in recipe_files:
            if not process_recipe(recipe_file, total):
                failed.append(recipe_file.stem)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(process_recipe, f, total): f 
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
    vprint("📊 VEGANIZATION SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {total - len(failed)}")
    vprint(f"❌ Failed: {len(failed)}")
    
    if failed:
        vprint("\nFailed recipes:")
        for name in failed:
            vprint(f"  - {name}")


if __name__ == "__main__":
    main()

