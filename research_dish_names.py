#!/usr/bin/env python3
"""
Research Dish Name Origins

Processes canonical recipes to research and enrich the etymology of dish names.
Uses web search + Gemini to find:
- True linguistic origins (Arabic, Hebrew, Ladino, French, etc.)
- Alternative names and spellings
- Similar dishes from other cultures
- Confidence level of the etymology

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

# Thread-safe progress tracking
_progress_lock = Lock()
_progress_count = 0

# ============================================================================
# CONFIGURATION - NEVER CHANGE MODEL
# ============================================================================
GEMINI_MODEL = "gemini-3-pro-preview"
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Paths
CANONICAL_DIR = Path("data/recipes_canonical")
RESEARCH_CACHE_DIR = Path("data/name_research_cache")

# Create directories
RESEARCH_CACHE_DIR.mkdir(parents=True, exist_ok=True)

def vprint(*args, **kwargs):
    """Print with immediate flush for real-time output."""
    print(*args, **kwargs, flush=True)


# ============================================================================
# WEB SEARCH FUNCTION
# ============================================================================
def search_web(query: str) -> str:
    """Search the web using Gemini's grounding with Google Search."""
    
    model = genai.GenerativeModel(GEMINI_MODEL)
    
    # Use Gemini with search grounding
    search_prompt = f"""Search the web and find information about: {query}

Focus on:
- Etymology and linguistic origins
- Historical references
- Regional variations
- Academic or culinary sources

Return a summary of what you found."""

    try:
        response = model.generate_content(
            search_prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                max_output_tokens=2048,
            ),
            tools=[{"google_search": {}}]
        )
        
        if response.candidates and response.candidates[0].content.parts:
            return response.text
        return ""
    except Exception as e:
        vprint(f"    ⚠️  Web search failed: {e}")
        return ""


# ============================================================================
# ETYMOLOGY RESEARCH SYSTEM PROMPT
# ============================================================================
RESEARCH_SYSTEM_PROMPT = """You are an expert etymologist and culinary historian specializing in:
- North African Jewish cuisine (Tunisian, Moroccan, Algerian, Libyan)
- Judeo-Arabic languages and dialects
- Ladino (Judeo-Spanish)
- Hebrew culinary terminology
- French colonial influence on Maghrebi cuisine

## YOUR TASK
Research the TRUE etymology of dish names from a Djerban Jewish cookbook.

## CRITICAL KNOWLEDGE

### Tunisian Arabic (Derja) Notes:
- "Adma" (عظمة) = egg in Tunisian (NOT "beyda" like in standard Arabic!)
- "Mhamsa" (محمصة) = from "حمّص" (to toast/roast)
- "Brik" = from Turkish "börek"
- Many dish names come from verbs describing cooking method

### French Influence:
- "Cholent" = from French "chaud lent" (slow heat)
- "Fricassée" = French cooking term adopted in Tunisia
- Many baking terms have French origins

### Ladino/Spanish:
- Some dishes have Spanish/Ladino names from Sephardic traditions
- "Adafina" = from Arabic "dafina" (buried/hidden) - the Shabbat stew

### Research Approach:
1. Look at the Hebrew name and transliterate it
2. Check if it's Arabic (Tunisian Derja, Moroccan Darija, or Fus'ha)
3. Check if it's Ladino/Spanish
4. Check if it's French
5. Check if it's Hebrew
6. Check if it's Turkish/Ottoman
7. Consider verb roots (most dish names describe the cooking action)

## OUTPUT REQUIREMENTS
You MUST be honest about your confidence level:
- "confirmed" = found in reliable etymological sources
- "likely" = strong linguistic evidence but not confirmed
- "possible" = educated guess based on patterns
- "unknown" = cannot determine origin

## SIMILAR DISHES
List dishes from OTHER cultures that are similar (not Jewish versions):
- Tunisian Muslim version
- Moroccan version  
- Turkish equivalent
- Middle Eastern parallels
- European parallels"""


RESEARCH_USER_PROMPT = """Research the etymology and origins of this dish:

## DISH INFORMATION:
- **Hebrew Name**: {name_hebrew}
- **English Name**: {name_english}
- **Current Description**: {description}
- **Current Origin Note**: {current_origin}

## WEB SEARCH RESULTS:
{web_search_results}

## REQUIRED OUTPUT (JSON):
```json
{{
  "name_origin": {{
    "etymology": "Detailed explanation of the name's origin. Be specific about which language/dialect.",
    "language_source": "tunisian_arabic | moroccan_arabic | hebrew | ladino | french | turkish | other",
    "root_word": "The original word/root if known",
    "meaning": "What the name literally means",
    "confidence": "confirmed | likely | possible | unknown",
    "sources_notes": "Notes about where this information comes from or why you're confident/uncertain"
  }},
  "alternative_names": [
    {{
      "name": "Alternative spelling or name",
      "language": "which language",
      "notes": "context for this variant"
    }}
  ],
  "similar_dishes": [
    {{
      "name": "Name of similar dish",
      "culture": "Which culture/region",
      "similarity": "How it's similar",
      "key_difference": "Main difference from the Jewish version"
    }}
  ]
}}
```

Be thorough and scholarly. If you're uncertain, say so. Return ONLY valid JSON."""


def research_dish_name(recipe: dict, use_web_search: bool = True) -> dict:
    """Research the etymology of a single dish name."""
    
    recipe_id = recipe.get("id", "unknown")
    name_hebrew = recipe.get("name_hebrew", "")
    name_english = recipe.get("name", "")
    description = recipe.get("description", "")
    current_origin = recipe.get("name_origin", "")
    
    vprint(f"  🔍 Researching: {name_english} ({name_hebrew})")
    
    # Perform web searches
    web_results = ""
    if use_web_search:
        queries = [
            f'"{name_hebrew}" etymology origin meaning',
            f'"{name_english}" Tunisian Jewish dish origin',
            f'"{name_hebrew}" Arabic word meaning food',
        ]
        
        for query in queries:
            vprint(f"    🌐 Searching: {query[:50]}...")
            result = search_web(query)
            if result:
                web_results += f"\n### Search: {query}\n{result}\n"
            time.sleep(1)  # Rate limiting
    
    # Build the research prompt
    prompt = RESEARCH_USER_PROMPT.format(
        name_hebrew=name_hebrew,
        name_english=name_english,
        description=description,
        current_origin=current_origin,
        web_search_results=web_results if web_results else "No web search results available."
    )
    
    model = genai.GenerativeModel(
        GEMINI_MODEL,
        system_instruction=RESEARCH_SYSTEM_PROMPT
    )
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=4096,
                )
            )
            
            if not response.candidates or not response.candidates[0].content.parts:
                if attempt < max_retries - 1:
                    vprint(f"    ⚠️  Empty response, retrying...")
                    time.sleep(2)
                    continue
                else:
                    raise RuntimeError(f"Empty response after {max_retries} attempts")
            
            response_text = response.text.strip()
            
            # Remove markdown code blocks
            if response_text.startswith("```"):
                response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
                response_text = re.sub(r'\n?```$', '', response_text)
            
            research_data = json.loads(response_text)
            vprint(f"    ✅ Research complete")
            return research_data
            
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  JSON parse error, retrying...")
                time.sleep(2)
                continue
            else:
                vprint(f"    ❌ JSON parse failed: {e}")
                vprint(f"    Response: {response_text[:500]}...")
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                vprint(f"    ⚠️  Error: {e}, retrying...")
                time.sleep(2)
                continue
            raise
    
    raise RuntimeError(f"Research failed for {recipe_id}")


def update_recipe_with_research(recipe_file: Path, research_data: dict) -> dict:
    """Update a canonical recipe with research findings."""
    
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    # Update name_origin with full etymology
    name_origin = research_data.get("name_origin", {})
    etymology = name_origin.get("etymology", "")
    confidence = name_origin.get("confidence", "unknown")
    language = name_origin.get("language_source", "")
    root = name_origin.get("root_word", "")
    meaning = name_origin.get("meaning", "")
    
    # Build comprehensive origin string
    origin_parts = []
    if etymology:
        origin_parts.append(etymology)
    if confidence != "confirmed":
        origin_parts.append(f"(Confidence: {confidence})")
    
    recipe["name_origin"] = " ".join(origin_parts) if origin_parts else recipe.get("name_origin", "")
    
    # Add new fields
    recipe["name_etymology"] = {
        "language_source": language,
        "root_word": root,
        "meaning": meaning,
        "confidence": confidence,
        "notes": name_origin.get("sources_notes", "")
    }
    
    recipe["alternative_names"] = research_data.get("alternative_names", [])
    recipe["similar_dishes"] = research_data.get("similar_dishes", [])
    
    # Save updated recipe
    with open(recipe_file, 'w', encoding='utf-8') as f:
        json.dump(recipe, f, ensure_ascii=False, indent=2)
    
    return recipe


def research_single(recipe_id: str, use_web_search: bool = True):
    """Research a single recipe by ID."""
    recipe_file = CANONICAL_DIR / f"{recipe_id}.json"
    
    if not recipe_file.exists():
        vprint(f"❌ File not found: {recipe_file}")
        return None
    
    vprint(f"🔬 Researching etymology: {recipe_id}")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Web search: {'enabled' if use_web_search else 'disabled'}")
    
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        # Research
        research_data = research_dish_name(recipe, use_web_search=use_web_search)
        
        # Cache the research
        cache_file = RESEARCH_CACHE_DIR / f"{recipe_id}_research.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, ensure_ascii=False, indent=2)
        vprint(f"  💾 Cached research: {cache_file.name}")
        
        # Update the recipe
        updated = update_recipe_with_research(recipe_file, research_data)
        
        vprint(f"\n✅ Updated: {recipe_file.name}")
        vprint(f"\n📖 Etymology: {updated.get('name_origin', 'N/A')}")
        
        if updated.get("alternative_names"):
            vprint(f"\n📝 Alternative names:")
            for alt in updated["alternative_names"]:
                vprint(f"   - {alt.get('name')} ({alt.get('language')})")
        
        if updated.get("similar_dishes"):
            vprint(f"\n🌍 Similar dishes from other cultures:")
            for sim in updated["similar_dishes"]:
                vprint(f"   - {sim.get('name')} ({sim.get('culture')})")
        
        return updated
        
    except Exception as e:
        vprint(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def process_single_recipe_task(recipe_file: Path, use_web_search: bool, total: int, skip_existing: bool) -> dict:
    """Process a single recipe (for parallel execution)."""
    global _progress_count
    
    recipe_id = recipe_file.stem
    result = {
        "recipe_id": recipe_id,
        "success": False,
        "skipped": False,
        "error": None
    }
    
    # Check if already researched
    if skip_existing:
        cache_file = RESEARCH_CACHE_DIR / f"{recipe_id}_research.json"
        if cache_file.exists():
            with _progress_lock:
                _progress_count += 1
                vprint(f"⏭️  [{_progress_count}/{total}] Skipping (cached): {recipe_id}")
            result["skipped"] = True
            return result
    
    try:
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        research_data = research_dish_name(recipe, use_web_search=use_web_search)
        
        # Cache
        cache_file = RESEARCH_CACHE_DIR / f"{recipe_id}_research.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, ensure_ascii=False, indent=2)
        
        # Update recipe
        update_recipe_with_research(recipe_file, research_data)
        
        result["success"] = True
        
        with _progress_lock:
            _progress_count += 1
            vprint(f"✅ [{_progress_count}/{total}] Done: {recipe_id}")
            
    except Exception as e:
        with _progress_lock:
            _progress_count += 1
            vprint(f"❌ [{_progress_count}/{total}] Failed {recipe_id}: {e}")
        result["error"] = str(e)
    
    return result


def research_all(use_web_search: bool = True, limit: int = None, skip_existing: bool = True, workers: int = 30):
    """Research all canonical recipes with parallel processing."""
    global _progress_count
    _progress_count = 0
    
    recipe_files = sorted([f for f in CANONICAL_DIR.glob("*.json")])
    
    if limit:
        recipe_files = recipe_files[:limit]
    
    total = len(recipe_files)
    
    vprint(f"🔬 Researching etymology for {total} recipes...")
    vprint(f"   Model: {GEMINI_MODEL}")
    vprint(f"   Workers: {workers} (parallel)")
    vprint(f"   Web search: {'enabled' if use_web_search else 'disabled'}")
    vprint(f"   Skip existing: {skip_existing}")
    vprint()
    vprint("=" * 60)
    
    results = {"success": [], "skipped": [], "failed": []}
    
    # Process in parallel
    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_file = {
            executor.submit(process_single_recipe_task, f, use_web_search, total, skip_existing): f
            for f in recipe_files
        }
        
        for future in as_completed(future_to_file):
            recipe_file = future_to_file[future]
            try:
                result = future.result()
                if result["skipped"]:
                    results["skipped"].append(result["recipe_id"])
                elif result["success"]:
                    results["success"].append(result["recipe_id"])
                else:
                    results["failed"].append({
                        "recipe_id": result["recipe_id"],
                        "error": result["error"]
                    })
            except Exception as e:
                vprint(f"❌ Exception for {recipe_file.name}: {e}")
                results["failed"].append({
                    "recipe_id": recipe_file.stem,
                    "error": str(e)
                })
    
    # Summary
    vprint()
    vprint("=" * 60)
    vprint("📊 RESEARCH SUMMARY")
    vprint("=" * 60)
    vprint(f"✅ Successful: {len(results['success'])}")
    vprint(f"⏭️  Skipped: {len(results['skipped'])}")
    vprint(f"❌ Failed: {len(results['failed'])}")
    
    if results["failed"]:
        vprint("\nFailed recipes:")
        for fail in results["failed"]:
            vprint(f"  - {fail['recipe_id']}: {fail['error']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Research dish name etymologies")
    parser.add_argument("--single", "-s", help="Research single recipe by ID")
    parser.add_argument("--limit", "-n", type=int, help="Process only N recipes")
    parser.add_argument("--workers", "-w", type=int, default=30, help="Number of parallel workers (default: 30)")
    parser.add_argument("--no-web", action="store_true", help="Disable web search")
    parser.add_argument("--force", "-f", action="store_true", help="Re-research even if cached")
    parser.add_argument("--list", "-l", action="store_true", help="List available recipes")
    
    args = parser.parse_args()
    
    if args.list:
        print("Available canonical recipes:")
        for i, f in enumerate(sorted(CANONICAL_DIR.glob("*.json"))):
            print(f"  {i:2d}. {f.stem}")
        sys.exit(0)
    
    if args.single:
        research_single(args.single, use_web_search=not args.no_web)
    else:
        research_all(
            use_web_search=not args.no_web,
            limit=args.limit,
            skip_existing=not args.force,
            workers=args.workers
        )

