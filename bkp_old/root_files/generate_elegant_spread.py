#!/usr/bin/env python3
"""
Generate Elegant 4-Language Recipe Spread
"""

import json
import os
from pathlib import Path

class ElegantSpreadGenerator:
    def __init__(self):
        self.recipes_dir = "data/recipes_comprehensive"
        self.output_dir = "typst/recipe_spreads"
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)

    def load_recipe(self, filename):
        with open(Path(self.recipes_dir) / filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def format_ingredients(self, ingredients):
        # Convert list of dicts to Typst bullet points
        items = []
        for ing in ingredients:
            if isinstance(ing, dict):
                text = f"{ing['amount']} {ing['unit']} {ing['name']}".strip()
            else:
                text = str(ing)
            items.append(f"- {text}")
        return "\n".join(items)

    def format_instructions(self, instructions):
        # Convert to numbered list
        items = []
        for inst in instructions:
            if isinstance(inst, dict):
                text = inst['text']
            else:
                text = str(inst)
            items.append(f"+ {text}")
        return "\n".join(items)

    def generate_typst(self, recipe):
        # Extract Data
        name_en = recipe['names']['english']
        name_he = recipe['names']['hebrew']
        # Mocking other names for visual proof
        name_ar = "المحمسة" 
        name_es = "Mahmessa"

        # Ingredients
        ing_en = self.format_ingredients(recipe['ingredients']['english'])
        # Mocking others
        ing_he = ing_en # In real version, this would be Hebrew text
        ing_ar = ing_en
        ing_es = ing_en

        # Instructions
        inst_en = self.format_instructions(recipe['instructions']['english'])
        inst_he = inst_en
        inst_ar = inst_en
        inst_es = inst_en

        # Story (Combine Etymology, History, Tradition)
        etym = recipe['etymology']['english'].get('summary', '')
        hist = recipe['history']['english'].get('summary', '')
        trad = recipe['djerban_tradition']['english'].get('summary', '')
        
        story_en = f"{etym} {hist} {trad}".replace('"', '\\"')
        story_he = story_en # Mock
        story_ar = story_en # Mock
        story_es = story_en # Mock

        # Typst Template Content
        template = f"""
// ELEGANT SPREAD FOR: {name_en}

#set page(
  paper: "a4",
  margin: (top: 1.5cm, bottom: 1.5cm, left: 1.5cm, right: 1.5cm),
  header: none,
  footer: none
)

#set text(font: ("Times New Roman", "Arial"), size: 10pt, fill: rgb("#202020"))
#let accent_color = rgb("#8B4513")
#let border_color = rgb("#dddddd")

// --- FUNCTIONS ---

#let language_section(title, ingredients, instructions, story, dir, font) = {{
  set text(font: font, dir: dir)
  block(
    height: 48%,
    width: 100%,
    inset: 1em,
    stroke: (bottom: 0.5pt + border_color),
    [
      #align(center, text(size: 18pt, weight: "bold", fill: accent_color, title))
      #v(1em)
      #grid(
        columns: if dir == rtl {{ (2fr, 1fr) }} else {{ (1fr, 2fr) }},
        gutter: 2em,
        
        // COL 1
        if dir == ltr {{
           [
             #text(weight: "bold")[Ingredients]
             #v(0.5em)
             #ingredients
           ]
        }} else {{
           [
             #text(weight: "bold")[Preparation]
             #v(0.5em)
             #instructions
             #v(1em)
             #line(length: 100%, stroke: 0.5pt + border_color)
             #v(0.5em)
             #text(style: "italic", story)
           ]
        }},

        // COL 2
        if dir == ltr {{
           [
             #text(weight: "bold")[Preparation]
             #v(0.5em)
             #instructions
             #v(1em)
             #line(length: 100%, stroke: 0.5pt + border_color)
             #v(0.5em)
             #text(style: "italic", story)
           ]
        }} else {{
           [
             #text(weight: "bold")[Ingredients]
             #v(0.5em)
             #ingredients
           ]
        }}
      )
    ]
  )
}}

// --- VERSO (LEFT PAGE) - SEMITIC LANGUAGES ---

#language_section(
  "{name_he}", // Hebrew Title
  [{ing_he}],
  [{inst_he}],
  "{story_he}",
  rtl,
  "Arial" // Placeholder for Hebrew font
)

#v(1fr) // Spacer

#language_section(
  "{name_ar}", // Arabic Title
  [{ing_ar}],
  [{inst_ar}],
  "{story_ar}",
  rtl,
  "Arial" // Placeholder for Arabic font
)

#pagebreak()

// --- RECTO (RIGHT PAGE) - EUROPEAN LANGUAGES ---

#language_section(
  "{name_en}", // English Title
  [{ing_en}],
  [{inst_en}],
  "{story_en}",
  ltr,
  "Times New Roman"
)

#v(1fr)

#language_section(
  "{name_es}", // Spanish Title
  [{ing_es}],
  [{inst_es}],
  "{story_es}",
  ltr,
  "Times New Roman"
)

"""
        return template

    def generate(self, filename):
        recipe = self.load_recipe(filename)
        content = self.generate_typst(recipe)
        
        out_name = filename.replace('.json', '_elegant.typ')
        with open(Path(self.output_dir) / out_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated {out_name}")

if __name__ == "__main__":
    gen = ElegantSpreadGenerator()
    gen.generate("00_מחמסה_en.json")

