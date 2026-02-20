# Silver Cooks - Four-Language Vegan Cookbook

A plant-based cookbook preserving recipes from two North African Jewish family lines, presented in four languages: **Hebrew**, **Arabic**, **Spanish**, and **English**.

## Live Site

**[silvercooks.com](https://silvercooks.com)**

## Family Heritage

- **Cohen-Trabelsi** — Djerban Jewish cuisine from Tunisia (David's maternal line)
- **Kadoch-Muyal** — Tangier Jewish cuisine from Morocco (Enny's maternal line)

All recipes have been adapted for plant-based cooking while preserving authentic flavors and cultural context.

## Project Stats

- **87 recipes** in 4 languages
- **88 dish images** (AI-generated, Gemini 3 Pro)
- **96 ingredient icons** (transparent PNG)
- **8×8 inch print-ready PDF** with WeasyPrint
- **Web viewer** at silvercooks.com (GitHub Pages)

## Project Structure

```
RecipeDjerba/
├── data/
│   ├── recipes_multilingual_v2/    # 87 recipe JSONs (4 languages each)
│   └── images/
│       ├── current/                # Final dish images (per recipe)
│       └── ingredients/            # 96 ingredient icons
├── gen_book/
│   ├── build.py                    # Main build script (web + print + PDF)
│   ├── cookbook.css                 # Print/web styling
│   ├── deploy_github.py            # Deploy to GitHub Pages
│   ├── flipbook/                   # Web viewer (viewer.js/css)
│   └── output/                     # Generated HTML + PDF
├── book_cover/                     # Cover design (LaTeX)
├── generate_cookbook_images.py      # Image generation (Gemini 3 Pro)
├── generate_ingredient_icons.py    # Ingredient icon generation
├── generate_intro_paragraphs.py    # Introduction text generation
├── canonize_recipes.py             # Recipe standardization
├── multilingualize_recipes.py      # 4-language translation
├── veganize_recipes.py             # Veganization pipeline
└── recipes_ingredients_matrix.csv  # Ingredient cross-reference
```

## Quick Start

### Setup

```bash
python3 -m venv venv_new
source venv_new/bin/activate
pip install -r requirements.txt
pip install weasyprint perplexipy google-genai
```

### Build

```bash
# Build everything (web + print HTML + PDF)
python gen_book/build.py

# Build web pages only (fast)
python gen_book/build.py --web-only

# Build print PDF only
python gen_book/build.py --print-only
```

### Deploy to silvercooks.com

```bash
python gen_book/deploy_github.py --push
```

### Add New Recipes

1. Create recipe JSON in `data/recipes_multilingual_v2/` (4 languages)
2. Generate image: use `generate_cookbook_images.py`
3. Copy image to `data/images/current/{recipe_id}/dish.png`
4. Rebuild: `python gen_book/build.py`
5. Deploy: `python gen_book/deploy_github.py --push`

## Recipe JSON Format

Each recipe is a JSON file with this structure:

```json
{
  "id": "recipe_id",
  "image": "images/current/recipe_id/dish.png",
  "meta": {
    "servings": "4",
    "prep_time": "15 min",
    "cook_time": "30 min",
    "difficulty": "Easy"
  },
  "name": { "he": "...", "es": "...", "ar": "...", "en": "..." },
  "description": { "he": "...", "es": "...", "ar": "...", "en": "..." },
  "ingredients": { "he": [...], "es": [...], "ar": [...], "en": [...] },
  "steps": { "he": [...], "es": [...], "ar": [...], "en": [...] }
}
```

## API Keys

Required in `.env`:

```
GEMINI_API_KEY=...      # Image generation (Gemini 3 Pro)
PERPLEXITY_API_KEY=...  # Recipe research
```

## Authors

David & Enny Silver
