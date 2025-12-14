#!/usr/bin/env python3
"""
Fix intro paragraphs and etymology for specific recipes based on review feedback.
"""

import json
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

CANONICAL_DIR = Path("data/recipes_canonical")

# Recipes to fix with specific instructions
FIXES = {
    "adafina": """
        - Remove parenthetical translations from the name discussion
        - This is for the traditional Shabbat MORNING meal, NOT lunch
        - Keep it concise (40-60 words)
    """,
    
    "adafina_wheat_side_dish": """
        - Focus etymology on "Trigo" (Spanish) and "Hita" (Arabic), NOT on Adafina
        - English name is "Wheat Berries"
        - Remove any mention that the vegan version is special - wheat is naturally vegan
        - Keep it concise (40-60 words)
    """,
    
    "artichoke_mushrooms_stew": """
        - Remove "Gannariya" from the intro - it's not the original name
        - This dish is from TANGIER (Enny's side), NOT Djerba
        - Just mention it's a popular Shabbat dish in our house
        - Keep it concise (40-60 words)
    """,
    
    "baked_potato_levivot": """
        - This is NOT Ma'akouda - don't mention that
        - It's also known as Latkes (Yiddish, from East Slavic "oladka" or "latka" meaning "small fried pancake")
        - Keep it concise (40-60 words)
    """,
    
    "banana_cake": """
        - The vegan version uses simple applesauce as egg replacement, not ריוויון
        - Don't explain what "cake" means - skip empty etymology
        - Just focus on it being a family favorite
        - Keep it concise (40-60 words)
    """,
    
    "biscoti_judy": """
        - Judy is simply a friend who shared this recipe with the family
        - No elaborate etymology needed
        - Keep it concise (40-60 words)
    """,
    
    "cholent": """
        - Add that Cholent is the Eastern European version of:
          - Adafina (Moroccan)
          - Tfina (Tunisian)
        - The word "Cholent" comes from French "chalant" (warm)
        - Keep it concise (40-60 words)
    """,
    
    "chraime_spicy_fish_stew": """
        - Keep existing etymology about Chraime
        - Add that in the vegan version, the seaweed is mixed with tofu to give it a fish-like aroma and appearance
        - Keep it concise (40-60 words)
    """,
    
    "ciceritos": """
        - IMPORTANT: Chicharos/Chicharitos means GREEN PEAS in Ladino, NOT chickpeas!
        - This is a green pea stew, not chickpea
        - Etymology: From the Spanish "chícharo" (pea), with the Ladino diminutive "-itos"
        - Keep it concise (40-60 words)
    """,
    
    "honey_cake_mami": """
        - "Mami" means "Mom" in many cultures
        - This is Enny's mom's recipe
        - Keep it concise (40-60 words)
    """,
    
    "mocha_java_cake": """
        - Mocha-Java refers to:
          - Mocha = port city in Yemen
          - Java = Indonesian island
        - These were historic coffee trading origins
        - Keep it concise (40-60 words)
    """,
    
    "original_toll_house_chocolate_chip_cookies": """
        - Remove "מתכון מקורי" - it's redundant
        - Keep the Toll House Inn origin story
        - Keep it concise (40-60 words)
    """,
    
    "pancakes_soly": """
        - Soly is Enny's sister, named Sol (Spanish for "sun")
        - She's from Tangier, Morocco
        - Keep it concise (40-60 words)
    """,
    
    "pancakes_efrat_shachor": """
        - Just call it "Efrat's Pancakes" - no surname needed
        - It's simply a favorite breakfast recipe, not a Djerban tradition
        - Keep it concise (40-60 words)
    """,
    
    "potache_white_bean_stew": """
        - The Hebrew name is פוטאכס (Potaches)
        - Related to Spanish "Potaje" (stew)
        - Keep it concise (40-60 words)
    """,
    
    "sfingh": """
        - Add that we have two similar recipes (Sfingh and Sfenj) because they came through different sides of the family
        - Different pronunciation and minor differences, but we kept both!
        - Keep it concise (40-60 words)
    """,
    
    "shlomit_tomato_salad": """
        - Shlomit is a family friend, not a relative
        - Yerachmiel (11 years old) simply loves this salad
        - Keep it concise (40-60 words)
    """,
    
    "tbikha_tomatem": """
        - Explain that "Tomatem" (תטמטם) is the Judeo-Tunisian word for tomatoes
        - Keep it concise (40-60 words)
    """,
}


def fix_recipe_intro(recipe_id: str, fix_instructions: str) -> dict:
    """Fix the intro paragraph for a recipe based on instructions."""
    recipe_file = CANONICAL_DIR / f"{recipe_id}.json"
    
    if not recipe_file.exists():
        return {"id": recipe_id, "status": "error", "message": "File not found"}
    
    with open(recipe_file) as f:
        recipe = json.load(f)
    
    # Build prompt
    prompt = f"""You are updating the intro_paragraph for a cookbook recipe.

RECIPE NAME: {recipe.get('name', recipe_id)}
HEBREW NAME: {recipe.get('name_hebrew', '')}
CURRENT INTRO: {recipe.get('intro_paragraph', 'None')}
CURRENT NAME_ORIGIN: {recipe.get('name_origin', 'None')[:500]}

SPECIFIC FIX INSTRUCTIONS:
{fix_instructions}

RULES:
- Write ONLY the new intro_paragraph text (40-60 words, max 320 characters)
- No markdown, no asterisks, no special formatting
- Be concise and factual
- Focus on what the dish IS and its cultural/linguistic origin
- If a vegan adaptation, mention it briefly but don't overemphasize

OUTPUT: Just the intro paragraph text, nothing else."""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200,
                temperature=0.3,
            )
        )
        
        new_intro = response.text.strip().strip('"').strip("'")
        
        # Update recipe
        old_intro = recipe.get('intro_paragraph', '')
        recipe['intro_paragraph'] = new_intro
        
        with open(recipe_file, 'w') as f:
            json.dump(recipe, f, indent=2, ensure_ascii=False)
        
        return {
            "id": recipe_id,
            "status": "success",
            "old": old_intro[:100] + "..." if len(old_intro) > 100 else old_intro,
            "new": new_intro
        }
        
    except Exception as e:
        return {"id": recipe_id, "status": "error", "message": str(e)}


def main():
    print("=" * 60)
    print("FIXING INTRO PARAGRAPHS")
    print("=" * 60)
    print(f"\nRecipes to fix: {len(FIXES)}")
    print()
    
    results = []
    
    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {
            executor.submit(fix_recipe_intro, recipe_id, instructions): recipe_id
            for recipe_id, instructions in FIXES.items()
        }
        
        for future in as_completed(futures):
            recipe_id = futures[future]
            result = future.result()
            results.append(result)
            
            if result["status"] == "success":
                print(f"✅ {recipe_id}")
                print(f"   New: {result['new'][:80]}...")
            else:
                print(f"❌ {recipe_id}: {result.get('message', 'Unknown error')}")
    
    print()
    print("=" * 60)
    print(f"Done! {sum(1 for r in results if r['status'] == 'success')}/{len(FIXES)} fixed")
    print("=" * 60)


if __name__ == "__main__":
    main()

