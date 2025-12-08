#!/usr/bin/env python3
"""
Generate a complete two-page recipe spread in Typst from comprehensive recipe JSON
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class RecipeSpreadGenerator:
    def __init__(self):
        self.recipes_dir = "data/recipes_comprehensive"
        self.typst_output_dir = "typst/recipe_spreads"
        Path(self.typst_output_dir).mkdir(parents=True, exist_ok=True)
    
    def load_recipe(self, recipe_file: str) -> Dict:
        """Load comprehensive recipe JSON"""
        file_path = Path(self.recipes_dir) / recipe_file
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def escape_typst(self, text: str) -> str:
        """Escape special characters for Typst"""
        if not text:
            return ""
        text = str(text)
        text = text.replace("\\", "\\\\")
        text = text.replace('"', '\\"')
        text = text.replace("#", "\\#")
        return text
    
    def format_ingredients_en(self, ingredients: list) -> str:
        """Format ingredients for English section"""
        lines = []
        for ing in ingredients:
            if isinstance(ing, dict):
                name = self.escape_typst(ing.get('name', ''))
                amount = ing.get('amount', '')
                unit = ing.get('unit', '')
                if amount and unit:
                    lines.append(f'        #ingredient_item("{name}", amount: "{amount}", unit: "{unit}")')
                else:
                    lines.append(f'        #ingredient_item("{name}")')
            else:
                name = self.escape_typst(str(ing))
                lines.append(f'        #ingredient_item("{name}")')
        return '\n'.join(lines)
    
    def format_instructions_en(self, instructions: list) -> str:
        """Format instructions for English section"""
        lines = []
        for inst in instructions:
            if isinstance(inst, dict):
                text = self.escape_typst(inst.get('text', ''))
                step = inst.get('step', 0)
                lines.append(f"        {step}. {text}")
            else:
                text = self.escape_typst(str(inst))
                lines.append(f"        • {text}")
        return '\n'.join(lines)
    
    def generate_typst(self, recipe: Dict) -> str:
        """Generate complete Typst file for recipe spread"""
        
        # Extract recipe data
        names = recipe.get('names', {})
        name_en = self.escape_typst(names.get('english', 'Recipe'))
        name_he = names.get('hebrew', '')
        name_ar = names.get('arabic', '[Arabic translation needed]')
        name_es = names.get('spanish', '[Spanish translation needed]')
        
        metadata = recipe.get('metadata', {})
        category = metadata.get('category', 'Main Dish')
        serves = metadata.get('serves', '4-6 people')
        prep_time = metadata.get('prep_time_minutes', 20)
        cook_time = metadata.get('cook_time_minutes', 30)
        
        # Extract sections
        ingredients = recipe.get('ingredients', {}).get('english', [])
        instructions = recipe.get('instructions', {}).get('english', [])
        etymology = recipe.get('etymology', {}).get('english', {})
        history = recipe.get('history', {}).get('english', {})
        djerban = recipe.get('djerban_tradition', {}).get('english', {})
        
        etymology_summary = self.escape_typst(etymology.get('summary', 'Traditional dish with rich cultural heritage'))
        history_summary = self.escape_typst(history.get('summary', 'An important part of Tunisian-Djerban Jewish cuisine'))
        djerban_summary = self.escape_typst(djerban.get('summary', 'Represents family tradition and cultural continuity'))
        
        ingredients_formatted = self.format_ingredients_en(ingredients)
        instructions_formatted = self.format_instructions_en(instructions)
        
        # Build Typst file
        typst_content = f'''// AUTO-GENERATED RECIPE SPREAD
// Recipe: {name_en}
// Generated for multilingual cookbook

// ===== COLOR SCHEME =====
#let primary_color = rgb("#8B4513")    // Saddle brown
#let secondary_color = rgb("#D2B48C")  // Tan
#let accent_color = rgb("#DC143C")     // Crimson

#set page(
  paper: "a4",
  margin: (left: 1cm, right: 1cm, top: 1cm, bottom: 1cm),
  header: none,
  footer: none,
)

#set text(font: "Georgia", size: 10pt, lang: "en")

// ===== HELPER FUNCTIONS =====

#let floating_box(title, content, bg_color: rgb("#f5f5f5")) = {{
  block(
    fill: bg_color,
    stroke: 1pt + rgb("#999"),
    radius: 6pt,
    inset: 0.6cm,
    [
      #text(size: 11pt, weight: "bold", fill: primary_color, title)
      #v(0.3cm)
      #text(size: 9pt, content)
    ]
  )
}}

#let two_column_layout(left_content, right_content) = {{
  grid(
    columns: (1fr, 1fr),
    gutter: 0.8cm,
    left_content,
    right_content,
  )
}}

#let ingredient_item(name, amount: "", unit: "") = {{
  text(size: 9pt)[
    • #name
    #if amount != "" {{
      text(fill: gray, " (" + amount + " " + unit + ")")
    }}
  ]
}}

// ===== RECIPE DATA =====
#let recipe_name_en = "{name_en}"
#let recipe_name_he = "{name_he}"
#let recipe_name_ar = "{name_ar}"
#let recipe_name_es = "{name_es}"
#let recipe_category = "{category}"
#let recipe_serves = "{serves}"
#let recipe_prep = "{prep_time} min"
#let recipe_cook = "{cook_time} min"

// ===== PAGE 1: ENGLISH & LAYOUT =====

#align(center)[
  #text(size: 22pt, weight: "bold", fill: primary_color)[
    #recipe_name_en
  ]
  
  #v(0.2cm)
  
  #text(size: 10pt, fill: gray)[
    #recipe_name_he #h(1cm) #recipe_name_ar #h(1cm) #recipe_name_es
  ]
  
  #v(0.4cm)
  
  #line(length: 80%, stroke: 1.5pt + secondary_color)
]

#v(0.6cm)

#two_column_layout(
  // LEFT COLUMN
  [
    // ETYMOLOGY
    #floating_box(
      "Etymology",
      [
        {etymology_summary}
      ],
      bg_color: rgb("#e8f4f8")
    )
    
    #v(0.5cm)
    
    // INGREDIENTS
    #floating_box(
      "Ingredients",
      [
{ingredients_formatted}
      ],
      bg_color: rgb("#fff8e8")
    )
  ],
  
  // RIGHT COLUMN
  [
    // INSTRUCTIONS
    #floating_box(
      "Instructions",
      [
        {instructions_formatted}
      ],
      bg_color: rgb("#f0e8ff")
    )
    
    #v(0.5cm)
    
    // DJERBAN TRADITION
    #floating_box(
      "Djerban Tradition",
      [
        {djerban_summary}
      ],
      bg_color: rgb("#ffe8f0")
    )
  ]
)

#pagebreak()

// ===== PAGE 2: HISTORY & MULTILINGUAL REFERENCE =====

#align(center)[
  #text(size: 18pt, weight: "bold", fill: primary_color)[
    History & Cultural Context
  ]
]

#v(0.4cm)

#floating_box(
  "Historical Background",
  [
    {history_summary}
  ],
  bg_color: rgb("#e8e8f0")
)

#v(0.6cm)

#align(center, text(size: 12pt, weight: "bold", fill: primary_color)[
  Multilingual Reference
])

#v(0.3cm)

#floating_box(
  "Hebrew (עברית)",
  [
    *שם המתכון:* {name_he}
    
    This section would contain the full Hebrew version of the recipe.
  ],
  bg_color: rgb("#e8f4f8")
)

#v(0.3cm)

#floating_box(
  "Arabic (العربية)",
  [
    *اسم الوصفة:* {name_ar}
    
    This section would contain the full Arabic version of the recipe.
  ],
  bg_color: rgb("#f0e8ff")
)

#v(0.3cm)

#floating_box(
  "Spanish (Español)",
  [
    *Nombre de la Receta:* {name_es}
    
    This section would contain the full Spanish version of the recipe.
  ],
  bg_color: rgb("#ffe8f0")
)

#v(0.6cm)

// FOOTER
#align(center, text(size: 8pt, fill: gray)[
  {name_en} | Serves: {serves} | Prep: {prep_time} min | Cook: {cook_time} min | {category}
])
'''
        
        return typst_content
    
    def generate_recipe_spread(self, recipe_file: str) -> bool:
        """Generate complete recipe spread"""
        recipe = self.load_recipe(recipe_file)
        if not recipe:
            print(f"❌ Failed to load {recipe_file}")
            return False
        
        recipe_name_en = recipe.get('names', {}).get('english', 'recipe')
        
        # Generate Typst content
        typst_content = self.generate_typst(recipe)
        
        # Save Typst file
        output_file = Path(self.typst_output_dir) / f"{recipe_name_en.lower().replace(' ', '_')}.typ"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(typst_content)
        
        # Compile to PDF
        pdf_file = output_file.with_suffix('.pdf')
        os.system(f'cd typst && typst compile recipe_spreads/{output_file.name} recipe_spreads/{pdf_file.name} 2>/dev/null')
        
        print(f"✓ Generated: {recipe_name_en}")
        print(f"  📄 Typst: {output_file}")
        print(f"  📊 PDF: {pdf_file}")
        
        return True


def main():
    try:
        generator = RecipeSpreadGenerator()
        
        print("\n" + "=" * 70)
        print("RECIPE SPREAD GENERATOR")
        print("=" * 70 + "\n")
        
        # Generate for one recipe as example
        recipe_file = "00_מחמסה_en.json"
        
        print(f"Generating recipe spread for: {recipe_file}\n")
        
        if generator.generate_recipe_spread(recipe_file):
            print("\n✓ Recipe spread generation complete!")
            print(f"📁 Output directory: typst/recipe_spreads/")
            print("\nTo generate all 35 recipes:")
            print("  recipes = [f for f in os.listdir('data/recipes_comprehensive') if f.endswith('.json')]")
            print("  for recipe_file in recipes:")
            print("    generator.generate_recipe_spread(recipe_file)")
        else:
            print("\n❌ Failed to generate recipe spread")
            return 1
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())

