# Silver Cooks - Project Plan

## Overview

**Goal**: A multilingual vegan cookbook preserving Djerban and Tangier Jewish family recipes.

**Family Heritage**:
- **Silver-Cohen-Trabelsi** — Djerban Jewish cuisine from Tunisia
- **Kadoch-Muyal** — Tangier Jewish cuisine from Morocco
- **Silver** — Modern vegan adaptations

**Languages**: Hebrew, English, Spanish, Tunisian Arabic

## Current Status

### Completed
- [x] 87 recipes collected, translated, and formatted (4 languages each)
- [x] AI image generation pipeline (Gemini 3 Pro)
- [x] 88 dish images generated and reviewed
- [x] 96 ingredient icons generated
- [x] Print-ready 8×8 inch PDF (WeasyPrint)
- [x] Web viewer at silvercooks.com (GitHub Pages)
- [x] Custom domain with HTTPS (Route53 + GitHub Pages)
- [x] Adaptive font sizing for recipe pages
- [x] Decorative ingredient icons on recipe pages
- [x] Book cover design (LaTeX)
- [x] Ingredient cross-reference matrix

### Pipeline Scripts

| Script | Purpose |
|--------|---------|
| `generate_cookbook_images.py` | Generate dish images with Gemini 3 Pro |
| `generate_ingredient_icons.py` | Generate ingredient icon PNGs |
| `generate_intro_paragraphs.py` | Generate introduction text |
| `canonize_recipes.py` | Standardize recipe format |
| `multilingualize_recipes.py` | Translate to 4 languages |
| `veganize_recipes.py` | Adapt recipes for plant-based |
| `gen_book/build.py` | Build web pages + print PDF |
| `gen_book/deploy_github.py` | Deploy to GitHub Pages |

### Data Flow

```
Source recipes (Hebrew/English)
    ↓
canonize_recipes.py → Standardized JSON
    ↓
veganize_recipes.py → Plant-based adaptations
    ↓
multilingualize_recipes.py → 4-language JSON
    ↓
generate_cookbook_images.py → Dish images
    ↓
gen_book/build.py → Web HTML + Print PDF
    ↓
gen_book/deploy_github.py → silvercooks.com
```

## Recipe Categories

| Category | Recipes |
|----------|---------|
| Stews & Mains | Adafina, Tfina, Cholent, Bkaila, Chraime, Tbikha, Ciceritos, Lentecha, Potache, Fricassee, Meatballs, Yellow Meat |
| Soups | Brodo, Hsou, Dwida, Kata'a, Couscous Soup, Green Pea Soup |
| Bread & Dough | Hallah, Khobz Dar, Sfenj, Sfingh, Mufleta, Fricassee Rolls, Brikot, Burekas |
| Couscous & Pasta | Couscous, Mhamsa, L'Intriya, Kugel |
| Salads & Sides | Marmouma, Tirshi, Msiyar, Charoset, Hummus Salad, Shlomit Salad, Kishke |
| Eggs & Omelets | Cujada, Shakshuka, Na'zha, Adamshusha, Ma'akouda, Vegan Egg Salad |
| Cakes & Sweets | Yoyo, Sufganiyot, Chocolate Cake, Honey Cake, Apple Crumble, Yeast Cake, Dolce de Leche, Mocha Java Cake, Nougat Cake, Hot Fudge Cake |
| Cookies & Bars | Biscotti, Granola Cookies, Chocolate Chip Cookies, Chocolate Peanut Bars |
| Modern | Shawarma, Schnitzel, Pizza, Vegan Fish, Caesar Dressing, Fried Rice, Cashew Cannelloni, Umami Mushrooms |
| Basics | Spice Mixes, Sourdough Bread, Pancakes, French Toast, Semolina Porridge, Bshisha |
