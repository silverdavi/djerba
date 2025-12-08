#!/usr/bin/env python3
"""
Recipe Research Interface using Perplexity Pro Search
Conduct in-depth research on Tunisian-Djerban recipes with multi-step reasoning,
real-time thought streaming, and adaptive research strategies.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
import requests
from typing import Optional, Dict, Any

load_dotenv()

class RecipeResearchInterface:
    def __init__(self):
        """Initialize the Perplexity Pro Search interface"""
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.api_url = "https://api.perplexity.ai/chat/completions"
        
        if not self.api_key:
            raise ValueError("PERPLEXITY_API_KEY not found in environment variables")
        
        self.recipes_dir = "data/safed_recipes_en"
        self.research_output_dir = "data/recipe_research"
        Path(self.research_output_dir).mkdir(parents=True, exist_ok=True)
        
        print("✓ Perplexity Pro Search Interface Initialized")
        print(f"  API Key: {self.api_key[:20]}...")
        print(f"  Output Directory: {self.research_output_dir}")
    
    def load_recipe(self, recipe_file: str) -> Optional[Dict[str, Any]]:
        """Load a recipe from JSON file"""
        file_path = Path(self.recipes_dir) / recipe_file
        
        if not file_path.exists():
            print(f"❌ Recipe file not found: {recipe_file}")
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_recipes(self) -> list:
        """List all available recipes"""
        recipe_files = sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
        return recipe_files
    
    def research_recipe_history(self, recipe_name: str, recipe_data: Dict) -> str:
        """Research the historical and cultural background of a recipe"""
        
        prompt = f"""Conduct an in-depth research on the recipe "{recipe_data['name_english']}" ({recipe_data['name_hebrew']}).

Please investigate:

1. **Historical Origins**: 
   - When and where did this dish originate?
   - How has it evolved over centuries?
   - Any documented historical references?

2. **Cultural Significance**:
   - What is its importance in Tunisian-Djerban Jewish cuisine?
   - Is it tied to specific holidays or occasions?
   - Any family or community traditions around it?

3. **Regional Variations**:
   - How do different regions prepare this dish?
   - Differences between Tunisian, Moroccan, and Libyan versions?
   - Modern adaptations vs traditional methods?

4. **Etymology**:
   - What does the name mean?
   - Any linguistic origins or connections?

5. **Related Dishes**:
   - Similar dishes in other cuisines?
   - Dishes it might be served alongside?

Provide citations and sources for your findings."""

        return self._send_pro_search_query(prompt, recipe_name, "history")
    
    def research_ingredient_substitutions(self, recipe_name: str, recipe_data: Dict) -> str:
        """Research vegan and ingredient substitutions"""
        
        ingredients_list = "\n".join(recipe_data.get('ingredients', []))
        
        prompt = f"""Research ingredient substitutions and variations for the recipe "{recipe_data['name_english']}".

**Current Ingredients:**
{ingredients_list}

Please investigate:

1. **Vegan Substitutions**:
   - What are the best plant-based substitutes for animal products in this dish?
   - How do substitutions affect taste and texture?
   - Traditional vegan versions that exist?

2. **Allergy-Friendly Alternatives**:
   - Gluten-free options?
   - Dairy-free alternatives?
   - Nut-free substitutions?

3. **Modern Ingredient Adaptations**:
   - Contemporary ingredients that could enhance the dish?
   - How to adapt for modern kitchens and appliances?
   - Ingredient sourcing in different countries?

4. **Nutritional Information**:
   - Estimated nutritional values?
   - Health benefits of key ingredients?
   - Dietary considerations?

5. **Quality and Sourcing**:
   - Where to source authentic ingredients?
   - Quality indicators for key components?
   - Seasonal availability?

Provide detailed recommendations with reasoning."""

        return self._send_pro_search_query(prompt, recipe_name, "substitutions")
    
    def research_cooking_techniques(self, recipe_name: str, recipe_data: Dict) -> str:
        """Research traditional and modern cooking techniques"""
        
        instructions_list = "\n".join(recipe_data.get('instructions', []))
        
        prompt = f"""Research cooking techniques and methods for "{recipe_data['name_english']}".

**Recipe Instructions:**
{instructions_list}

Please investigate:

1. **Traditional Techniques**:
   - What cooking methods were traditionally used?
   - How does the method affect flavor and texture?
   - Historical equipment and tools used?

2. **Modern Adaptations**:
   - How can this be made with modern appliances?
   - Oven vs stovetop vs slow cooker approaches?
   - Time-saving methods while maintaining authenticity?

3. **Professional Cooking Tips**:
   - Chef recommendations for perfecting the dish?
   - Common mistakes and how to avoid them?
   - Temperature and timing optimization?

4. **Science Behind the Cooking**:
   - Chemical reactions that occur during cooking?
   - How ingredients interact and transform?
   - Why specific techniques produce the best results?

5. **Texture and Flavor Development**:
   - How to achieve the perfect consistency?
   - Flavor layering and development?
   - Tips for enhancing taste complexity?

Provide technical insights with practical applications."""

        return self._send_pro_search_query(prompt, recipe_name, "techniques")
    
    def research_pairing_suggestions(self, recipe_name: str, recipe_data: Dict) -> str:
        """Research wine, beverage, and food pairing suggestions"""
        
        prompt = f"""Research pairing suggestions for "{recipe_data['name_english']}".

**Dish Type:** {recipe_data.get('notes', 'Traditional Tunisian-Djerban dish')}

Please investigate:

1. **Wine Pairings**:
   - Best red wines to pair with this dish?
   - White wine options?
   - Mediterranean or North African wines?
   - Wine tasting notes that complement the flavors?

2. **Beverage Pairings**:
   - Traditional beverages from the region?
   - Tea or coffee pairings?
   - Alcoholic and non-alcoholic options?
   - Cultural serving traditions?

3. **Food Pairings**:
   - What dishes does this pair well with?
   - Traditional meal structures in Tunisian cuisine?
   - Appetizers, sides, and desserts?
   - Full meal planning around this dish?

4. **Serving Suggestions**:
   - Traditional serving vessels or presentations?
   - Temperature serving recommendations?
   - Garnishes and final touches?

5. **Complementary Flavors**:
   - Flavor profiles that work well?
   - Spices that enhance the dining experience?
   - Textural contrasts?

Provide detailed pairing recommendations with reasoning."""

        return self._send_pro_search_query(prompt, recipe_name, "pairings")
    
    def research_nutritional_analysis(self, recipe_name: str, recipe_data: Dict) -> str:
        """Research nutritional and health aspects"""
        
        ingredients_list = "\n".join(recipe_data.get('ingredients', []))
        
        prompt = f"""Conduct a nutritional analysis of the recipe "{recipe_data['name_english']}".

**Ingredients:**
{ingredients_list}

Please investigate:

1. **Nutritional Profile**:
   - Estimated macronutrients (proteins, fats, carbs)?
   - Micronutrients and vitamins present?
   - Caloric content per serving?
   - Glycemic index considerations?

2. **Health Benefits**:
   - Nutritional benefits of key ingredients?
   - Traditional medicinal uses of components?
   - Health claims supported by research?

3. **Dietary Considerations**:
   - Suitable for specific diets (Mediterranean, etc.)?
   - Allergen information?
   - Sodium and sugar content?
   - Cholesterol considerations?

4. **Ingredient Nutritional Value**:
   - Most nutrient-dense ingredients?
   - Any ingredients with particular health benefits?
   - Antioxidant and anti-inflammatory properties?

5. **Optimization for Health**:
   - How to make this dish healthier without losing authenticity?
   - Ingredient modifications for specific dietary needs?
   - Cooking methods that preserve nutrition?

Provide scientifically-backed nutritional insights."""

        return self._send_pro_search_query(prompt, recipe_name, "nutrition")
    
    def _send_pro_search_query(self, prompt: str, recipe_name: str, research_type: str) -> str:
        """Send a Pro Search query to Perplexity API with streaming"""
        
        print(f"\n🔍 Researching: {research_type.upper()} for {recipe_name}")
        print("-" * 60)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "sonar-pro",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": True,
            "web_search_options": {
                "search_type": "pro"
            }
        }
        
        full_response = ""
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            
            if response.status_code != 200:
                print(f"❌ API Error: {response.status_code}")
                print(response.text)
                return f"Error: {response.status_code}"
            
            print("\n📚 Research Results:\n")
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data_str = line[6:]
                    
                    if data_str == '[DONE]':
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        if 'choices' in data and data['choices']:
                            delta = data['choices'][0].get('delta', {})
                            content = delta.get('content', '')
                            
                            if content:
                                print(content, end='', flush=True)
                                full_response += content
                    
                    except json.JSONDecodeError:
                        continue
            
            print("\n" + "-" * 60)
            
            # Save research to file
            self._save_research(recipe_name, research_type, full_response)
            
            return full_response
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return f"Error: {str(e)}"
    
    def _save_research(self, recipe_name: str, research_type: str, content: str):
        """Save research results to a file"""
        
        safe_name = recipe_name.lower().replace(' ', '_').replace('(', '').replace(')', '')
        filename = f"{safe_name}_{research_type}.md"
        file_path = Path(self.research_output_dir) / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"# {recipe_name.upper()} - {research_type.upper()}\n\n")
            f.write(content)
        
        print(f"\n✓ Research saved to: {file_path}")
    
    def interactive_menu(self):
        """Interactive menu for recipe research"""
        
        while True:
            print("\n" + "=" * 60)
            print("RECIPE RESEARCH INTERFACE - Perplexity Pro Search")
            print("=" * 60)
            
            recipes = self.list_recipes()
            
            print(f"\nAvailable Recipes ({len(recipes)}):\n")
            for i, recipe_file in enumerate(recipes, 1):
                recipe = self.load_recipe(recipe_file)
                if recipe:
                    print(f"  {i:2d}. {recipe.get('name_english', 'Unknown')}")
            
            print("\nOptions:")
            print("  [1-N] Research a specific recipe")
            print("  [q]   Quit")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == 'q':
                print("\n👋 Goodbye!")
                break
            
            try:
                recipe_idx = int(choice) - 1
                if 0 <= recipe_idx < len(recipes):
                    self._research_recipe_interactive(recipes[recipe_idx])
                else:
                    print("❌ Invalid selection")
            except ValueError:
                print("❌ Invalid input")
    
    def _research_recipe_interactive(self, recipe_file: str):
        """Interactive research options for a specific recipe"""
        
        recipe = self.load_recipe(recipe_file)
        if not recipe:
            return
        
        recipe_name = recipe.get('name_english', 'Unknown')
        
        while True:
            print("\n" + "-" * 60)
            print(f"RESEARCH OPTIONS FOR: {recipe_name}")
            print("-" * 60)
            print("\n  [1] Historical & Cultural Background")
            print("  [2] Ingredient Substitutions & Variations")
            print("  [3] Cooking Techniques & Methods")
            print("  [4] Food & Wine Pairings")
            print("  [5] Nutritional Analysis")
            print("  [6] Research All")
            print("  [b] Back to Menu")
            
            choice = input("\nEnter your choice: ").strip().lower()
            
            if choice == '1':
                self.research_recipe_history(recipe_file, recipe)
            elif choice == '2':
                self.research_ingredient_substitutions(recipe_file, recipe)
            elif choice == '3':
                self.research_cooking_techniques(recipe_file, recipe)
            elif choice == '4':
                self.research_pairing_suggestions(recipe_file, recipe)
            elif choice == '5':
                self.research_nutritional_analysis(recipe_file, recipe)
            elif choice == '6':
                print("\n🔬 Running comprehensive research on all aspects...")
                self.research_recipe_history(recipe_file, recipe)
                input("\n[Press Enter to continue...]")
                self.research_ingredient_substitutions(recipe_file, recipe)
                input("\n[Press Enter to continue...]")
                self.research_cooking_techniques(recipe_file, recipe)
                input("\n[Press Enter to continue...]")
                self.research_pairing_suggestions(recipe_file, recipe)
                input("\n[Press Enter to continue...]")
                self.research_nutritional_analysis(recipe_file, recipe)
            elif choice == 'b':
                break
            else:
                print("❌ Invalid choice")


def main():
    """Main entry point"""
    
    try:
        interface = RecipeResearchInterface()
        interface.interactive_menu()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())

