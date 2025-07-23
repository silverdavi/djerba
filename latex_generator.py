#!/usr/bin/env python3
"""
LaTeX Book Generator for Vegan Djerban Family Cookbook
Converts generated recipes into professional LaTeX cookbook format
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

class LaTeXGenerator:
    def __init__(self):
        self.setup_latex_structure()
        
    def setup_latex_structure(self):
        """Create LaTeX project structure"""
        latex_dirs = [
            "latex/chapters",
            "latex/recipes/english",
            "latex/recipes/hebrew", 
            "latex/recipes/spanish",
            "latex/recipes/arabic",
            "latex/images",
            "latex/styles",
            "latex/fonts",
            "latex/output"
        ]
        
        for dir_path in latex_dirs:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            
    def create_document_class(self):
        """Create custom cookbook document class"""
        cookbook_cls = '''%% cookbook.cls - Custom document class for Vegan Djerban Family Cookbook
\\NeedsTeXFormat{LaTeX2e}
\\ProvidesClass{cookbook}[2024/12/19 Vegan Djerban Family Cookbook Class]

% Base class
\\LoadClass[11pt,a4paper,twoside]{book}

% Required packages
\\RequirePackage[utf8]{inputenc}
\\RequirePackage{fontspec}
\\RequirePackage{polyglossia}
\\RequirePackage[margin=2.5cm,top=3cm,bottom=3cm]{geometry}
\\RequirePackage{graphicx}
\\RequirePackage{xcolor}
\\RequirePackage{tcolorbox}
\\RequirePackage{multicol}
\\RequirePackage{fancyhdr}
\\RequirePackage{titlesec}
\\RequirePackage{enumitem}
\\RequirePackage{array}
\\RequirePackage{booktabs}
\\RequirePackage{microtype}
\\RequirePackage{setspace}

% Language setup
\\setmainlanguage{english}
\\setotherlanguage{hebrew}
\\setotherlanguage{spanish}
\\setotherlanguage{arabic}

% Font setup
\\setmainfont{Crimson Pro}[
    Path = fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic,
    BoldItalicFont = *-BoldItalic
]

\\setsansfont{Inter}[
    Path = fonts/,
    Extension = .ttf,
    UprightFont = *-Regular,
    BoldFont = *-Bold,
    ItalicFont = *-Italic
]

\\newfontfamily\\hebrewfont{SBL Hebrew}[
    Path = fonts/,
    Extension = .ttf,
    Script = Hebrew
]

\\newfontfamily\\arabicfont{Scheherazade New}[
    Path = fonts/,
    Extension = .ttf,
    Script = Arabic
]

% Color scheme
\\definecolor{djerbaBlue}{RGB}{41, 128, 185}
\\definecolor{tangierGold}{RGB}{241, 196, 15}
\\definecolor{warmBrown}{RGB}{125, 102, 79}
\\definecolor{oliveGreen}{RGB}{142, 152, 103}
\\definecolor{lightBg}{RGB}{250, 250, 248}

% Custom environments
\\newtcolorbox{culturalcontext}{
    colback=lightBg,
    colframe=djerbaBlue,
    boxrule=1.5pt,
    arc=3pt,
    left=10pt,
    right=10pt,
    top=8pt,
    bottom=8pt,
    fonttitle=\\bfseries\\sffamily,
    title=Cultural Heritage
}

\\newtcolorbox{recipecard}{
    colback=white,
    colframe=warmBrown,
    boxrule=1pt,
    arc=2pt,
    left=15pt,
    right=15pt,
    top=10pt,
    bottom=10pt
}

% Recipe environment
\\newenvironment{recipe}[1]{
    \\chapter{#1}
    \\thispagestyle{fancy}
}{
    \\clearpage
}

% Multilingual recipe sections
\\newcommand{\\recipesection}[2]{
    \\section*{\\textcolor{djerbaBlue}{#1}}
    \\selectlanguage{#2}
}

% Ingredient list styling
\\newenvironment{ingredientlist}{
    \\begin{multicols}{2}
    \\begin{itemize}[leftmargin=*,itemsep=3pt]
}{
    \\end{itemize}
    \\end{multicols}
}

% Instructions styling
\\newenvironment{instructions}{
    \\begin{enumerate}[leftmargin=*,itemsep=5pt]
}{
    \\end{enumerate}
}

% Header/footer styling
\\pagestyle{fancy}
\\fancyhf{}
\\fancyhead[LE]{\\sffamily\\small\\leftmark}
\\fancyhead[RO]{\\sffamily\\small\\rightmark}
\\fancyfoot[C]{\\sffamily\\thepage}
\\renewcommand{\\headrulewidth}{0.5pt}
\\renewcommand{\\footrulewidth}{0pt}

% Chapter styling
\\titleformat{\\chapter}[display]
{\\sffamily\\huge\\bfseries\\color{djerbaBlue}}
{\\filright\\large\\color{tangierGold}Chapter \\thechapter}
{20pt}
{\\filleft}

\\titlespacing*{\\chapter}{0pt}{-30pt}{40pt}

% Section styling
\\titleformat{\\section}
{\\sffamily\\Large\\bfseries\\color{warmBrown}}
{\\thesection}
{1em}
{}

\\titleformat{\\subsection}
{\\sffamily\\large\\bfseries\\color{oliveGreen}}
{\\thesubsection}
{1em}
{}

% Custom commands
\\newcommand{\\recipetime}[1]{\\textcolor{djerbaBlue}{\\sffamily\\textbf{Time:} #1}}
\\newcommand{\\recipeserves}[1]{\\textcolor{djerbaBlue}{\\sffamily\\textbf{Serves:} #1}}
\\newcommand{\\recipedifficulty}[1]{\\textcolor{djerbaBlue}{\\sffamily\\textbf{Difficulty:} #1}}

% Hebrew text command
\\newcommand{\\heb}[1]{\\begingroup\\hebrewfont\\selectlanguage{hebrew}#1\\endgroup}
\\newcommand{\\ar}[1]{\\begingroup\\arabicfont\\selectlanguage{arabic}#1\\endgroup}
'''
        
        with open('latex/styles/cookbook.cls', 'w', encoding='utf-8') as f:
            f.write(cookbook_cls)
            
    def create_main_document(self):
        """Create main LaTeX document"""
        main_tex = '''\\documentclass{cookbook}

\\usepackage[hidelinks]{hyperref}
\\usepackage{bookmark}

% Document metadata
\\title{Vegan Djerban Family Cookbook\\\\
       \\large A Journey Through North African Jewish Cuisine}
\\author{David Silver \& Enny Silver\\\\
        \\small Honoring the culinary heritage of\\\\
        \\small Ruth Cohen-Trabelsi (Djerba, Tunisia) \&\\\\
        \\small Kadoch-Muyal (Tangier, Morocco)}
\\date{\\today}

\\begin{document}

% Title page
\\maketitle
\\thispagestyle{empty}

% Copyright page
\\clearpage
\\thispagestyle{empty}
\\vspace*{\\fill}
\\begin{center}
\\textcopyright\\ 2024 David Silver \& Enny Silver\\\\[1em]
\\textit{Preserving family traditions through plant-based innovation}\\\\[2em]
First Edition\\\\[1em]
Generated using artificial intelligence research\\\\
and traditional family knowledge
\\end{center}
\\vspace*{\\fill}

% Table of contents
\\clearpage
\\tableofcontents

% Introduction
\\chapter*{Introduction}
\\addcontentsline{toc}{chapter}{Introduction}

This cookbook represents a bridge between generations, cultures, and culinary traditions. It honors the rich heritage of North African Jewish cuisine while embracing modern plant-based living.

Our family's culinary journey spans from the ancient island of Djerba in Tunisia to the vibrant port city of Tangier in Morocco. Through the recipes of Ruth Cohen-Trabelsi and the Kadoch-Muyal family line, we preserve not just dishes, but stories, memories, and cultural identity.

Each recipe has been carefully researched and adapted to be completely plant-based while maintaining the authentic flavors and cultural significance that have been passed down through generations.

\\begin{culturalcontext}
This cookbook is presented in four languages: English, Hebrew (עברית), Spanish (Español), and Tunisian Arabic (تونسي) with Hebrew transliteration, reflecting the multicultural heritage of our family and the diaspora communities that preserved these traditions.
\\end{culturalcontext}

% Include chapters
\\input{chapters/01-heritage.tex}
\\input{chapters/02-breads.tex}
\\input{chapters/03-sabbath.tex}
\\input{chapters/04-holidays.tex}
\\input{chapters/05-everyday.tex}
\\input{chapters/06-sweets.tex}
\\input{chapters/07-modern.tex}

% Appendices
\\appendix
\\chapter{Ingredient Glossary}
\\input{chapters/appendix-ingredients.tex}

\\chapter{Cultural Context}
\\input{chapters/appendix-culture.tex}

% Index
\\printindex

\\end{document}
'''
        
        with open('latex/main.tex', 'w', encoding='utf-8') as f:
            f.write(main_tex)
            
    def create_chapter_templates(self):
        """Create chapter template files"""
        chapters = {
            '01-heritage': 'Heritage and History',
            '02-breads': 'Daily Breads and Foundations', 
            '03-sabbath': 'Sabbath Specialties',
            '04-holidays': 'Holiday Traditions',
            '05-everyday': 'Everyday Comfort',
            '06-sweets': 'Sweet Traditions',
            '07-modern': 'Modern Innovations'
        }
        
        for file_prefix, title in chapters.items():
            chapter_content = f'''% Chapter: {title}
\\chapter{{{title}}}

% Chapter introduction will be added here
\\section*{{Heritage Context}}

This chapter contains recipes from the family tradition, carefully adapted for plant-based preparation while maintaining cultural authenticity.

% Individual recipes will be included here
% \\input{{recipes/english/recipe_name.tex}}

'''
            with open(f'latex/chapters/{file_prefix}.tex', 'w', encoding='utf-8') as f:
                f.write(chapter_content)
                
    def convert_markdown_to_latex(self, markdown_text, recipe_name, image_path=None):
        """Convert markdown recipe to LaTeX format"""
        # Basic markdown to LaTeX conversion
        latex_text = markdown_text
        
        # Convert headers
        latex_text = re.sub(r'^# (.*)', r'\\section*{\\1}', latex_text, flags=re.MULTILINE)
        latex_text = re.sub(r'^## (.*)', r'\\subsection*{\\1}', latex_text, flags=re.MULTILINE)
        latex_text = re.sub(r'^### (.*)', r'\\subsubsection*{\\1}', latex_text, flags=re.MULTILINE)
        
        # Convert bold text
        latex_text = re.sub(r'\\*\\*(.*?)\\*\\*', r'\\textbf{\\1}', latex_text)
        
        # Convert italic text
        latex_text = re.sub(r'\\*(.*?)\\*', r'\\textit{\\1}', latex_text)
        
        # Convert lists - this is a simplified version
        latex_text = re.sub(r'^- (.*)', r'\\item \\1', latex_text, flags=re.MULTILINE)
        latex_text = re.sub(r'^\\d+\\. (.*)', r'\\item \\1', latex_text, flags=re.MULTILINE)
        
        # Wrap lists in environments (simplified)
        if '\\item' in latex_text:
            latex_text = re.sub(r'(\\item.*?)(?=\\n\\n|\\n\\section|\\n\\subsection|$)', 
                              r'\\begin{itemize}\n\\1\n\\end{itemize}', 
                              latex_text, flags=re.DOTALL)
        
        # Add image if provided
        if image_path:
            relative_image_path = os.path.relpath(image_path, 'latex')
            image_latex = f'''\\begin{{center}}
\\includegraphics[width=0.8\\textwidth]{{{relative_image_path}}}
\\end{{center}}

'''
            latex_text = image_latex + latex_text
            
        return latex_text
    
    def generate_recipe_latex(self, recipe_data):
        """Generate LaTeX file for a single recipe"""
        recipe = recipe_data['recipe']
        safe_name = self.safe_filename(recipe['english_name'])
        
        # Generate English version
        english_latex = self.convert_markdown_to_latex(
            recipe_data['recipe_markdown'], 
            recipe['english_name'],
            recipe_data.get('image_path')
        )
        
        # Full recipe LaTeX with multilingual support
        full_latex = f'''% Recipe: {recipe['english_name']} ({recipe['hebrew_name']})
% Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

\\begin{{recipe}}{{{recipe['english_name']}}}

% Cultural context
\\begin{{culturalcontext}}
This recipe comes from the {recipe['source']} family line, representing the rich culinary heritage of {"Djerban" if "Cohen-Trabelsi" in recipe['source'] else "Moroccan"} Jewish cuisine.
\\end{{culturalcontext}}

% English version (primary)
\\recipesection{{English}}{{english}}
\\begin{{recipecard}}
{english_latex}
\\end{{recipecard}}

% Hebrew version
\\recipesection{{עברית (Hebrew)}}{{hebrew}}
\\begin{{recipecard}}
\\heb{{
% Hebrew translation will be inserted here
תרגום עברי של המתכון יוכנס כאן
}}
\\end{{recipecard}}

% Spanish version
\\recipesection{{Español (Spanish)}}{{spanish}}
\\begin{{recipecard}}
% Spanish translation will be inserted here
Traducción española se insertará aquí
\\end{{recipecard}}

% Arabic version
\\recipesection{{العربية (Arabic)}}{{arabic}}
\\begin{{recipecard}}
\\ar{{
% Arabic translation will be inserted here
الترجمة العربية ستدرج هنا
}}
\\end{{recipecard}}

\\end{{recipe}}
'''
        
        # Save recipe LaTeX file
        recipe_file = f'latex/recipes/english/{safe_name}.tex'
        with open(recipe_file, 'w', encoding='utf-8') as f:
            f.write(full_latex)
            
        return recipe_file
    
    def safe_filename(self, name):
        """Convert recipe name to safe filename"""
        if not name:
            return "unknown_recipe"
        safe = re.sub(r'[^\w\s-]', '', name)
        safe = re.sub(r'[-\s]+', '_', safe)
        safe = safe.strip('_')
        return safe.lower() if safe else "unknown_recipe"
    
    def create_build_script(self):
        """Create build script for LaTeX compilation"""
        build_script = '''#!/bin/bash
# LaTeX Build Script for Vegan Djerban Family Cookbook

echo "🔨 Building Vegan Djerban Family Cookbook..."

# Create output directory
mkdir -p latex/output

# Copy images to latex directory
echo "📸 Copying images..."
cp -R data/images/generated/* latex/images/ 2>/dev/null || true

# Build LaTeX document (requires XeLaTeX for Unicode fonts)
echo "📚 Compiling LaTeX document..."
cd latex

# First pass
xelatex -output-directory=output main.tex

# Second pass for references
xelatex -output-directory=output main.tex

# Third pass for final formatting
xelatex -output-directory=output main.tex

echo "✅ Build complete! Check latex/output/main.pdf"

# Open PDF if on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    open output/main.pdf
fi
'''
        
        with open('build_latex.sh', 'w') as f:
            f.write(build_script)
            
        # Make script executable
        os.chmod('build_latex.sh', 0o755)
        
    def generate_cookbook(self, recipe_results):
        """Generate complete LaTeX cookbook from recipe results"""
        print("📚 Generating LaTeX cookbook...")
        
        # Create LaTeX structure
        self.create_document_class()
        self.create_main_document()
        self.create_chapter_templates()
        self.create_build_script()
        
        # Generate individual recipe files
        generated_recipes = []
        for recipe_data in recipe_results:
            recipe_file = self.generate_recipe_latex(recipe_data)
            generated_recipes.append(recipe_file)
            
        print(f"✅ Generated {len(generated_recipes)} recipe LaTeX files")
        print("📝 LaTeX structure created")
        print("🔨 Run './build_latex.sh' to compile the cookbook")
        
        return generated_recipes

def main():
    """Test LaTeX generation"""
    generator = LaTeXGenerator()
    
    # Create basic structure for testing
    generator.create_document_class()
    generator.create_main_document() 
    generator.create_chapter_templates()
    generator.create_build_script()
    
    print("✅ LaTeX structure created successfully!")
    print("📁 Check the 'latex/' directory for generated files")

if __name__ == "__main__":
    main() 