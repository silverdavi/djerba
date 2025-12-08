#!/usr/bin/env python3
"""
Generate Typst recipe content from JSON recipe files
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Any

class TypstRecipeGenerator:
    def __init__(self):
        self.recipes_dir = "data/safed_recipes_en"
        self.output_file = "typst/recipes-content.typ"
        self.research_dir = "data/recipe_research"
    
    def load_recipes(self) -> List[Dict]:
        """Load all recipe JSON files"""
        recipes = []
        recipe_files = sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
        
        for recipe_file in recipe_files:
            with open(os.path.join(self.recipes_dir, recipe_file), 'r', encoding='utf-8') as f:
                recipe = json.load(f)
                recipes.append(recipe)
        
        return recipes
    
    def escape_typst(self, text: str) -> str:
        """Escape special characters for Typst"""
        # Escape special characters for Typst strings
        text = text.replace("\\", "\\\\")  # Escape backslashes first
        text = text.replace('"', '\\"')     # Escape double quotes
        text = text.replace("#", "\\#")     # Escape hash marks
        text = text.replace("°", "")        # Remove degree symbols
        return text
    
    def format_ingredients(self, ingredients: List[str]) -> str:
        """Format ingredients for Typst"""
        formatted = []
        for ingredient in ingredients:
            # Skip empty or section headers
            if not ingredient.strip() or ingredient.endswith(":"):
                continue
            escaped = self.escape_typst(ingredient)
            formatted.append(f'    ingredient("{escaped}"),')
        return "\n".join(formatted)
    
    def format_instructions(self, instructions: List[str]) -> str:
        """Format instructions for Typst"""
        formatted = []
        for instruction in instructions:
            if not instruction.strip():
                continue
            # Remove numbering if present
            step = instruction.lstrip('0123456789.\\-) ')
            escaped = self.escape_typst(step)
            formatted.append(f'    step("{escaped}"),')
        return "\n".join(formatted)
    
    def get_category(self, recipe: Dict) -> str:
        """Determine recipe category from notes or name"""
        notes = recipe.get('notes', '').lower()
        name = recipe.get('name_english', '').lower()
        
        if 'soup' in notes or 'soup' in name or 'broth' in notes:
            return "Soup"
        elif 'bread' in notes or 'bread' in name or 'pastry' in notes:
            return "Bread & Pastry"
        elif 'dessert' in notes or 'sweet' in notes or 'cake' in name or 'cookie' in name:
            return "Desserts"
        elif 'egg' in notes or 'omelette' in name or 'shakshuka' in name:
            return "Eggs & Breakfast"
        elif 'stew' in notes or 'stew' in name or 'tagine' in name:
            return "Stews & Braises"
        else:
            return "Main Course"
    
    def load_research(self, recipe: Dict) -> str:
        """Load historical research for recipe"""
        safe_name = recipe.get('name_english', '').lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        research_file = os.path.join(self.research_dir, f"{safe_name}_history.md")
        
        if os.path.exists(research_file):
            with open(research_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract first 2-3 lines of significant content
                lines = content.split('\n')
                for line in lines:
                    if line.startswith('### ') or (line.strip() and not line.startswith('#')):
                        return line.strip()[:100] + "..."
        
        return ""
    
    def generate_typst_content(self) -> str:
        """Generate complete Typst recipe content"""
        recipes = self.load_recipes()
        
        content = [
            '// Recipe Content - Auto-generated from JSON\n',
            '#import "template.typ": *\n',
            '\n',
        ]
        
        # Group recipes by category
        categories = {}
        for recipe in recipes:
            category = self.get_category(recipe)
            if category not in categories:
                categories[category] = []
            categories[category].append(recipe)
        
        # Generate content for each category
        for category in sorted(categories.keys()):
            content.append(f"= {category}\n\n")
            
            for recipe in categories[category]:
                name = self.escape_typst(recipe.get('name_english', 'Unknown'))
                name_hebrew = recipe.get('name_hebrew', '')
                
                ingredients = recipe.get('ingredients', [])
                instructions = recipe.get('instructions', [])
                notes = self.escape_typst(recipe.get('notes', 'Traditional recipe from Djerban Jewish cuisine.'))
                
                # Format ingredients
                ingredients_formatted = self.format_ingredients(ingredients)
                
                # Format instructions
                instructions_formatted = self.format_instructions(instructions)
                
                # Build recipe block
                recipe_block = f'''#recipe(
  name: "{name}",
  name-hebrew: "{name_hebrew}",
  serves: "4-6",
  prep-time: "20 min",
  cook-time: "30 min",
  ingredients: (
{ingredients_formatted}
  ),
  instructions: (
{instructions_formatted}
  ),
  notes: "{notes}",
  category: "{category}"
)

'''
                content.append(recipe_block)
                
                # Add cultural note if available
                research = self.load_research(recipe)
                if research:
                    content.append(f'#cultural-note(\n')
                    content.append(f'  "Historical Background",\n')
                    content.append(f'  "{research}"\n')
                    content.append(f')\n\n')
                
                content.append("\n")
        
        return "".join(content)
    
    def write_output(self):
        """Write generated content to file"""
        content = self.generate_typst_content()
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ Generated Typst recipe content: {self.output_file}")
        print(f"  Total recipes: {len(self.load_recipes())}")


def main():
    try:
        generator = TypstRecipeGenerator()
        generator.write_output()
        print("\n✓ Typst cookbook content generated successfully!")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

