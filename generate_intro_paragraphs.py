#!/usr/bin/env python3
"""
Generate Intro Paragraphs for Cookbook

Creates a 40-60 word intro paragraph for each recipe that explains:
- What the dish is
- Basic etymology
- Brief history/cultural context

Uses Gemini 3 Pro Preview exclusively (no fallbacks).
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

# Thread-safe progress tracking
_progress_lock = Lock()
_progress_count = 0

def vprint(*args, **kwargs):
    """Print with immediate flush for real-time output."""
    print(*args, **kwargs, flush=True)


# ============================================================================
# INTRO PARAGRAPH SYSTEM PROMPT
# ============================================================================
INTRO_SYSTEM_PROMPT = """You are a culinary writer for a Djerban Jewish family cookbook.

Write a single paragraph (40-60 words) that introduces a recipe. The paragraph should:
1. Explain what the dish IS (type of food, main ingredients, how it's served)
2. Include the etymology/meaning of the name if interesting
3. Mention cultural/historical context briefly

Style guidelines:
- Warm but informative tone
- No flowery language or excessive adjectives
- Factual and concise
- Should read naturally as an intro before a recipe
- Do NOT use phrases like "This dish..." or "This recipe..." - start with the dish name or a description

Example (for Mhamsa):
"Mhamsa—from the Arabic for 'toasted'—is a comforting Tunisian pasta dish made with pearl-shaped semolina grains similar to Israeli couscous. Traditionally hand-rolled and sun-dried, the grains are toasted before cooking to deepen their nutty flavor. In Djerban homes, it's served both dry like pilaf or simmered in a rich tomato broth."

Return ONLY the paragraph text, no quotes, no labels."""


INTRO_USER_PROMPT = """Write a 40-60 word intro paragraph for this dish:

**Name**: {name}
**Hebrew Name**: {name_hebrew}
**Etymology**: {name_origin}
**Description**: {description}
**Cultural Context**: {cultural_context}

Write the intro paragraph (40-60 words):"""


def generate_intro(recipe: dict, max_retries: int = 5) -> str:
    """Generate intro paragraph for a single recipe."""
    
    recipe_id = recipe.get("id", "unknown")
    
    # Truncate long fields to avoid issues
    name_origin = recipe.get("name_origin", "")
    if len(name_origin) > 500:
        name_origin = name_origin[:500] + "..."
    
    prompt = INTRO_USER_PROMPT.format(
        name=recipe.get("name", ""),
        name_hebrew=recipe.get("name_hebrew", ""),
        name_origin=name_origin,
        description=recipe.get("description", ""),
        cultural_context=recipe.get("cultural_context", "")
    )
    
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                INTRO_SYSTEM_PROMPT + "\n\n" + prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.5 + (attempt * 0.1),
                    max_output_tokens=2048,
                )
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Empty response, retrying ({attempt + 2}/{max_retries})...")
                    time.sleep(2)
                    continue
                else:
                    raise RuntimeError(f"Empty response after {max_retries} attempts")
            
            intro_text = response.text.strip()
            
            # Remove quotes if present
            intro_text = intro_text.strip('"\'')
            
            # Verify word count
            word_count = len(intro_text.split())
            if word_count < 25 or word_count > 90:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Word count {word_count}, retrying...")
                    continue  # Try again for better length
            
            return intro_text
            
        except ValueError as e:
            if "finish_reason" in str(e) and attempt < max_retries - 1:
                vprint(f"    ⚠️  Safety filter, retrying ({attempt + 2}/{max_retries})...")
                time.sleep(2)
                continue
            raise
        except Exception as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  Error: {e}, retrying...")
                time.sleep(2)
                continue
            raise
    
    raise RuntimeError(f"Failed to generate intro for {recipe_id}")


def process_single_recipe(recipe_file: Path, total: int) -> dict:
    """Process a single recipe."""
    global _progress_count
    
    result = {
        "recipe_id": recipe_file.stem,
        "success": False,
        "error": None
    }
    
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_name = recipe.get("name", recipe_file.stem)
        
        # Generate intro
        intro_paragraph = generate_intro(recipe)
        
        # Add to recipe
        recipe["intro_paragraph"] = intro_paragraph
        
        # Save
        with open(recipe_file, 'w', encoding='utf-8') as f:
            json.dump(recipe, f, ensure_ascii=False, indent=2)
        
        result["success"] = True
        result["word_count"] = len(intro_paragraph.split())
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] {recipe_name} ({result['word_count']} words)")
            
    except Exception as e:
        with _progress_lock:
            _progress_count += 1
            vprint(f"❌ [{_progress_count}/{total}] Failed {recipe_file.stem}: {e}")
        result["error"] = str(e)
    
    return result


def generate_all(workers: int = 30, limit: int = None, force: bool = False):
    """Generate intro paragraphs for all recipes."""
    global _progress_count
    _progress_count = 0
    
    recipe_files = sorted([f for f in CANONICAL_DIR.glob("*.json")])
    
    # Filter out already processed if not forcing
    if not force:
        to_process = []
        for f in recipe_files:
            with open(f, 'r', encoding='utf-8') as file:
                recipe = json.load(file)
                if "intro_paragraph" not in recipe:
                    to_process.append(f)
        recipe_files = to_process
    
    if limit:
        recipe_files = recipe_files[:limit]
    
    total = len(recipe_files)
    
    if total == 0:
        vprint("All recipes already have intro paragraphs. Use --force to regenerate.")
        return
    
    vprint(f"📝 Generating intro paragraphs for {total} recipes...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {workers}")
    vprint()
    vprint("=" * 60)
    
    results = {"success": [], "failed": []}
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_file = {
            executor.submit(process_single_recipe, f, total): f
            for f in recipe_files
        }
        
        for future in as_completed(future_to_file):
            recipe_file = future_to_file[future]
            try:
                result = future.result()
                if result["success"]:
                    results["success"].append(result["recipe_id"])
                else:
                    results["failed"].append({
                        "recipe_id": result["recipe_id"],
                        "error": result["error"]
                    })
            except Exception as e:
                results["failed"].append({
                    "recipe_id": recipe_file.stem,
                    "error": str(e)
                })
    
    vprint()
    vprint("=" * 60)
    vprint("📊 SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {len(results['success'])}")
    vprint(f"❌ Failed: {len(results['failed'])}")
    
    if results["failed"]:
        vprint("\nFailed:")
        for fail in results["failed"]:
            vprint(f"  - {fail['recipe_id']}: {fail['error']}")


def generate_single(recipe_id: str):
    """Generate intro for a single recipe."""
    recipe_file = CANONICAL_DIR / f"{recipe_id}.json"
    
    if not recipe_file.exists():
        vprint(f"❌ File not found: {recipe_file}")
        return
    
    vprint(f"📝 Generating intro for: {recipe_id}")
    
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    intro = generate_intro(recipe)
    recipe["intro_paragraph"] = intro
    
    with open(recipe_file, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, ensure_ascii=False, indent=2)
    
    vprint(f"\n✅ Generated ({len(intro.split())} words):")
    vprint(f"\n{intro}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate intro paragraphs for recipes")
    parser.add_argument("--single", "-s", help="Generate for single recipe by ID")
    parser.add_argument("--limit", "-n", type=int, help="Process only N recipes")
    parser.add_argument("--workers", "-w", type=int, default=30, help="Number of parallel workers (default: 30)")
    parser.add_argument("--force", "-f", action="store_true", help="Regenerate even if exists")
    parser.add_argument("--list", "-l", action="store_true", help="List recipes without intro")
    
    args = parser.parse_args()
    
    if args.list:
        print("Recipes without intro_paragraph:")
        for f in sorted(CANONICAL_DIR.glob("*.json")):
            with open(f, 'r', encoding='utf-8') as file:
                recipe = json.load(file)
                if "intro_paragraph" not in recipe:
                    print(f"  - {f.stem}")
        sys.exit(0)
    
    if args.single:
        generate_single(args.single)
    else:
        generate_all(workers=args.workers, limit=args.limit, force=args.force)

