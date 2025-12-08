#!/usr/bin/env python3
"""
Build comprehensive recipe JSON files for multilingual cookbook
Combines: recipe data + etymology research + history research
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List

class ComprehensiveRecipeBuilder:
    def __init__(self):
        self.recipes_dir = "data/safed_recipes_en"
        self.research_dir = "data/recipe_research"
        self.output_dir = "data/recipes_comprehensive"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def load_recipe(self, recipe_file: str) -> Dict:
        """Load base recipe JSON"""
        file_path = Path(self.recipes_dir) / recipe_file
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_research(self, recipe_name: str, research_type: str) -> str:
        """Load research markdown and extract content"""
        safe_name = recipe_name.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        research_file = Path(self.research_dir) / f"{safe_name}_{research_type}.md"
        
        if not research_file.exists():
            return ""
        
        with open(research_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content
    
    def extract_etymology_summary(self, research_content: str) -> Dict:
        """Extract etymology information from research"""
        etymology = {
            "name_meaning": "",
            "linguistic_roots": "",
            "historical_reference": "",
            "summary": ""
        }
        
        # Parse markdown sections
        lines = research_content.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            if '### Etymology' in line:
                current_section = 'etymology'
                section_content = []
            elif '### ' in line and current_section:
                # Found new section, save previous
                if section_content:
                    text = '\n'.join(section_content).strip()
                    if current_section == 'etymology':
                        etymology["summary"] = text[:500]  # First 500 chars as summary
                current_section = None
            elif current_section:
                section_content.append(line)
        
        return etymology
    
    def extract_history_summary(self, research_content: str) -> Dict:
        """Extract history information from research"""
        history = {
            "origins": "",
            "evolution": "",
            "cultural_significance": "",
            "regional_variations": "",
            "summary": ""
        }
        
        # Parse markdown sections
        lines = research_content.split('\n')
        sections = {
            'Historical Origins': 'origins',
            'Cultural Significance': 'cultural_significance',
            'Regional Variations': 'regional_variations'
        }
        
        current_section = None
        section_content = []
        
        for line in lines:
            for section_title, section_key in sections.items():
                if f'### {section_title}' in line:
                    if section_content and current_section:
                        text = '\n'.join(section_content).strip()
                        history[current_section] = text[:400]
                    current_section = section_key
                    section_content = []
                    break
            else:
                if current_section:
                    section_content.append(line)
        
        # Combine for summary
        all_text = '\n'.join([
            history.get('origins', ''),
            history.get('cultural_significance', '')
        ])
        history['summary'] = all_text[:400]
        
        return history
    
    def categorize_recipe(self, recipe: Dict) -> str:
        """Determine recipe category"""
        notes = recipe.get('notes', '').lower()
        name = recipe.get('name_english', '').lower()
        
        if 'soup' in notes or 'soup' in name or 'broth' in notes:
            return "Soup"
        elif 'bread' in notes or 'bread' in name or 'pastry' in notes or 'brik' in name:
            return "Bread & Pastry"
        elif 'dessert' in notes or 'sweet' in notes or 'donut' in name or 'cookie' in name:
            return "Desserts & Sweets"
        elif 'egg' in notes or 'omelette' in name or 'shakshuka' in name:
            return "Eggs & Breakfast"
        elif 'stew' in notes or 'tagine' in name or 'tafina' in name:
            return "Stews & Braises"
        else:
            return "Main Dishes"
    
    def build_comprehensive_recipe(self, recipe_file: str) -> Dict:
        """Build comprehensive recipe from base recipe + research"""
        
        recipe = self.load_recipe(recipe_file)
        if not recipe:
            return None
        
        recipe_name_en = recipe.get('name_english', 'Unknown')
        recipe_name_he = recipe.get('name_hebrew', '')
        
        # Load research
        etymology_research = self.load_research(recipe_name_en, 'history')
        history_research = self.load_research(recipe_name_en, 'history')
        
        # Extract summaries from research
        etymology_data = self.extract_etymology_summary(etymology_research)
        history_data = self.extract_history_summary(history_research)
        
        # Build comprehensive recipe
        comprehensive = {
            "id": recipe.get('id', recipe_name_en.lower().replace(' ', '_')),
            
            "names": {
                "english": recipe_name_en,
                "hebrew": recipe_name_he,
                "arabic": f"[TODO: Translate to Arabic]",
                "spanish": f"[TODO: Translate to Spanish]"
            },
            
            "metadata": {
                "category": self.categorize_recipe(recipe),
                "serves": "4-6 people",
                "prep_time_minutes": 20,
                "cook_time_minutes": 30,
                "difficulty": "Medium"
            },
            
            "ingredients": {
                "english": self._format_ingredients(recipe.get('ingredients', [])),
                "hebrew": [],
                "arabic": [],
                "spanish": []
            },
            
            "instructions": {
                "english": self._format_instructions(recipe.get('instructions', [])),
                "hebrew": [],
                "arabic": [],
                "spanish": []
            },
            
            "etymology": {
                "english": etymology_data,
                "hebrew": {},
                "arabic": {},
                "spanish": {}
            },
            
            "history": {
                "english": history_data,
                "hebrew": {},
                "arabic": {},
                "spanish": {}
            },
            
            "djerban_tradition": {
                "english": {
                    "role_in_family": recipe.get('notes', ''),
                    "occasions": "Traditional Tunisian-Djerban Jewish cuisine",
                    "preparation_rituals": "[To be expanded from research]",
                    "cultural_meaning": "[To be expanded from research]",
                    "summary": recipe.get('notes', '')[:300]
                },
                "hebrew": {},
                "arabic": {},
                "spanish": {}
            },
            
            "cooking_notes": {
                "english": {
                    "tips": [
                        "Traditional preparation methods recommended",
                        "Adjust spicing to taste preference",
                        "Source: Safed family tradition"
                    ],
                    "variations": ["[To be documented]"],
                    "substitutions": ["[To be documented]"]
                },
                "hebrew": {},
                "arabic": {},
                "spanish": {}
            },
            
            "research_references": {
                "etymology_md": f"{recipe_name_en.lower().replace(' ', '_')}_history.md",
                "history_md": f"{recipe_name_en.lower().replace(' ', '_')}_history.md",
                "sources": ["Safed family oral tradition", "Perplexity Pro Search research"]
            }
        }
        
        return comprehensive
    
    def _format_ingredients(self, ingredients: List[str]) -> List[Dict]:
        """Format ingredients into structured format"""
        formatted = []
        
        for ingredient in ingredients:
            if not ingredient.strip() or ingredient.endswith(':'):
                continue
            
            # Try to parse amount and unit
            parts = ingredient.split()
            name = ingredient
            amount = ""
            unit = ""
            
            # Simple parsing
            if parts and parts[0].replace('.', '').replace('/', '').isdigit():
                amount = parts[0]
                if len(parts) > 1 and parts[1] in ['cup', 'cups', 'tbsp', 'tsp', 'tablespoon', 'teaspoon', 'oz', 'g', 'kg', 'liter', 'liters', 'ml']:
                    unit = parts[1]
                    name = ' '.join(parts[2:]) if len(parts) > 2 else ingredient
                else:
                    name = ' '.join(parts[1:]) if len(parts) > 1 else ingredient
            
            formatted.append({
                "name": name,
                "amount": amount,
                "unit": unit
            })
        
        return formatted
    
    def _format_instructions(self, instructions: List[str]) -> List[Dict]:
        """Format instructions into structured format"""
        formatted = []
        step_num = 1
        
        for instruction in instructions:
            if not instruction.strip():
                continue
            
            # Remove numbering if present
            text = instruction.lstrip('0123456789.\\-) ')
            
            formatted.append({
                "step": step_num,
                "text": text
            })
            step_num += 1
        
        return formatted
    
    def process_all_recipes(self):
        """Process all recipes and save comprehensive versions"""
        recipe_files = sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
        
        print(f"\nBuilding comprehensive recipes for {len(recipe_files)} recipes...")
        print("=" * 70)
        
        successful = 0
        
        for i, recipe_file in enumerate(recipe_files, 1):
            comprehensive = self.build_comprehensive_recipe(recipe_file)
            
            if comprehensive:
                # Save to output directory
                output_file = Path(self.output_dir) / recipe_file
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(comprehensive, f, indent=2, ensure_ascii=False)
                
                print(f"[{i:2d}/{len(recipe_files)}] ✓ {comprehensive['names']['english']}")
                successful += 1
            else:
                print(f"[{i:2d}/{len(recipe_files)}] ✗ Failed to build")
        
        print("=" * 70)
        print(f"\n✓ Successfully built {successful}/{len(recipe_files)} comprehensive recipes")
        print(f"📁 Output directory: {self.output_dir}/\n")
        
        return successful


def main():
    try:
        builder = ComprehensiveRecipeBuilder()
        builder.process_all_recipes()
        print("✓ Comprehensive recipe building complete!")
        print("\nNext steps:")
        print("1. Review sample recipes in data/recipes_comprehensive/")
        print("2. Validate structure and content")
        print("3. Build translation pipeline for Hebrew, Arabic, Spanish")
        print("4. Design Typst layout with floating text boxes\n")
        return 0
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

