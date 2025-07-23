#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from docx import Document
import os
import re
from markdownify import markdownify as md

def clean_filename(text):
    """Clean text for use as filename"""
    # Remove or replace problematic characters
    cleaned = re.sub(r'[<>:"/\\|?*]', '', text)
    cleaned = re.sub(r'\s+', '_', cleaned.strip())
    return cleaned[:50]  # Limit length

def extract_recipes(filepath):
    """Extract individual recipes from the docx file"""
    print(f"Processing: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return []
    
    try:
        doc = Document(filepath)
        recipes = []
        current_recipe = []
        recipe_name = ""
        in_recipe = False
        
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            
            if not text:
                if in_recipe:
                    current_recipe.append("")  # Add empty line
                continue
            
            # Check if this is the start of a new recipe
            if text.startswith("שם המתכון:"):
                # Save previous recipe if exists
                if current_recipe and recipe_name:
                    recipes.append({
                        'name': recipe_name,
                        'content': current_recipe.copy()
                    })
                
                # Start new recipe
                recipe_name = text.replace("שם המתכון:", "").strip()
                current_recipe = [text]
                in_recipe = True
                print(f"Found recipe: {recipe_name}")
                
            elif in_recipe:
                current_recipe.append(text)
                
                # Check if this is the end of the recipe
                if text == "בתאבון!!!":
                    recipes.append({
                        'name': recipe_name,
                        'content': current_recipe.copy()
                    })
                    current_recipe = []
                    recipe_name = ""
                    in_recipe = False
        
        # Handle last recipe if it doesn't end with "בתאבון!!!"
        if current_recipe and recipe_name:
            recipes.append({
                'name': recipe_name,
                'content': current_recipe.copy()
            })
            
        print(f"Extracted {len(recipes)} recipes")
        return recipes
        
    except Exception as e:
        print(f"Error processing document: {e}")
        return []

def convert_to_markdown(recipe):
    """Convert recipe content to markdown format"""
    content_lines = []
    
    for line in recipe['content']:
        if line.startswith("שם המתכון:"):
            # Recipe title
            name = line.replace("שם המתכון:", "").strip()
            content_lines.append(f"# {name}\n")
            
        elif line.startswith("רשימת מצרכים:"):
            # Ingredients section
            content_lines.append("## רשימת מצרכים (Ingredients)\n")
            
        elif line.startswith("אופן ההכנה:"):
            # Instructions section
            content_lines.append("## אופן ההכנה (Instructions)\n")
            
        elif line.startswith("תבלינים:"):
            # Spices/seasonings
            content_lines.append(f"**{line}**\n")
            
        elif line == "בתאבון!!!":
            # End marker
            content_lines.append("---\n**בתאבון!!!** (Bon Appétit!)\n")
            
        elif line.startswith(("למחמסה", "להכנת", "לרוטב:", "סירופ:")):
            # Sub-sections
            content_lines.append(f"### {line}\n")
            
        elif line.strip() and any(line.startswith(prefix) for prefix in ["1.", "2.", "3.", "4.", "5."]):
            # Numbered steps
            content_lines.append(f"{line}\n")
            
        elif line.strip():
            # Regular content - check if it's an ingredient or instruction
            if len(line) < 50 and not any(verb in line for verb in ["מוסיפים", "שמים", "מטגנים", "לבשל", "מערבבים"]):
                # Likely an ingredient
                content_lines.append(f"- {line}\n")
            else:
                # Likely an instruction
                content_lines.append(f"{line}\n")
        else:
            # Empty line
            content_lines.append("\n")
    
    return "".join(content_lines)

def save_recipes(recipes, output_dir="recipes"):
    """Save each recipe as a separate markdown file"""
    
    # Create output directory
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    saved_count = 0
    
    for i, recipe in enumerate(recipes, 1):
        try:
            # Create filename
            clean_name = clean_filename(recipe['name'])
            if not clean_name:
                clean_name = f"recipe_{i}"
            
            filename = f"{i:02d}_{clean_name}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Convert to markdown
            markdown_content = convert_to_markdown(recipe)
            
            # Save file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Saved: {filepath}")
            saved_count += 1
            
        except Exception as e:
            print(f"Error saving recipe '{recipe['name']}': {e}")
    
    print(f"\nSuccessfully saved {saved_count} recipe files to '{output_dir}' directory")
    return saved_count

def main():
    """Main function"""
    # Input file
    input_file = "מתכונים לדוד.docx"
    
    print("Hebrew Recipe Splitter")
    print("=" * 50)
    
    # Extract recipes
    recipes = extract_recipes(input_file)
    
    if not recipes:
        print("No recipes found!")
        return
    
    # Save recipes
    saved = save_recipes(recipes)
    
    print(f"\nProcess completed!")
    print(f"Original file: {input_file}")
    print(f"Recipes extracted: {len(recipes)}")
    print(f"Files saved: {saved}")

if __name__ == "__main__":
    main() 