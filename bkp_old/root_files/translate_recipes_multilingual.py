#!/usr/bin/env python3
"""
Multilingual Translation Pipeline
Translates comprehensive recipe JSONs from English to Hebrew, Arabic, and Spanish.
"""

import json
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import openai

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
client = openai.OpenAI()

LANGUAGES = {
    'hebrew': 'Hebrew (עברית)',
    'arabic': 'Arabic (العربية)',
    'spanish': 'Spanish (Español)'
}

class RecipeTranslator:
    def __init__(self):
        self.recipes_dir = "data/recipes_comprehensive"
        self.output_dir = "data/recipes_comprehensive" # Update in place
        
    def load_recipe(self, filename):
        with open(Path(self.recipes_dir) / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_recipe(self, filename, data):
        with open(Path(self.output_dir) / filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def translate_content(self, content, target_lang, context=""):
        """Translate a string or list of strings"""
        if not content:
            return content
            
        is_list = isinstance(content, list)
        text_to_translate = json.dumps(content, ensure_ascii=False) if is_list else content
        
        prompt = f"""Translate the following text from English to {LANGUAGES[target_lang]}.
Context: This is for a cookbook of Tunisian-Djerban Jewish heritage.
Keep culinary terms authentic.
Maintain the tone: warm, informative, respectful.

Input:
{text_to_translate}

Return ONLY the translated text (or JSON list). No markdown, no explanations."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            result = response.choices[0].message.content.strip()
            
            if is_list:
                try:
                    return json.loads(result)
                except:
                    # Fallback if JSON parsing fails, treat as newline separated or just return text
                    return [result]
            return result
        except Exception as e:
            print(f"Translation error ({target_lang}): {e}")
            return content

    def translate_recipe(self, recipe):
        print(f"Translating {recipe['names']['english']}...")
        
        for lang_key in LANGUAGES.keys():
            print(f"  > {lang_key}...")
            
            # 1. Name
            if not recipe['names'].get(lang_key) or "TODO" in recipe['names'][lang_key]:
                recipe['names'][lang_key] = self.translate_content(recipe['names']['english'], lang_key, "Recipe Title")

            # 2. Ingredients (List of objects)
            # We need to translate 'name' and 'unit' inside each object
            # To save tokens/calls, we'll batch translate
            ing_list_en = recipe['ingredients']['english']
            # Prepare batch
            items_to_translate = [f"{i.get('amount','')} {i.get('unit','')} {i.get('name','')}".strip() for i in ing_list_en]
            
            # We actually need structure back. Let's just translate the list of ingredient strings for now
            # Or better, ask LLM to return structured JSON of translated ingredients.
            
            ing_prompt = f"""Translate these recipe ingredients to {LANGUAGES[lang_key]}.
Input JSON:
{json.dumps(ing_list_en, ensure_ascii=False)}

Output JSON (same structure, translated 'name' and 'unit', keep 'amount' as is):"""
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": ing_prompt}],
                    response_format={"type": "json_object"}
                )
                translated_ings = json.loads(response.choices[0].message.content)
                # Handle if it returns wrapped object
                if 'ingredients' in translated_ings:
                    recipe['ingredients'][lang_key] = translated_ings['ingredients']
                elif isinstance(translated_ings, list):
                    recipe['ingredients'][lang_key] = translated_ings
                else:
                    # Fallback: try to find list in values
                    for v in translated_ings.values():
                        if isinstance(v, list):
                            recipe['ingredients'][lang_key] = v
                            break
            except Exception as e:
                print(f"    x Ingredients error: {e}")

            # 3. Instructions (List of objects)
            inst_list_en = recipe['instructions']['english']
            inst_prompt = f"""Translate these cooking instructions to {LANGUAGES[lang_key]}.
Input JSON:
{json.dumps(inst_list_en, ensure_ascii=False)}

Output JSON (same structure, translated 'text', keep 'step'):"""
            
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": inst_prompt}],
                    response_format={"type": "json_object"}
                )
                translated_inst = json.loads(response.choices[0].message.content)
                if 'instructions' in translated_inst:
                    recipe['instructions'][lang_key] = translated_inst['instructions']
                elif isinstance(translated_inst, list):
                    recipe['instructions'][lang_key] = translated_inst
                else:
                    for v in translated_inst.values():
                        if isinstance(v, list):
                            recipe['instructions'][lang_key] = v
                            break
            except Exception as e:
                print(f"    x Instructions error: {e}")

            # 4. Sections (Etymology, History, Tradition)
            for section in ['etymology', 'history', 'djerban_tradition']:
                if section in recipe and 'english' in recipe[section]:
                    # Translate summary primarily
                    summary = recipe[section]['english'].get('summary', '')
                    if summary:
                        recipe[section][lang_key] = recipe[section].get(lang_key, {})
                        recipe[section][lang_key]['summary'] = self.translate_content(summary, lang_key)

        return recipe

    def run(self):
        files = sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
        print(f"Found {len(files)} recipes to translate.")
        
        for filename in files:
            recipe = self.load_recipe(filename)
            updated_recipe = self.translate_recipe(recipe)
            self.save_recipe(filename, updated_recipe)
            print(f"Saved {filename}")
            # time.sleep(1) # Rate limit buffer

if __name__ == "__main__":
    translator = RecipeTranslator()
    translator.run()
