#!/usr/bin/env python3
"""
Translation Quality Review - All 87 recipes × 4 languages
Uses Gemini 3.1 Pro with 35 parallel workers.
"""

import json
import os
import time
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types

RECIPES_DIR = Path("data/recipes_multilingual_v2")
MODEL = "gemini-3.1-pro-preview"
MAX_WORKERS = 10
CHANGES_LOG = []

# Load API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    from dotenv import load_dotenv
    load_dotenv(Path(".env"))
    api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # Read directly
    env_text = Path(".env").read_text()
    for line in env_text.strip().split("\n"):
        if line.startswith("GEMINI_API_KEY="):
            api_key = line.split("=", 1)[1].strip()

REVIEW_PROMPT = """You are a professional multilingual cookbook editor fluent in Hebrew, Arabic (Tunisian/Maghrebi dialect), Spanish, and English.

Review this recipe's text in ALL FOUR LANGUAGES. Fix any issues:

1. **Hebrew**: Must read naturally to an Israeli Hebrew speaker. Fix awkward transliterations (e.g., "TVP (חלבון סויה מרקם)" should be "חלבון סויה מרקם (TVP)"). Fix unnatural phrasing. Keep cooking terms authentic.

2. **Arabic (Tunisian/Maghrebi)**: Must read naturally in Djerban/Tunisian dialect. Not Modern Standard Arabic. Fix any MSA that crept in. Use authentic Maghrebi cooking vocabulary.

3. **Spanish**: Must be natural Latin American/general Spanish. Fix any awkward constructions. Cooking terms should be widely understood.

4. **English**: Must be clear, natural cookbook English. Fix any awkward phrasing.

RULES:
- Keep the SAME meaning and approximate length
- Do NOT add new content or remove existing content
- Fix phrasing, word order, transliterations, and grammar only
- Ingredient lists: fix transliteration issues, ensure quantities are clear
- Steps: ensure they are clear and actionable
- Description: ensure it reads like professional cookbook text
- If a language version is already perfect, return it unchanged

IMPORTANT: Return the COMPLETE corrected recipe as a valid JSON object. Do NOT use trailing commas. Do NOT add comments. Return ONLY valid JSON with this structure:

{"changes": [{"field": "...", "reason": "..."}], "name": {"he": "...", "es": "...", "ar": "...", "en": "..."}, "description": {"he": "...", "es": "...", "ar": "...", "en": "..."}, "ingredients": {"he": ["..."], "es": ["..."], "ar": ["..."], "en": ["..."]}, "steps": {"he": ["..."], "es": ["..."], "ar": ["..."], "en": ["..."]}}

Here is the recipe to review:
"""


def review_recipe(recipe_path: Path) -> tuple:
    """Review a single recipe with Gemini 3.1 Pro."""
    recipe_id = recipe_path.stem
    
    try:
        with open(recipe_path, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        name_en = recipe.get("name", {}).get("en", recipe_id)
        
        # Build review payload (only text fields)
        review_data = {
            "id": recipe["id"],
            "name": recipe["name"],
            "description": recipe["description"],
            "ingredients": recipe["ingredients"],
            "steps": recipe["steps"],
        }
        
        prompt = REVIEW_PROMPT + json.dumps(review_data, ensure_ascii=False, indent=2)
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=MODEL,
            contents=[prompt],
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=16384,
            )
        )
        
        response_text = response.text.strip()
        
        # Clean response - remove markdown fences if present
        if response_text.startswith("```"):
            lines = response_text.split("\n")
            # Remove first and last lines (fences)
            lines = [l for l in lines if not l.strip().startswith("```")]
            response_text = "\n".join(lines)
        
        # Parse JSON response with robust handling
        import re as _re
        
        def try_parse_json(text):
            """Try multiple strategies to parse JSON from model output."""
            # Strategy 1: direct parse
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                pass
            
            # Strategy 2: extract JSON block
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                block = text[start:end]
                try:
                    return json.loads(block)
                except json.JSONDecodeError:
                    pass
                
                # Strategy 3: fix trailing commas
                fixed = _re.sub(r',\s*}', '}', block)
                fixed = _re.sub(r',\s*]', ']', fixed)
                try:
                    return json.loads(fixed)
                except json.JSONDecodeError:
                    pass
                
                # Strategy 4: fix unescaped quotes in strings
                # Replace \" that might be double-escaped
                fixed2 = fixed.replace('\\\\"', '\\"')
                try:
                    return json.loads(fixed2)
                except json.JSONDecodeError:
                    pass
            
            return None
        
        reviewed = try_parse_json(response_text)
        if reviewed is None:
            return (recipe_id, name_en, False, f"Failed to parse JSON response", [])
        
        changes = reviewed.get("changes", [])
        
        if changes:
            # Apply changes to the original recipe
            if "name" in reviewed:
                recipe["name"] = reviewed["name"]
            if "description" in reviewed:
                recipe["description"] = reviewed["description"]
            if "ingredients" in reviewed:
                recipe["ingredients"] = reviewed["ingredients"]
            if "steps" in reviewed:
                recipe["steps"] = reviewed["steps"]
            
            # Save updated recipe
            with open(recipe_path, 'w', encoding='utf-8') as f:
                json.dump(recipe, f, ensure_ascii=False, indent=2)
            
            return (recipe_id, name_en, True, f"{len(changes)} changes", changes)
        else:
            return (recipe_id, name_en, True, "No changes needed", [])
    
    except Exception as e:
        return (recipe_id, recipe_id, False, f"Error: {str(e)[:100]}", [])


def main():
    print("=" * 70)
    print("  Translation Quality Review - 87 Recipes × 4 Languages")
    print(f"  Model: {MODEL}")
    print(f"  Workers: {MAX_WORKERS}")
    print("=" * 70)
    print()
    
    # Check for retry mode
    retry_mode = "--retry" in sys.argv
    
    # Collect recipe files
    if retry_mode and Path("translation_review_log.json").exists():
        # Only retry recipes that weren't in the success log
        existing_log = json.load(open("translation_review_log.json"))
        done_ids = set(rid for rid, _ in existing_log)
        all_files = sorted(RECIPES_DIR.glob("*.json"))
        recipe_files = [f for f in all_files if f.stem not in done_ids]
        print(f"RETRY MODE: {len(recipe_files)} failed recipes (skipping {len(done_ids)} already done)")
    else:
        recipe_files = sorted(RECIPES_DIR.glob("*.json"))
    
    total = len(recipe_files)
    print(f"Found {total} recipes to review")
    print()
    
    start_time = time.time()
    success = 0
    errors = 0
    total_changes = 0
    all_changes = []
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(review_recipe, f): f 
            for f in recipe_files
        }
        
        completed = 0
        for future in as_completed(futures):
            completed += 1
            recipe_id, name_en, ok, message, changes = future.result()
            
            if ok:
                success += 1
                if changes:
                    total_changes += len(changes)
                    all_changes.extend([(recipe_id, c) for c in changes])
                    status = f"✏️  {len(changes)} fixes"
                else:
                    status = "✓ perfect"
            else:
                errors += 1
                status = f"❌ {message}"
            
            # Verbose output
            print(f"[{completed:>3}/{total}] {status:<20} {name_en}")
            if changes:
                for c in changes:
                    field = c.get("field", "?")
                    reason = c.get("reason", "")
                    print(f"         └─ {field}: {reason}")
            
            sys.stdout.flush()
    
    elapsed = time.time() - start_time
    
    print()
    print("=" * 70)
    print(f"  Completed in {elapsed:.1f}s")
    print(f"  Success: {success}/{total}")
    print(f"  Errors: {errors}")
    print(f"  Total changes: {total_changes}")
    print("=" * 70)
    
    # Write/merge change log
    log_path = Path("translation_review_log.json")
    if retry_mode and log_path.exists():
        existing = json.load(open(log_path))
        merged = existing + all_changes
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        print(f"\n  Change log merged: {log_path} ({len(existing)} existing + {len(all_changes)} new)")
    elif all_changes:
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(all_changes, f, ensure_ascii=False, indent=2)
        print(f"\n  Change log: {log_path}")
    
    # Update TRANSLATION_REVIEW.md
    md = Path("TRANSLATION_REVIEW.md").read_text()
    md += f"\n\n## Run Results ({time.strftime('%Y-%m-%d %H:%M')})\n"
    md += f"- Recipes reviewed: {total}\n"
    md += f"- Successful: {success}\n"
    md += f"- Errors: {errors}\n"
    md += f"- Total changes: {total_changes}\n"
    md += f"- Duration: {elapsed:.1f}s\n"
    
    if all_changes:
        md += f"\n### Changes Summary\n"
        # Group by recipe
        by_recipe = {}
        for rid, c in all_changes:
            by_recipe.setdefault(rid, []).append(c)
        
        for rid, changes in sorted(by_recipe.items()):
            md += f"\n**{rid}** ({len(changes)} changes):\n"
            for c in changes:
                md += f"- `{c.get('field', '?')}`: {c.get('reason', '')}\n"
    
    Path("TRANSLATION_REVIEW.md").write_text(md)
    print(f"  Updated: TRANSLATION_REVIEW.md")


if __name__ == "__main__":
    main()
