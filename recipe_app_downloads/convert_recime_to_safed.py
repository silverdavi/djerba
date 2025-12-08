#!/usr/bin/env python3
"""
Convert ReciMe recipe format to Safed recipe format for pipeline processing

This adapter converts recipes from:
  ReciMe format: {name, ingredients[], instructions[], serves, source}
  
To:
  Safed format: {name_hebrew, ingredients[], instructions, metadata, id}

Which is what the transform_recipes_gemini.py pipeline expects.

Usage:
    python convert_recime_to_safed.py raw/ --output converted/
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import re

class ReciMeToSafedConverter:
    """Convert ReciMe recipes to Safed pipeline format"""
    
    def __init__(self, input_dir: str, output_dir: str = "converted"):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.recipes_converted = 0
        self.recipes_failed = 0
        self.log_entries = []
    
    def log(self, message: str):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_entries.append(full_message)
        print(full_message)
    
    def convert_all(self) -> int:
        """Convert all recipes from input directory"""
        if not self.input_dir.exists():
            self.log(f"❌ Input directory not found: {self.input_dir}")
            return 0
        
        self.log(f"📂 Reading recipes from: {self.input_dir}")
        
        json_files = list(self.input_dir.glob("*.json"))
        self.log(f"  Found {len(json_files)} recipe files")
        
        for json_file in sorted(json_files):
            try:
                self._convert_recipe(json_file)
            except Exception as e:
                self.log(f"  ❌ Error processing {json_file.name}: {e}")
                self.recipes_failed += 1
        
        return self.recipes_converted
    
    def _convert_recipe(self, json_file: Path):
        """Convert a single recipe file"""
        with open(json_file, 'r', encoding='utf-8') as f:
            recime_recipe = json.load(f)
        
        # Convert format
        safed_recipe = self._recime_to_safed(recime_recipe)
        
        # Generate output filename (use recipe name as basis)
        output_name = self._generate_filename(safed_recipe['name_hebrew'])
        output_file = self.output_dir / f"{output_name}.json"
        
        # Save converted recipe
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(safed_recipe, f, ensure_ascii=False, indent=2)
        
        self.recipes_converted += 1
        self.log(f"  ✓ Converted: {safed_recipe['name_hebrew']} → {output_file.name}")
    
    def _recime_to_safed(self, recime_recipe: Dict) -> Dict:
        """Convert ReciMe format to Safed format"""
        
        # Extract name - use as-is or sanitize if needed
        name = recime_recipe.get('name', 'Unknown Recipe').strip()
        
        # Build ingredients list
        ingredients = recime_recipe.get('ingredients', [])
        if isinstance(ingredients, str):
            ingredients = [ingredients]
        ingredients = [ing.strip() for ing in ingredients if ing.strip()]
        
        # Build instructions
        instructions = recime_recipe.get('instructions', [])
        if isinstance(instructions, str):
            instructions = [instructions]
        # Clean up instruction steps (remove pure numbers)
        instructions = [
            ins.strip() 
            for ins in instructions 
            if ins.strip() and not ins.strip().isdigit()
        ]
        
        # Generate ID
        recipe_id = name.lower().strip()
        recipe_id = ''.join(c if c.isalnum() or c in '_- ' else '_' for c in recipe_id)
        recipe_id = '_'.join(recipe_id.split())
        
        # Build metadata
        metadata = {
            'source': 'recime_app',
            'source_file': recime_recipe.get('source', 'unknown'),
            'original_serves': recime_recipe.get('serves', 'Unknown'),
            'imported_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        # Create safed format recipe
        safed_recipe = {
            'name_hebrew': name,
            'ingredients': ingredients,
            'instructions': instructions,
            'metadata': metadata,
            'id': recipe_id
        }
        
        return safed_recipe
    
    def _generate_filename(self, recipe_name: str) -> str:
        """Generate a valid filename from recipe name"""
        filename = recipe_name.lower().strip()
        filename = ''.join(c if c.isalnum() or c in '_- ' else '_' for c in filename)
        filename = '_'.join(filename.split())[:80]  # Limit length
        return filename
    
    def write_log(self):
        """Write conversion log"""
        log_file = self.output_dir.parent / "CONVERSION_LOG.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# ReciMe to Safed Format Conversion Log\n\n")
            f.write(f"**Conversion Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Recipes converted:** {self.recipes_converted}\n")
            f.write(f"- **Conversion failed:** {self.recipes_failed}\n")
            f.write(f"- **Output directory:** {self.output_dir}\n\n")
            
            f.write("## Next Steps\n\n")
            f.write("1. **Copy to safed_recipes for processing:**\n")
            f.write(f"   ```bash\n")
            f.write(f"   cp {self.output_dir}/*.json data/safed_recipes/\n")
            f.write(f"   ```\n\n")
            
            f.write("2. **Run full pipeline (veganize + translate + images):**\n")
            f.write(f"   ```bash\n")
            f.write(f"   python transform_recipes_gemini.py --start 0 --with-images\n")
            f.write(f"   ```\n\n")
            
            f.write("3. **Or process specific recipes:**\n")
            f.write(f"   ```bash\n")
            f.write(f"   python transform_recipes_gemini.py --single \"01_recipe_name.json\" --with-images\n")
            f.write(f"   ```\n\n")
            
            f.write("## Output Format\n\n")
            f.write("Each converted recipe has:\n")
            f.write("- `name_hebrew`: Recipe name\n")
            f.write("- `ingredients[]`: List of ingredients\n")
            f.write("- `instructions[]`: List of instruction steps\n")
            f.write("- `metadata`: Source information and import date\n")
            f.write("- `id`: Machine-readable identifier\n\n")
            
            f.write("## Log Entries\n\n")
            for entry in self.log_entries:
                f.write(f"{entry}\n")
        
        print(f"✅ Conversion log written to {log_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Convert ReciMe recipes to Safed pipeline format"
    )
    parser.add_argument(
        "input_dir",
        help="Input directory with ReciMe JSON recipes (e.g., raw/)"
    )
    parser.add_argument(
        "--output",
        default="converted",
        help="Output directory for converted recipes (default: converted)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("ReciMe → Safed Format Converter")
    print("=" * 70)
    print()
    
    converter = ReciMeToSafedConverter(args.input_dir, args.output)
    
    # Convert all recipes
    converted_count = converter.convert_all()
    
    print()
    print("=" * 70)
    print(f"✅ Conversion complete: {converted_count} recipes converted")
    print("=" * 70)
    
    # Write log
    print()
    converter.write_log()
    
    print()
    print(f"📂 Converted recipes are in: {converter.output_dir}")


if __name__ == "__main__":
    main()
