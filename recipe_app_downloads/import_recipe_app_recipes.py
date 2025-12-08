#!/usr/bin/env python3
"""
Import recipes from recipe.app exports (JSON/CSV)

Usage:
    python import_recipe_app_recipes.py raw/
    python import_recipe_app_recipes.py raw/ --output processed/

Features:
- Accepts JSON or CSV format
- Validates recipe structure
- Deduplicates recipes
- Converts to standard format
- Logs import results
"""

import os
import sys
import json
import csv
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class RecipeAppImporter:
    """Import recipes from recipe.app exports"""
    
    def __init__(self, input_dir: str, output_dir: str = None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir.parent / "processed"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.recipes = {}  # id -> recipe
        self.duplicates = []
        self.errors = []
        self.log_entries = []
    
    def import_all(self) -> int:
        """Import all recipe files from input directory"""
        if not self.input_dir.exists():
            self.log(f"❌ Input directory not found: {self.input_dir}")
            return 0
        
        count = 0
        for file_path in self.input_dir.iterdir():
            if file_path.suffix == ".json":
                count += self._import_json(file_path)
            elif file_path.suffix == ".csv":
                count += self._import_csv(file_path)
        
        return count
    
    def _import_json(self, file_path: Path) -> int:
        """Import recipes from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both single recipe and list of recipes
            recipes = data if isinstance(data, list) else [data]
            
            count = 0
            for recipe in recipes:
                if self._validate_and_add(recipe):
                    count += 1
                    self.log(f"✓ Imported: {recipe.get('name', 'Unknown')}")
            
            self.log(f"📄 {file_path.name}: {count} recipes imported")
            return count
            
        except json.JSONDecodeError as e:
            self.log(f"❌ JSON parse error in {file_path.name}: {e}")
            self.errors.append(str(e))
            return 0
        except Exception as e:
            self.log(f"❌ Error processing {file_path.name}: {e}")
            self.errors.append(str(e))
            return 0
    
    def _import_csv(self, file_path: Path) -> int:
        """Import recipes from CSV file"""
        try:
            count = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    recipe = {
                        'name': row.get('name', row.get('Name', 'Unknown')),
                        'ingredients': self._parse_list_field(
                            row.get('ingredients', row.get('Ingredients', ''))
                        ),
                        'instructions': self._parse_list_field(
                            row.get('instructions', row.get('Instructions', ''))
                        ),
                    }
                    
                    # Add optional fields if present
                    for key in ['description', 'servings', 'prep_time', 'cook_time']:
                        if key in row and row[key]:
                            recipe[key] = row[key]
                    
                    if self._validate_and_add(recipe):
                        count += 1
                        self.log(f"✓ Imported: {recipe.get('name', 'Unknown')}")
            
            self.log(f"📄 {file_path.name}: {count} recipes imported")
            return count
            
        except Exception as e:
            self.log(f"❌ Error processing CSV {file_path.name}: {e}")
            self.errors.append(str(e))
            return 0
    
    def _parse_list_field(self, field: str) -> List[str]:
        """Parse CSV field that might be a list (comma-separated or JSON)"""
        if not field:
            return []
        
        # Try JSON first
        if field.startswith('['):
            try:
                return json.loads(field)
            except:
                pass
        
        # Fall back to comma-separated
        return [item.strip() for item in field.split(',') if item.strip()]
    
    def _validate_and_add(self, recipe: Dict) -> bool:
        """Validate recipe structure and add if unique"""
        # Check required fields
        if not recipe.get('name'):
            self.log("⚠️  Skipping recipe with no name")
            return False
        
        # Generate ID from name (or use existing)
        recipe_id = recipe.get('id', self._generate_id(recipe['name']))
        recipe['id'] = recipe_id
        
        # Check for duplicates
        if recipe_id in self.recipes:
            self.duplicates.append({
                'id': recipe_id,
                'name': recipe['name'],
                'existing': self.recipes[recipe_id]['name']
            })
            self.log(f"⚠️  Duplicate: {recipe['name']} (skipping)")
            return False
        
        # Ensure standard fields
        recipe.setdefault('ingredients', [])
        recipe.setdefault('instructions', [])
        recipe.setdefault('metadata', {})
        
        self.recipes[recipe_id] = recipe
        return True
    
    def _generate_id(self, name: str) -> str:
        """Generate recipe ID from name"""
        # Convert to lowercase, replace spaces with underscores, remove special chars
        recipe_id = name.lower().strip()
        recipe_id = ''.join(c if c.isalnum() or c == '_' else '_' for c in recipe_id)
        recipe_id = '_'.join(word for word in recipe_id.split('_') if word)
        return recipe_id
    
    def save_recipes(self) -> int:
        """Save imported recipes to output directory"""
        count = 0
        for recipe_id, recipe in self.recipes.items():
            output_file = self.output_dir / f"{recipe_id}.json"
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(recipe, f, ensure_ascii=False, indent=2)
                count += 1
            except Exception as e:
                self.log(f"❌ Error saving {recipe_id}: {e}")
                self.errors.append(str(e))
        
        self.log(f"💾 Saved {count} recipes to {self.output_dir}")
        return count
    
    def log(self, message: str):
        """Log a message"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_entries.append(full_message)
        print(full_message)
    
    def write_log(self, log_file: str = None):
        """Write log to file"""
        if log_file is None:
            log_file = self.input_dir.parent / "IMPORT_LOG.md"
        
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("# Recipe.app Import Log\n\n")
            f.write(f"**Import Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write(f"## Summary\n\n")
            f.write(f"- **Total recipes imported:** {len(self.recipes)}\n")
            f.write(f"- **Duplicates found:** {len(self.duplicates)}\n")
            f.write(f"- **Errors:** {len(self.errors)}\n\n")
            
            if self.duplicates:
                f.write("## Duplicates\n\n")
                for dup in self.duplicates:
                    f.write(f"- **{dup['name']}** (ID: {dup['id']})\n")
                f.write("\n")
            
            if self.errors:
                f.write("## Errors\n\n")
                for error in self.errors:
                    f.write(f"- {error}\n")
                f.write("\n")
            
            f.write("## Log Entries\n\n")
            for entry in self.log_entries:
                f.write(f"{entry}\n")
        
        print(f"✅ Log written to {log_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python import_recipe_app_recipes.py <input_dir> [--output <output_dir>]")
        print("\nExample:")
        print("  python import_recipe_app_recipes.py raw/")
        print("  python import_recipe_app_recipes.py raw/ --output processed/")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = None
    
    if "--output" in sys.argv:
        idx = sys.argv.index("--output")
        if idx + 1 < len(sys.argv):
            output_dir = sys.argv[idx + 1]
    
    print("=" * 70)
    print("Recipe.app Import Tool")
    print("=" * 70)
    print()
    
    importer = RecipeAppImporter(input_dir, output_dir)
    
    print(f"📂 Input directory: {importer.input_dir}")
    print(f"💾 Output directory: {importer.output_dir}")
    print()
    
    # Import recipes
    imported_count = importer.import_all()
    print()
    
    # Save recipes
    if imported_count > 0:
        saved_count = importer.save_recipes()
        importer.log(f"✅ Import complete: {saved_count} recipes saved")
    else:
        importer.log("⚠️  No recipes imported")
    
    # Write log
    print()
    importer.write_log()
    
    print()
    print("=" * 70)
    print(f"✅ Summary: {len(importer.recipes)} recipes imported")
    print(f"⚠️  Duplicates: {len(importer.duplicates)}")
    print(f"❌ Errors: {len(importer.errors)}")
    print("=" * 70)


if __name__ == "__main__":
    main()
