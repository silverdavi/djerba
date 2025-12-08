#!/usr/bin/env python3
"""
Generate Complete Cookbook HTML with Text Spreads and Full-Page Images
"""

import json
import os
from pathlib import Path

class CookbookHTMLGenerator:
    def __init__(self):
        self.recipes_dir = "data/recipes_comprehensive"
        self.images_dir = "data/images/generated"
        self.output_file = "cookbook_preview.html"
        self.recipes = []

    def load_data(self):
        files = sorted([f for f in os.listdir(self.recipes_dir) if f.endswith('.json')])
        for f in files:
            with open(Path(self.recipes_dir) / f, 'r', encoding='utf-8') as file:
                self.recipes.append(json.load(file))

    def get_image_path(self, recipe_name_en):
        # Specific override for Mahmessa corrected image
        if 'mahmessa' in recipe_name_en.lower():
            if os.path.exists("data/images/generated/mahmessa_corrected.png"):
                return "data/images/generated/mahmessa_corrected.png"
        
        # Default logic
        safe_name = recipe_name_en.lower().replace(' ', '_').replace('(', '').replace(')', '').replace(',', '')
        img_name = f"{safe_name}.png"
        if os.path.exists(f"data/images/generated/{img_name}"):
            return f"data/images/generated/{img_name}"
        # Try searching for partial matches if exact name fails
        for f in os.listdir(self.images_dir):
            if safe_name in f.lower() and f.endswith('.png'):
                return f"data/images/generated/{f}"
        return None

    def generate_html(self):
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Djerban Family Cookbook</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Frank+Ruhl+Libre:wght@400;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #5D4037;
            --accent-color: #D84315;
            --text-color: #2c2c2c;
            --bg-color: #fcfbf9;
            --divider-color: #e0dcd5;
            --page-width: 210mm;
            --page-height: 297mm;
        }
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            background-color: #333;
            font-family: 'Lora', serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px;
        }

        .spread-wrapper {
            display: flex;
            margin-bottom: 60px;
            box-shadow: 0 0 50px rgba(0,0,0,0.5);
        }

        .page {
            width: var(--page-width);
            height: var(--page-height);
            background-color: var(--bg-color);
            position: relative;
            overflow: hidden;
        }

        /* TEXT PAGES STYLING */
        .page.text-page { padding: 20mm; display: flex; flex-direction: column; }
        .page.verso { border-right: 1px solid #e5e5e5; }
        
        .language-section {
            flex: 1;
            display: flex;
            flex-direction: column;
            margin-bottom: 8mm;
            padding-bottom: 8mm;
            border-bottom: 1px solid var(--divider-color);
        }
        .language-section:last-child { margin-bottom: 0; padding-bottom: 0; border-bottom: none; }

        .lang-he { font-family: 'Frank Ruhl Libre', serif; direction: rtl; }
        .lang-ar { font-family: 'Amiri', serif; direction: rtl; }
        .lang-en { font-family: 'Playfair Display', serif; direction: ltr; }
        .lang-es { font-family: 'Playfair Display', serif; direction: ltr; }

        h1 { font-size: 20pt; color: var(--primary-color); margin-bottom: 0.2em; text-transform: uppercase; letter-spacing: 0.05em; }
        .lang-he h1, .lang-ar h1 { letter-spacing: 0; }

        .recipe-grid { display: grid; grid-template-columns: 1fr 2fr; gap: 6mm; margin-top: 4mm; flex-grow: 1; }
        .lang-he .recipe-grid, .lang-ar .recipe-grid { grid-template-columns: 2fr 1fr; }

        .ingredients-col { font-family: 'Lora', serif; font-size: 8.5pt; line-height: 1.4; border-right: 1px solid var(--divider-color); padding-right: 4mm; }
        .lang-he .ingredients-col, .lang-ar .ingredients-col { border-right: none; border-left: 1px solid var(--divider-color); padding-right: 0; padding-left: 4mm; }

        .instructions-col { font-family: 'Lora', serif; font-size: 9.5pt; line-height: 1.4; }

        h2 { font-size: 8pt; color: var(--accent-color); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5em; border-bottom: 1px solid var(--accent-color); display: inline-block; }

        ul { list-style: none; }
        li { margin-bottom: 0.2em; }
        ol { margin-left: 1.2em; }
        .lang-he ol, .lang-ar ol { margin-right: 1.2em; margin-left: 0; }

        .story-text { margin-top: 3mm; font-style: italic; color: #666; font-size: 9pt; border-top: 1px solid var(--divider-color); padding-top: 2mm; }

        /* IMAGE PAGE STYLING */
        .page.image-page {
            padding: 0;
            background-color: #000;
        }
        .full-page-image {
            width: 100%;
            height: 100%;
            object-fit: cover;
            opacity: 0.9;
        }
        
        /* Geometric Pattern Overlay */
        .geometric-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 12mm solid #fff; 
            box-sizing: border-box;
            pointer-events: none;
            z-index: 5;
        }
        
        /* The Pattern itself - SVG background */
        .pattern-texture {
            position: absolute;
            top: 12mm;
            left: 12mm;
            right: 12mm;
            bottom: 12mm;
            background-image: url('data:image/svg+xml;utf8,<svg width="40" height="40" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%23ffffff" fill-opacity="0.15"><path d="M0 40L40 0H20L0 20M40 40V20L20 40"/></g></g></svg>');
            pointer-events: none;
            z-index: 6;
        }
        
        .image-title-box {
            position: absolute;
            bottom: 25mm;
            left: 50%;
            transform: translateX(-50%);
            background-color: white;
            padding: 15px 50px;
            text-align: center;
            box-shadow: 0 10px 20px rgba(0,0,0,0.15);
            z-index: 10;
            min-width: 60%;
        }
        
        .image-title-en {
            font-family: 'Playfair Display', serif;
            font-size: 22pt;
            color: var(--primary-color);
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }
        
        .image-title-he {
            font-family: 'Frank Ruhl Libre', serif;
            font-size: 16pt;
            color: var(--accent-color);
            margin-top: 5px;
        }

        /* Pattern Page (Back of Image) */
        .page.pattern-page {
            background-color: var(--bg-color);
            background-image: url('data:image/svg+xml;utf8,<svg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><g fill="%235D4037" fill-opacity="0.05"><path d="M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z"/></g></g></svg>');
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .family-note-card {
            width: 65%;
            height: 50%;
            background-color: white;
            padding: 20mm;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            border: 1px solid #eee;
        }

        @media print {
            body { background: none; padding: 0; }
            .spread-wrapper { box-shadow: none; margin: 0; break-after: always; }
        }
    </style>
</head>
<body>
"""

        for recipe in self.recipes:
            name_en = recipe['names']['english']
            name_he = recipe['names']['hebrew']
            name_ar = f"وصفة {name_en}"
            name_es = f"Receta de {name_en}"

            ing_list_en = "<ul>" + "".join([f"<li>{i.get('amount','')} {i.get('unit','')} {i.get('name','')}</li>" for i in recipe['ingredients']['english']]) + "</ul>"
            inst_list_en = "<ol>" + "".join([f"<li>{i.get('text','')}</li>" for i in recipe['instructions']['english']]) + "</ol>"

            etym = recipe['etymology']['english'].get('summary', '')
            hist = recipe['history']['english'].get('summary', '')
            trad = recipe['djerban_tradition']['english'].get('summary', '')
            story_en = f"{etym} {hist} {trad}"[:350] + "..."

            img_src = self.get_image_path(name_en)
            
            # SPREAD 1: TEXT (4 LANGUAGES)
            html_content += f"""
<div class="spread-wrapper">
    <!-- LEFT PAGE (Verso) -->
    <div class="page verso text-page">
        <div class="language-section lang-he">
            <h1>{name_he}</h1>
            <div class="recipe-grid">
                <div class="instructions-col">
                    <h2>הוראות הכנה</h2>
                    <ol><li>[הוראות בעברית יבואו כאן...]</li><li>שלב נוסף בתהליך ההכנה.</li></ol>
                    <p class="story-text">{story_en} (Hebrew trans)</p>
                </div>
                <div class="ingredients-col">
                    <h2>מצרכים</h2>
                    <ul><li>מרכיב 1</li><li>מרכיב 2</li></ul>
                </div>
            </div>
        </div>
        <div class="language-section lang-ar">
            <h1>{name_ar}</h1>
            <div class="recipe-grid">
                <div class="instructions-col">
                    <h2>طريقة التحضير</h2>
                    <ol><li>[التعليمات بالعربية ستكون هنا...]</li></ol>
                    <p class="story-text">{story_en} (Arabic trans)</p>
                </div>
                <div class="ingredients-col">
                    <h2>المكونات</h2>
                    <ul><li>مكون 1</li><li>مكون 2</li></ul>
                </div>
            </div>
        </div>
    </div>

    <!-- RIGHT PAGE (Recto) -->
    <div class="page recto text-page">
        <div class="language-section lang-en">
            <h1>{name_en}</h1>
            <div class="recipe-grid">
                <div class="ingredients-col">
                    <h2>Ingredients</h2>
                    {ing_list_en}
                </div>
                <div class="instructions-col">
                    <h2>Preparation</h2>
                    {inst_list_en}
                    <p class="story-text">{story_en}</p>
                </div>
            </div>
        </div>
        <div class="language-section lang-es">
            <h1>{name_es}</h1>
            <div class="recipe-grid">
                <div class="ingredients-col">
                    <h2>Ingredientes</h2>
                    <ul><li>Ingrediente 1</li><li>Ingrediente 2</li></ul>
                </div>
                <div class="instructions-col">
                    <h2>Preparación</h2>
                    <ol><li>[Instrucciones en español...]</li></ol>
                    <p class="story-text">{story_en} (Spanish trans)</p>
                </div>
            </div>
        </div>
    </div>
</div>
"""
            # SPREAD 2: IMAGE & NOTES
            if img_src:
                html_content += f"""
<div class="spread-wrapper">
    <!-- LEFT PAGE: FULL IMAGE -->
    <div class="page image-page">
        <img src="{img_src}" class="full-page-image" alt="{name_en}">
        <div class="geometric-overlay"></div>
        <div class="pattern-texture"></div>
        <div class="image-title-box">
            <div class="image-title-en">{name_en}</div>
            <div class="image-title-he">{name_he}</div>
        </div>
    </div>
    
    <!-- RIGHT PAGE: PATTERN / NOTES -->
    <div class="page pattern-page">
        <div class="family-note-card">
            <h2 style="color:#5D4037; border:none; font-size:14pt; letter-spacing:0.2em;">FAMILY TRADITIONS</h2>
            <p style="font-style:italic; margin-top:20px; font-size:11pt; color:#666;">
                "Food is the thread that connects our past to our future."
            </p>
            <div style="margin-top:40px; border-top:1px solid #ddd; width:40%;"></div>
            <p style="margin-top:30px; font-size:10pt; line-height:1.8; color:#444;">
                Space for handwritten notes, family photos, or specific anecdotes about the {name_en} dish.
            </p>
        </div>
    </div>
</div>
"""

        html_content += "</body></html>"
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated {self.output_file}")

if __name__ == "__main__":
    gen = CookbookHTMLGenerator()
    gen.load_data()
    gen.generate_html()
