#!/usr/bin/env python3
"""
Recipe Research Tool - Generate comprehensive historical/cultural context
Searches Wikipedia (Hebrew, Arabic, English) + recipe sites via Perplexity

Usage:
  python research_recipes.py --recipe "בשישה"
  python research_recipes.py --all  # Research all recipes without history files
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Try to import required libraries
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Paths
SAFED_RECIPES_DIR = Path("data/safed_recipes")
RESEARCH_DIR = Path("data/recipe_research")
RESEARCH_DIR.mkdir(parents=True, exist_ok=True)

# Configure APIs
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

if GEMINI_AVAILABLE and GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)


def vprint(*args, **kwargs):
    """Print with immediate flush."""
    print(*args, **kwargs, flush=True)


RESEARCH_PROMPT = """You are a culinary historian specializing in North African Jewish cuisine, particularly:
- Tunisian Jewish (especially Djerba) traditions
- Moroccan Jewish (especially Tangier) traditions
- Sephardic cuisine across the Maghreb

Research the dish "{dish_name}" and provide:

## 1. ETYMOLOGY (CRITICAL - GET THIS RIGHT!)
- What is the Arabic root of the name? (e.g., بسيسة from ب-س-س meaning "to mix")
- What does the name literally mean?
- Are there alternate spellings/names in different regions?
- DO NOT GUESS - if uncertain, say so

## 2. HISTORICAL ORIGINS
- Where did this dish originate? (Be specific: Tunisia, Morocco, Libya, etc.)
- Is it associated with specific Jewish communities (Djerba, Tangier, etc.)?
- How old is the tradition?

## 3. CULTURAL SIGNIFICANCE
- When is this dish traditionally served? (Shabbat, holidays, daily, ceremonies?)
- Any rituals or customs associated with it?
- Symbolic meaning?

## 4. REGIONAL VARIATIONS
- How does the Tunisian version differ from Moroccan?
- Israeli adaptations?
- Family variations?

## 5. TRADITIONAL INGREDIENTS
- What are the AUTHENTIC traditional ingredients?
- Which ingredients are essential vs. optional?

IMPORTANT NOTES:
- Search Wikipedia in Hebrew (ויקיפדיה), Arabic (ويكيبيديا), and English
- Cross-reference with recipe sites: אוכל טוב, מתכונים, 750g, Marmiton
- If the dish is commonly made with meat/fish/eggs, STATE THIS CLEARLY
- Be accurate - wrong etymology is worse than no etymology

Dish to research: {dish_name}
Hebrew name: {hebrew_name}
Any context from recipe: {context}
"""


def search_perplexity(query: str) -> str:
    """Search using Perplexity API for comprehensive web results."""
    if not PERPLEXITY_API_KEY or not REQUESTS_AVAILABLE:
        return ""
    
    vprint(f"  🔍 Searching Perplexity: {query[:50]}...")
    
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sonar",  # Updated model name
        "messages": [
            {
                "role": "system",
                "content": "You are a culinary research assistant. Search for accurate historical and cultural information about dishes. Include sources."
            },
            {
                "role": "user", 
                "content": query
            }
        ],
        "temperature": 0.2,
        "max_tokens": 2000,
        "return_citations": True
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        result = response.json()
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        vprint(f"    ✅ Got Perplexity response ({len(content)} chars)")
        return content
    except Exception as e:
        vprint(f"    ⚠️ Perplexity error: {e}")
        return ""


def research_with_gemini(dish_name: str, hebrew_name: str, context: str) -> str:
    """Use Gemini to synthesize research."""
    if not GEMINI_AVAILABLE or not GOOGLE_API_KEY:
        # NO FALLBACKS - crash if Gemini not configured
        raise RuntimeError("Gemini API not available - GOOGLE_API_KEY must be set in .env")
    
    vprint(f"  🧠 Researching with Gemini...")
    
    # First, gather web research via Perplexity
    web_research = ""
    
    # Search in multiple languages
    queries = [
        f'"{dish_name}" OR "{hebrew_name}" etymology origin history North African Jewish cuisine Wikipedia',
        f'بسيسة OR "{dish_name}" المطبخ اليهودي تونس المغرب تاريخ',  # Arabic
        f'"{hebrew_name}" מתכון מסורתי יהודי צפון אפריקה ויקיפדיה היסטוריה',  # Hebrew
    ]
    
    for query in queries:
        result = search_perplexity(query)
        if result:
            web_research += f"\n\n--- Search Result ---\n{result}"
    
    # Now use Gemini to synthesize
    prompt = RESEARCH_PROMPT.format(
        dish_name=dish_name,
        hebrew_name=hebrew_name,
        context=context
    )
    
    if web_research:
        prompt += f"\n\n## WEB RESEARCH RESULTS:\n{web_research}"
    
    model = genai.GenerativeModel(
        "gemini-2.0-flash",  # Fast model for research
        system_instruction="You are a culinary historian. Be accurate and cite sources. If uncertain, say so."
    )
    
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                max_output_tokens=3000,
            )
        )
        return response.text
    except Exception as e:
        # NO FALLBACKS - crash if Gemini fails
        raise RuntimeError(f"Gemini research failed for {dish_name}: {e}")


def research_recipe(recipe_file: Path) -> bool:
    """Research a single recipe and save history file."""
    
    # Load recipe
    with open(recipe_file, 'r', encoding='utf-8') as f:
        recipe = json.load(f)
    
    hebrew_name = recipe.get('name_hebrew', recipe.get('id', 'unknown'))
    recipe_id = recipe.get('id', recipe_file.stem)
    
    # Create English transliteration for filename
    transliteration = recipe_id.lower().replace(' ', '_').replace('-', '_')
    transliteration = re.sub(r'[^\w]', '', transliteration)
    if not transliteration or transliteration.isdigit():
        # Use Hebrew name transliteration
        transliteration = hebrew_name.lower().replace(' ', '_')
    
    output_file = RESEARCH_DIR / f"{transliteration}_history.md"
    
    vprint(f"\n📚 Researching: {hebrew_name}")
    
    # Gather context from recipe
    context_parts = []
    if 'ingredients' in recipe:
        ingredients = recipe['ingredients']
        if isinstance(ingredients, list):
            context_parts.append(f"Ingredients: {', '.join(ingredients[:5])}")
    if 'instructions' in recipe:
        instructions = recipe['instructions']
        if isinstance(instructions, list) and instructions:
            context_parts.append(f"Method hint: {instructions[0][:100]}")
    if 'metadata' in recipe and 'notes' in recipe['metadata']:
        context_parts.append(f"Notes: {recipe['metadata']['notes']}")
    
    context = "\n".join(context_parts) if context_parts else "No additional context"
    
    # Do research
    research_content = research_with_gemini(transliteration, hebrew_name, context)
    
    if not research_content:
        vprint(f"  ❌ No research generated for {hebrew_name}")
        return False
    
    # Format output
    output = f"""# {transliteration.upper().replace('_', ' ')} - HISTORY

**Hebrew Name:** {hebrew_name}
**Research Date:** {datetime.now().strftime('%Y-%m-%d')}

---

{research_content}

---

**Family Context:**
This recipe is from the Silver family cookbook, preserving traditions from:
- Cohen family (Djerba, Tunisia)
- Kadoch and Maloul families (Tangier, Morocco)

"""
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    vprint(f"  ✅ Saved: {output_file.name}")
    return True


def get_recipes_needing_research() -> list:
    """Find recipes without history files."""
    recipes = []
    
    for recipe_file in sorted(SAFED_RECIPES_DIR.glob("*.json")):
        # Check if history exists
        with open(recipe_file, 'r', encoding='utf-8') as f:
            recipe = json.load(f)
        
        recipe_id = recipe.get('id', recipe_file.stem)
        hebrew_name = recipe.get('name_hebrew', '')
        
        # Check various possible history file patterns
        has_history = False
        for pattern in [f"*{recipe_id}*_history.md", f"*{hebrew_name}*_history.md"]:
            if list(RESEARCH_DIR.glob(pattern)):
                has_history = True
                break
        
        if not has_history:
            recipes.append(recipe_file)
    
    return recipes


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Research recipe history and etymology")
    parser.add_argument("--recipe", "-r", help="Research specific recipe (Hebrew or English name)")
    parser.add_argument("--file", "-f", help="Research specific recipe file")
    parser.add_argument("--all", "-a", action="store_true", help="Research all recipes without history")
    parser.add_argument("--force", action="store_true", help="Re-research even if history exists")
    parser.add_argument("--list", "-l", action="store_true", help="List recipes needing research")
    
    args = parser.parse_args()
    
    if args.list:
        recipes = get_recipes_needing_research()
        vprint(f"Recipes needing research ({len(recipes)}):")
        for r in recipes:
            with open(r, 'r', encoding='utf-8') as f:
                recipe = json.load(f)
            vprint(f"  - {r.name}: {recipe.get('name_hebrew', 'unknown')}")
        return
    
    if args.file:
        recipe_file = Path(args.file)
        if not recipe_file.exists():
            recipe_file = SAFED_RECIPES_DIR / args.file
        if recipe_file.exists():
            research_recipe(recipe_file)
        else:
            vprint(f"❌ File not found: {args.file}")
        return
    
    if args.recipe:
        # Find recipe by name
        for recipe_file in SAFED_RECIPES_DIR.glob("*.json"):
            with open(recipe_file, 'r', encoding='utf-8') as f:
                recipe = json.load(f)
            if args.recipe in [recipe.get('name_hebrew'), recipe.get('id'), recipe_file.stem]:
                research_recipe(recipe_file)
                return
        vprint(f"❌ Recipe not found: {args.recipe}")
        return
    
    if args.all:
        if args.force:
            recipes = list(SAFED_RECIPES_DIR.glob("*.json"))
        else:
            recipes = get_recipes_needing_research()
        
        vprint(f"🔬 Researching {len(recipes)} recipes...")
        
        success = 0
        for recipe_file in recipes:
            if research_recipe(recipe_file):
                success += 1
        
        vprint(f"\n✅ Researched {success}/{len(recipes)} recipes")
        return
    
    parser.print_help()


if __name__ == "__main__":
    main()
