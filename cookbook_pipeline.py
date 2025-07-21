#!/usr/bin/env python3
"""
Vegan Djerban Family Cookbook - Complete AI Pipeline
Automated generation from CSV to final LaTeX book

Pipeline: CSV → Research → Synthesis → Recipe Generation → Translation → Image Generation → LaTeX
"""

import os
import sys
import csv
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime
import re
import requests

# Import AI libraries
try:
    import openai
    import google.generativeai as genai
    from perplexipy import PerplexityClient
except ImportError as e:
    print(f"❌ Missing required package: {e}")
    sys.exit(1)

load_dotenv()

class CookbookPipeline:
    def __init__(self):
        self.setup_directories()
        self.setup_ai_clients()
        self.recipes_data = []
        self.progress_log = []
        
    def setup_directories(self):
        """Create project directory structure"""
        dirs = [
            "data/research",
            "data/recipes/markdown", 
            "data/recipes/translations",
            "data/images/generated",
            "latex/chapters",
            "latex/recipes/english",
            "latex/recipes/hebrew", 
            "latex/recipes/spanish",
            "latex/recipes/arabic",
            "latex/images",
            "latex/styles",
            "latex/fonts",
            "output"
        ]
        
        for dir_path in dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
        print("📁 Project directory structure created")
        
    def setup_ai_clients(self):
        """Initialize AI service clients"""
        try:
            # OpenAI
            self.openai_client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            # Google Gemini
            genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
            self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            
            # Perplexity
            self.perplexity_client = PerplexityClient(key=os.getenv('PERPLEXITY_API_KEY'))
            
            print("🤖 AI clients initialized successfully")
            
        except Exception as e:
            print(f"❌ Error setting up AI clients: {e}")
            sys.exit(1)
    
    def load_recipes_csv(self, csv_path="RecipesDjerba.csv"):
        """Load recipes from CSV file"""
        recipes = []
        
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['SOURCE'] and row['Dish (Hebrew)']:  # Skip empty rows
                    recipes.append({
                        'source': row['SOURCE'],
                        'hebrew_name': row['Dish (Hebrew)'],
                        'description': row['Dish description'],
                        'english_name': row['Dish (English)'],
                        'native_name': row['Dish native name (Tunisia, Morocco, Israel)'],
                        'type': row['Type (Main/Side/Dip/Soup/Snack)'],
                        'served': row['Served (Hot/Cold)'],
                        'flavor': row['Flavor (Sweet/Savory)'],
                        'notes': row['Notes']
                    })
        
        print(f"📋 Loaded {len(recipes)} recipes from CSV")
        return recipes
    
    def research_dish_etymology(self, recipe):
        """Step 1: Research dish etymology and cultural context using Perplexity"""
        print(f"🔍 Researching etymology for: {recipe['english_name']}")
        
        # Determine origin for prompt
        if 'Cohen-Trabelsi' in recipe['source']:
            origin_context = "in Tunisian Jewish cuisine from Djerba"
            community = "Djerban"
        elif 'Kadoch-Muyal' in recipe['source']:
            origin_context = "in Moroccan Jewish cuisine from Tangier"
            community = "Tangier"
        else:
            origin_context = "in North African Jewish cuisine"
            community = "North African Jewish"
            
        prompt = f"""Research the dish "{recipe['english_name']}" ({recipe['hebrew_name']}) {origin_context}:

1. Etymology and meaning of the name
2. Historical significance in {community} Jewish community  
3. Traditional preparation methods and ingredients
4. Cultural context (Sabbath, holidays, daily meals)
5. Regional variations across North African Jewish communities
6. Differences between Tunisian and Moroccan Jewish culinary traditions
7. Any connection to Sephardic or Mizrahi culinary traditions

Description from family: {recipe['description']}
Native names: {recipe['native_name']}
Type: {recipe['type']}, Served: {recipe['served']}, Flavor: {recipe['flavor']}
"""
        
        try:
            response = self.perplexity_client.query(prompt)
            
            # Save research
            research_file = f"data/research/{self.safe_filename(recipe['english_name'])}_etymology.txt"
            with open(research_file, 'w', encoding='utf-8') as f:
                f.write(f"ETYMOLOGY RESEARCH: {recipe['english_name']}\n")
                f.write("=" * 50 + "\n\n")
                f.write(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Error researching etymology: {e}")
            return f"Error: Unable to research etymology - {e}"
    
    def research_veganization(self, recipe):
        """Step 2: Research veganization strategies using Perplexity"""  
        print(f"🌱 Researching veganization for: {recipe['english_name']}")
        
        # Determine origin for prompt
        if 'Cohen-Trabelsi' in recipe['source']:
            origin_context = "from Tunisian Jewish cuisine"
        elif 'Kadoch-Muyal' in recipe['source']:
            origin_context = "from Moroccan Jewish cuisine" 
        else:
            origin_context = "from North African Jewish cuisine"
            
        prompt = f"""Find information about veganizing "{recipe['english_name']}" - a traditional {recipe['type']} {origin_context}:

1. Any existing traditional vegan versions in North African Jewish cooking
2. Common plant-based substitutions for typical ingredients in this dish type
3. Techniques to maintain authentic flavors without animal products
4. Modern vegan adaptations while preserving cultural authenticity
5. Regional differences in ingredient availability (Tunisia vs Morocco)
6. Nutritional considerations for substitutions

Traditional description: {recipe['description']}
Dish type: {recipe['type']}
Flavor profile: {recipe['flavor']}
Serving style: {recipe['served']}
"""
        
        try:
            response = self.perplexity_client.query(prompt)
            
            # Save research
            research_file = f"data/research/{self.safe_filename(recipe['english_name'])}_vegan.txt"
            with open(research_file, 'w', encoding='utf-8') as f:
                f.write(f"VEGANIZATION RESEARCH: {recipe['english_name']}\n")
                f.write("=" * 50 + "\n\n")
                f.write(response)
            
            return response
            
        except Exception as e:
            print(f"❌ Error researching veganization: {e}")
            return f"Error: Unable to research veganization - {e}"
    
    def synthesize_research(self, recipe, etymology_research, vegan_research):
        """Step 3: Synthesize research using Gemini"""
        print(f"🧠 Synthesizing research for: {recipe['english_name']}")
        
        prompt = f"""Compile and synthesize the following research about "{recipe['english_name']}" ({recipe['hebrew_name']}):

ETYMOLOGY & CULTURAL RESEARCH:
{etymology_research}

VEGANIZATION RESEARCH:
{vegan_research}

FAMILY CONTEXT:
- Source: {recipe['source']}
- Traditional description: {recipe['description']}
- Type: {recipe['type']}
- Notes: {recipe['notes']}

Create a structured report including:
1. Cultural Background & Etymology
2. Traditional Preparation Overview  
3. Vegan Adaptation Strategy
4. Key Ingredients & Substitutions
5. Cultural Significance & Family Context
6. Preparation Tips & Techniques

Focus on preserving authenticity while enabling plant-based preparation."""
        
        try:
            response = self.gemini_model.generate_content(prompt)
            synthesis = response.text
            
            # Save synthesis
            synthesis_file = f"data/research/{self.safe_filename(recipe['english_name'])}_synthesis.txt"
            with open(synthesis_file, 'w', encoding='utf-8') as f:
                f.write(f"RESEARCH SYNTHESIS: {recipe['english_name']}\n")
                f.write("=" * 50 + "\n\n")
                f.write(synthesis)
            
            return synthesis
            
        except Exception as e:
            print(f"❌ Error synthesizing research: {e}")
            return f"Error: Unable to synthesize research - {e}"
    
    def generate_recipe(self, recipe, synthesis):
        """Step 4: Generate complete recipe using GPT-4o"""
        print(f"📝 Generating recipe for: {recipe['english_name']}")
        
        prompt = f"""Create a simple, authentic vegan recipe for "{recipe['english_name']}" ({recipe['hebrew_name']}) based on this research:

{synthesis}

Format as markdown with:
1. Brief cultural background (1-2 sentences)
2. Simple ingredient list (max 8-10 basic ingredients)
3. Step-by-step instructions (numbered, keep it simple)
4. Serving suggestions
5. Family notes from {recipe['source']} tradition
6. Preparation time and difficulty

Requirements:
- Keep it SIMPLE and traditional - don't add complex spices or invented ingredients
- Use only basic, authentic ingredients that would have been available historically
- Make it completely vegan with minimal substitutions
- Focus on traditional cooking methods, not modern techniques
- Don't force elaborate flavors - respect the original simplicity
- Include Hebrew names for key ingredients only

Recipe type: {recipe['type']}
Original description: {recipe.get('description', 'Traditional family recipe')}"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            recipe_markdown = response.choices[0].message.content
            
            # Save recipe
            recipe_file = f"data/recipes/markdown/{self.safe_filename(recipe['english_name'])}.md"
            with open(recipe_file, 'w', encoding='utf-8') as f:
                f.write(recipe_markdown)
            
            return recipe_markdown
            
        except Exception as e:
            print(f"❌ Error generating recipe: {e}")
            return f"Error: Unable to generate recipe - {e}"
    
    def translate_recipe(self, recipe, recipe_markdown, target_language):
        """Step 5: Translate recipe to target language"""
        print(f"🌐 Translating {recipe['english_name']} to {target_language}")
        
        language_instructions = {
            'hebrew': 'Hebrew (עברית) - Family heritage language',
            'spanish': 'Spanish (Español) - For wider accessibility',
            'arabic': 'Tunisian Arabic (تونسي) with Hebrew transliteration'
        }
        
        prompt = f"""Translate this recipe for "{recipe['english_name']}" into {language_instructions[target_language]}:

{recipe_markdown}

Requirements:
- Maintain cultural authenticity in food terminology
- Keep original dish names with pronunciation guides
- Preserve cooking technique descriptions
- Include cultural context appropriately
- For Tunisian Arabic: provide Hebrew transliteration in parentheses
- Keep ingredient measurements in both metric and traditional units"""
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            translated_recipe = response.choices[0].message.content
            
            # Save translation
            translation_file = f"data/recipes/translations/{self.safe_filename(recipe['english_name'])}_{target_language}.md"
            with open(translation_file, 'w', encoding='utf-8') as f:
                f.write(translated_recipe)
            
            return translated_recipe
            
        except Exception as e:
            print(f"❌ Error translating to {target_language}: {e}")
            return f"Error: Unable to translate to {target_language} - {e}"
    
    def generate_recipe_image(self, recipe):
        """Step 6: Generate recipe image using DALL-E"""
        print(f"🎨 Generating image for: {recipe['english_name']}")
        
        # Simple description of the dish for colorful line art
        dish_description = recipe.get('description', '')
        
        # Handle NaN/None values
        if not dish_description or str(dish_description).lower() in ['nan', 'none', '']:
            clean_description = f"Traditional North African {recipe['english_name']}"
        else:
            # Clean description - remove Hebrew/Arabic text and keep only the basic description
            import re
            # Remove Hebrew characters and complex formatting
            clean_description = re.sub(r'[\u0590-\u05FF]+', '', str(dish_description))
            clean_description = re.sub(r'[^\w\s,.-]', ' ', clean_description)
            clean_description = ' '.join(clean_description.split())  # Clean up whitespace
            
            # Fallback if description is too short or empty after cleaning
            if len(clean_description.strip()) < 10:
                clean_description = f"Traditional North African {recipe['english_name']}"
            
        prompt = f"""A simple, colorful line art illustration of a finished {recipe['english_name']} dish on a plate or serving bowl. Show the complete prepared food as it would appear when served. Clean artistic lines, vibrant colors, minimal background. Focus on the final dish appearance, not ingredients. Traditional North African cuisine presentation. Hand-drawn cookbook illustration style."""
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024", 
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download and save image
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                filename = f"data/images/generated/{self.safe_filename(recipe['english_name'])}.png"
                with open(filename, 'wb') as f:
                    f.write(img_response.content)
                
                print(f"✅ Image saved: {filename}")
                return filename
            else:
                print(f"❌ Failed to download image")
                return None
                
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            return None
    
    def safe_filename(self, name):
        """Convert recipe name to safe filename"""
        if not name:
            return "unknown_recipe"
        # Remove special characters and replace spaces with underscores
        safe = re.sub(r'[^\w\s-]', '', name)
        safe = re.sub(r'[-\s]+', '_', safe)
        safe = safe.strip('_')
        return safe.lower() if safe else "unknown_recipe"
    
    def process_single_recipe(self, recipe):
        """Process a single recipe through the complete pipeline"""
        print(f"\n🍽️  Processing: {recipe['english_name']} ({recipe['hebrew_name']})")
        print("=" * 60)
        
        try:
            # Step 1: Etymology research
            etymology_research = self.research_dish_etymology(recipe)
            time.sleep(2)  # Rate limiting
            
            # Step 2: Veganization research  
            vegan_research = self.research_veganization(recipe)
            time.sleep(2)
            
            # Step 3: Synthesis
            synthesis = self.synthesize_research(recipe, etymology_research, vegan_research)
            time.sleep(2)
            
            # Step 4: Recipe generation
            recipe_markdown = self.generate_recipe(recipe, synthesis)
            time.sleep(2)
            
            # Step 5: Translations
            translations = {}
            for lang in ['hebrew', 'spanish', 'arabic']:
                translations[lang] = self.translate_recipe(recipe, recipe_markdown, lang)
                time.sleep(2)
            
            # Step 6: Image generation
            image_path = self.generate_recipe_image(recipe)
            time.sleep(5)  # DALL-E takes longer
            
            # Log success
            self.progress_log.append({
                'recipe': recipe['english_name'],
                'status': 'SUCCESS',
                'timestamp': datetime.now().isoformat(),
                'image_path': image_path
            })
            
            print(f"✅ {recipe['english_name']} completed successfully!")
            
            return {
                'recipe': recipe,
                'etymology_research': etymology_research,
                'vegan_research': vegan_research,
                'synthesis': synthesis,
                'recipe_markdown': recipe_markdown,
                'translations': translations,
                'image_path': image_path
            }
            
        except Exception as e:
            print(f"❌ Error processing {recipe['english_name']}: {e}")
            self.progress_log.append({
                'recipe': recipe['english_name'],
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            })
            return None
    
    def run_pipeline(self, limit=None):
        """Run the complete pipeline for all recipes"""
        print("🚀 Starting Cookbook Pipeline")
        print("=" * 50)
        
        # Load recipes
        recipes = self.load_recipes_csv()
        
        if limit:
            recipes = recipes[:limit]
            print(f"🔬 Testing with {limit} recipes")
        
        # Process each recipe
        successful_recipes = []
        for i, recipe in enumerate(recipes, 1):
            print(f"\n📖 Recipe {i}/{len(recipes)}")
            
            result = self.process_single_recipe(recipe)
            if result:
                successful_recipes.append(result)
                
            # Save progress log after each recipe
            with open('data/pipeline_progress.json', 'w') as f:
                json.dump(self.progress_log, f, indent=2)
        
        print(f"\n🎉 Pipeline completed!")
        print(f"✅ Successful: {len(successful_recipes)}/{len(recipes)} recipes")
        
        return successful_recipes

def main():
    """Main execution function with command line support"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Vegan Djerban Family Cookbook AI Pipeline')
    parser.add_argument('--test', type=int, default=2, 
                       help='Run test mode with specified number of recipes (default: 2)')
    parser.add_argument('--full', action='store_true', 
                       help='Run full pipeline for all recipes')
    parser.add_argument('--recipe', type=str, 
                       help='Process specific recipe by name (partial match)')
    
    args = parser.parse_args()
    
    pipeline = CookbookPipeline()
    
    if args.full:
        print("🏃‍♂️ Running FULL pipeline for all recipes...")
        print("⚠️  This will take 30-60 minutes and use significant API credits!")
        results = pipeline.run_pipeline()
    elif args.recipe:
        print(f"🎯 Processing specific recipe: {args.recipe}")
        # Load recipes and filter by name
        recipes = pipeline.load_recipes_csv()
        matching_recipes = [r for r in recipes if args.recipe.lower() in r['english_name'].lower()]
        
        if not matching_recipes:
            print(f"❌ No recipes found matching '{args.recipe}'")
            return
            
        if len(matching_recipes) > 1:
            print(f"Found {len(matching_recipes)} matching recipes:")
            for r in matching_recipes:
                print(f"  • {r['english_name']} ({r['hebrew_name']})")
            print("Processing first match...")
        
        # Process the recipe directly
        result = pipeline.process_single_recipe(matching_recipes[0])
        results = [result] if result else []
    else:
        print(f"🧪 Running test pipeline with {args.test} recipes...")
        results = pipeline.run_pipeline(limit=args.test)
    
    if results and len(results) > 0:
        print("\n✅ Pipeline successful!")
        print("💡 Use master_pipeline.py --full for complete cookbook generation")
    else:
        print("❌ Pipeline failed. Check your API keys and try again.")

if __name__ == "__main__":
    main() 