#!/usr/bin/env python3
"""
Extract individual recipes from raw_raw.txt file where recipes are separated by --- or ----

Usage:
    python extract_recipes_from_raw.py raw/raw_raw.txt --output raw/
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class RecipeExtractor:
    """Extract recipes from raw text file"""
    
    def __init__(self, input_file: str, output_dir: str = "raw"):
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.recipes = []
        self.log_entries = []
    
    def log(self, message: str):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_entries.append(full_message)
        print(full_message)
    
    def extract_all(self) -> int:
        """Extract all recipes from the raw file"""
        if not self.input_file.exists():
            self.log(f"❌ Input file not found: {self.input_file}")
            return 0
        
        self.log(f"📖 Reading file: {self.input_file}")
        
        with open(self.input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by recipe separators (--- or ----)
        # Be more specific with the pattern to catch separator lines
        recipe_blocks = re.split(r'\n(-{3,})\n', content)
        
        self.log(f"  Found {len(recipe_blocks)} blocks")
        
        # Process blocks (odd indices are separators, even are content)
        recipe_count = 0
        for i, block in enumerate(recipe_blocks):
            # Skip separator lines
            if block.strip() in ['---', '----', '-' * 3, '-' * 4]:
                continue
            
            block = block.strip()
            if not block:
                continue
            
            # Check if this block contains recipe content (has INGREDIENTS)
            if 'INGREDIENTS' in block or 'METHOD' in block:
                recipe = self._parse_recipe(block)
                if recipe and recipe.get('name'):
                    self.recipes.append(recipe)
                    recipe_count += 1
                    self.log(f"  ✓ Extracted: {recipe.get('name', 'Unknown')}")
        
        self.log(f"📚 Total recipes extracted: {recipe_count}")
        return recipe_count
    
    def _parse_recipe(self, block: str) -> Optional[Dict]:
        """Parse a recipe block from raw text"""
        lines = block.split('\n')
        
        recipe = {
            'name': '',
            'ingredients': [],
            'instructions': [],
            'serves': '',
            'source': 'recime_raw'
        }
        
        current_section = None
        name_found = False
        recipe_image_found = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            # Track when we find "Recipe Image" - the next non-empty line is likely the recipe name
            if line_stripped == 'Recipe Image':
                recipe_image_found = True
                continue
            
            # Skip UI elements and empty lines
            if not line_stripped or line_stripped in ['Recime Logo', 'Open menu', 'Add Recipe', 
                                                       'Cookbooks', 'Meal Plan', 'Groceries', 
                                                       'Chrome extension', 'NEW!', 'Log in to mobile app',
                                                       'Settings', 'Recipe Image', 'convertConvert',
                                                       'convert', 'Open website', 'Your rating', 'Update',
                                                       'From:', 'Cookbooks:',
                                                       'Prep:', 'Cook:', '4/8']:
                continue
            
            # Get recipe name (right after "Recipe Image")
            if not name_found and not current_section:
                # If we found Recipe Image marker, use the next non-empty line as name
                if recipe_image_found and line_stripped and 'serves' not in line_stripped.lower():
                    recipe['name'] = line_stripped
                    name_found = True
                    recipe_image_found = False
                    continue
                
                # Skip serving info
                if 'serves' in line_stripped.lower():
                    recipe['serves'] = line_stripped
                    continue
            
            # Detect sections
            if line_stripped == 'INGREDIENTS':
                current_section = 'ingredients'
                continue
            elif line_stripped == 'METHOD':
                current_section = 'instructions'
                continue
            
            # Process serving info
            if 'serves' in line_stripped.lower() and current_section is None:
                recipe['serves'] = line_stripped
                continue
            
            # Parse ingredients
            if current_section == 'ingredients':
                # Skip serving/convert lines
                if any(skip in line_stripped.lower() for skip in ['serves', 'convert', 'prep:', 'cook:']):
                    continue
                
                # Add ingredient lines
                if line_stripped and not line_stripped.startswith('http'):
                    recipe['ingredients'].append(line_stripped)
            
            # Parse instructions
            elif current_section == 'instructions':
                # Skip "No instructions added yet"
                if 'No instructions added yet' in line_stripped:
                    continue
                
                # Check if line is a numbered instruction
                if line_stripped:
                    # Try to extract instruction number and text
                    match = re.match(r'^(\d+)\s+(.+)$', line_stripped)
                    if match:
                        instruction = match.group(2).strip()
                        if instruction:
                            recipe['instructions'].append(instruction)
                    elif not line_stripped[0].isdigit():  # Skip pure numbers
                        recipe['instructions'].append(line_stripped)
        
        # Clean up empty items
        recipe['ingredients'] = [ing for ing in recipe['ingredients'] if ing.strip()]
        recipe['instructions'] = [ins for ins in recipe['instructions'] if ins.strip()]
        
        return recipe if recipe['name'] else None
    
    def save_recipes(self) -> int:
        """Save extracted recipes to JSON files"""
        if not self.recipes:
            self.log("⚠️  No recipes to save")
            return 0
        
        count = 0
        for recipe in self.recipes:
            try:
                # Use recipe name as filename, sanitize it
                filename = recipe['name'].lower().strip()
                filename = ''.join(c if c.isalnum() or c in '_- ' else '_' for c in filename)
                filename = '_'.join(filename.split())[:100]  # Limit filename length
                
                output_file = self.output_dir / f"{filename}.json"
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, ensure_ascii=False, indent=2)
                
                count += 1
                # self.log(f"  💾 Saved: {output_file.name}")
                
            except Exception as e:
                self.log(f"  ❌ Error saving recipe: {e}")
        
        self.log(f"💾 Saved {count} recipes to {self.output_dir}")
        return count
    
    def write_log(self):
        """Write extraction log"""
        log_file = self.output_dir.parent / "EXTRACTION_LOG.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# Recipe Extraction Log\n\n")
            f.write(f"**Extraction Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Source File:** {self.input_file.name}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Total recipes extracted:** {len(self.recipes)}\n\n")
            
            if self.recipes:
                f.write("## Recipes Extracted\n\n")
                for recipe in sorted(self.recipes, key=lambda r: r['name']):
                    f.write(f"- **{recipe['name']}** ({len(recipe['ingredients'])} ingredients, {len(recipe['instructions'])} steps)\n")
                f.write("\n")
            
            f.write("## Log Entries\n\n")
            for entry in self.log_entries:
                f.write(f"{entry}\n")
        
        print(f"✅ Log written to {log_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Extract individual recipes from raw text file"
    )
    parser.add_argument(
        "input_file",
        help="Input file with recipes (e.g., raw/raw_raw.txt)"
    )
    parser.add_argument(
        "--output",
        default="raw",
        help="Output directory for extracted recipes (default: raw)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("Recipe Extractor from Raw Text")
    print("=" * 70)
    print()
    
    extractor = RecipeExtractor(args.input_file, args.output)
    
    # Extract recipes
    extracted_count = extractor.extract_all()
    
    print()
    
    # Save recipes
    if extracted_count > 0:
        saved_count = extractor.save_recipes()
        extractor.log(f"✅ Extraction complete: {saved_count} recipes saved")
    else:
        extractor.log("⚠️  No recipes extracted")
    
    # Write log
    print()
    extractor.write_log()
    
    print()
    print("=" * 70)
    print(f"✅ Total recipes extracted and saved: {len(extractor.recipes)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
