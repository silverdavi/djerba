# Usage Guide

## Build Pipeline

### 1. Build Cookbook

The main build script generates web pages, print HTML, and PDF:

```bash
source venv_new/bin/activate

# Build everything
python gen_book/build.py

# Web pages only (fastest, for iteration)
python gen_book/build.py --web-only

# Print PDF only (8×8 inch)
python gen_book/build.py --print-only

# Bleed PDF (8.5×8.5 inch, for professional printing)
python gen_book/build.py --bleed-only
```

**Output:**
- `gen_book/output/web/` — Individual recipe HTML pages
- `gen_book/output/print/full-cookbook.html` — Combined print HTML
- `gen_book/output/print/full-cookbook.pdf` — Print-ready PDF

### 2. Deploy to Website

```bash
python gen_book/deploy_github.py --push
```

This:
- Copies web pages, images, and viewer to `deploy/`
- Fixes image paths for web deployment
- Pushes to `silverdavi/silvercooks` on GitHub
- GitHub Pages serves at silvercooks.com

### 3. Generate Images

```bash
# Generate image for a single recipe
python -c "
import json
from generate_cookbook_images import CookbookImageGenerator
recipe = json.load(open('data/recipes_multilingual_v2/RECIPE_ID.json'))
gen = CookbookImageGenerator()
gen.generate_recipe_images(recipe, generate_dish=True, generate_ingredients=False)
"
```

Then copy to current:
```bash
cp data/images/generated/RECIPE_ID_dish.png data/images/current/RECIPE_ID/dish.png
```

### 4. Add a New Recipe

1. Create `data/recipes_multilingual_v2/my_recipe.json` with all 4 languages
2. Generate image (see above)
3. Copy image to `data/images/current/my_recipe/dish.png`
4. Update image path in JSON: `"image": "images/current/my_recipe/dish.png"`
5. Build: `python gen_book/build.py --web-only`
6. Deploy: `python gen_book/deploy_github.py --push`

## Cookbook Layout

Each recipe generates 4 pages in the print PDF:

| Page | Content |
|------|---------|
| 1 | Title (4 languages) + Description + Metadata |
| 2 | Full-bleed dish photograph |
| 3 | Spanish (left) + Hebrew (right) — ingredients & steps |
| 4 | English (left) + Arabic (right) — ingredients & steps |

### Fonts
- **English**: Sora (geometric sans-serif)
- **Spanish**: Fraunces (quirky serif)
- **Hebrew**: Heebo
- **Arabic**: Noto Naskh Arabic
- **Titles**: Bona Nova

### Design Features
- Adaptive font sizing per recipe (based on content length)
- Staggered column layout (LTR starts higher, RTL lower)
- Decorative ingredient icons in empty diagonal spaces
- Chapter numbers with oriental styling on title pages
- Ingredient mosaic on book title page

## DNS & Hosting

- **Domain**: silvercooks.com (Route53, AWS)
- **Hosting**: GitHub Pages (`silverdavi/silvercooks`)
- **DNS Records**: A records → GitHub Pages IPs, CNAME www → silverdavi.github.io
