# Image and Recipe Organization System

## Overview

The organization system provides a structured way to manage recipes and images with index numbers, organized folders, and archived old files.

## Indexing

All recipes and images are indexed with numbers (e.g., `001_adafina`, `002_admeshushah`) for easy sorting and reference. Recipes are sorted alphabetically by English name.

## Structure

```
data/
├── recipes_multilingual/
│   ├── 001_adafina.json
│   ├── 002_admeshushah.json
│   └── ...
├── images/
│   ├── index.json              # Index mapping recipe_id to image paths
│   ├── generated/              # Generated images (001_adafina_dish.png)
│   ├── current/                 # Organized images by recipe
│   │   ├── 001_adafina/
│   │   │   ├── dish.png
│   │   │   └── ingredients.png
│   │   └── ...
│   └── archive/                 # Old/mismatched images
└── recipes_multilingual_backup/ # Backup of original files
```

## Index Format

The `index.json` file maps recipe IDs (with index numbers) to their image information:

```json
{
  "001_adafina": {
    "recipe_id": "001_adafina",
    "dish_name": "Adafina",
    "dish_image": "001_adafina/dish.png",
    "ingredients_image": "001_adafina/ingredients.png",
    "last_updated": "2025-12-09T07:03:35.006973"
  }
}
```

## Usage

### Index Recipes and Images

Run the indexing script to:
1. Add index numbers to all recipe files (sorted by English name)
2. Rename corresponding images
3. Update recipe IDs inside JSON files
4. Create/update the index
5. Create backup of original files

```bash
python index_recipes.py
```

### Organize Images

Run the organization script to:
1. Create/update the index
2. Archive old images
3. Organize current images into structured folders

```bash
python organize_images.py
```

### Access Images in Code

```python
from pathlib import Path
import json

# Load index
index = json.load(open('data/images/index.json'))

# Get image path for a recipe (now with index)
recipe_id = "001_adafina"
image_path = Path('data/images/current') / recipe_id / 'dish.png'

# Or use the helper in build.py
from gen_book.build import get_image_path
image_path = get_image_path(recipe_id, base_path="../images/", use_absolute=False)
```

### In build.py

The `get_image_path()` function automatically:
- Checks the index for organized images
- Falls back to generated/ convention if needed
- Uses absolute paths for PDF generation
- Uses relative paths for web deployment

## Recipe-Specific Corrections

The image generation system now supports recipe-specific corrections to fix known issues:

### Adafina
- **Issue**: Potatoes shown as whole unpeeled
- **Fix**: Potatoes must be SLICED (cut into rounds or chunks)

### Apple Crumble
- **Issue**: Shown as soupy liquid
- **Fix**: Must be a BAKED DESSERT with CRISP CRUMBLE TOPPING, solid and sliceable

### Artichoke Mushroom Stew
- **Issue**: Mushrooms sliced, not dominant
- **Fix**: WHOLE portobello/baby mushrooms, MOST DOMINANT ingredient

These corrections are applied automatically during image generation via `_get_recipe_specific_corrections()`.

## Benefits

1. **Easy Reference**: Index provides quick lookup of all recipe images
2. **Organization**: Images organized by recipe in separate folders
3. **Archive**: Old images preserved but separated
4. **Flexibility**: System works with both organized and generated/ paths
5. **Corrections**: Recipe-specific fixes applied automatically

