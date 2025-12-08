#!/usr/bin/env python3
"""
Translate Hebrew recipes from safed_recipes to English with proper formatting
"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

def translate_recipe(recipe_data):
    """Translate a single recipe to English"""
    
    hebrew_name = recipe_data.get('name_hebrew', '')
    ingredients = recipe_data.get('ingredients', [])
    instructions = recipe_data.get('instructions', [])
    
    # Create a structured prompt for translation
    prompt = f"""Translate this Tunisian-Djerban Jewish recipe from Hebrew to English. 
Make it proper, clear, and professional for a cookbook.

HEBREW NAME: {hebrew_name}

INGREDIENTS (Hebrew):
{chr(10).join(ingredients)}

INSTRUCTIONS (Hebrew):
{chr(10).join(instructions)}

Please provide ONLY the response in this exact JSON format (no markdown, no extra text):
{{
  "name_english": "English recipe name",
  "ingredients_english": [
    "Ingredient 1",
    "Ingredient 2"
  ],
  "instructions_english": [
    "Step 1",
    "Step 2"
  ],
  "notes": "Any cultural or cooking notes"
}}

Keep ingredient amounts and measurements in their original form if mentioned.
Preserve the structure and numbering of steps.
Make it natural and clear English, suitable for an international cookbook."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
        
    except Exception as e:
        print(f"❌ Error translating {hebrew_name}: {e}")
        return None

def process_all_recipes():
    """Process all recipes in the safed_recipes folder"""
    
    input_dir = "data/safed_recipes"
    output_dir = "data/safed_recipes_en"
    
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    recipe_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.json')])
    
    print(f"Found {len(recipe_files)} recipes to translate...")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for i, filename in enumerate(recipe_files, 1):
        file_path = os.path.join(input_dir, filename)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            recipe_data = json.load(f)
        
        hebrew_name = recipe_data.get('name_hebrew', 'Unknown')
        print(f"\n[{i}/{len(recipe_files)}] Translating: {hebrew_name}")
        
        # Translate
        translated = translate_recipe(recipe_data)
        
        if translated:
            # Create the English recipe object
            english_recipe = {
                "id": translated.get('name_english', '').lower().replace(' ', '_'),
                "name_hebrew": hebrew_name,
                "name_english": translated.get('name_english', ''),
                "ingredients": translated.get('ingredients_english', []),
                "instructions": translated.get('instructions_english', []),
                "notes": translated.get('notes', ''),
                "metadata": {
                    "source": "safed_some.md",
                    "translated_from_hebrew": True,
                    "original_json": filename
                }
            }
            
            # Save to output directory
            output_filename = filename.replace('.json', '_en.json')
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(english_recipe, f, indent=2, ensure_ascii=False)
            
            print(f"   ✓ Saved: {translated.get('name_english', 'Unknown')}")
            successful += 1
        else:
            print(f"   ✗ Failed to translate")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Translation complete!")
    print(f"✓ Successful: {successful}/{len(recipe_files)}")
    print(f"✗ Failed: {failed}/{len(recipe_files)}")
    print(f"Output directory: {output_dir}")

if __name__ == "__main__":
    process_all_recipes()

