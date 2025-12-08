# recipe.app Quick Start

## Setup (One-time)

Already done! Folder structure is ready:
```
recipe_app_downloads/
├── raw/              ← Put exported recipes here
├── processed/        ← Import script saves here
├── README.md
├── IMPORT_LOG.md
└── import_recipe_app_recipes.py
```

## Download Recipes from recipe.app

1. **Open recipe.app** in your browser
2. **Settings → Export**
3. **Choose format:** JSON (recommended) or CSV
4. **Download** all recipes
5. **Save to:** `recipe_app_downloads/raw/`

## Import Recipes

```bash
cd recipe_app_downloads/
python import_recipe_app_recipes.py raw/
```

**Output:**
- `processed/*.json` - Imported recipes
- `IMPORT_LOG.md` - Import results

## What the Import Script Does

✅ Accepts JSON or CSV format  
✅ Validates recipe structure  
✅ Deduplicates (same recipe multiple times)  
✅ Generates IDs from recipe names  
✅ Logs all results  

## File Formats Supported

### JSON
```json
{
  "id": "recipe-id",
  "name": "Recipe Name",
  "ingredients": ["ingredient1", "ingredient2"],
  "instructions": ["step1", "step2"],
  "description": "Optional description",
  "servings": "4",
  "prep_time": "15 min",
  "cook_time": "30 min"
}
```

### CSV
```
name,ingredients,instructions,servings,prep_time,cook_time
"Recipe Name","ing1, ing2, ing3","step1, step2, step3","4","15 min","30 min"
```

## Next Steps

After importing, recipes are in `processed/` as JSON files.

### Option 1: Use in Djerba Pipeline
```bash
cp processed/*.json ../data/recipes_multilingual/
```

### Option 2: Process with Disambiguation
```python
from src.ingredient_disambiguator import RecipeDisambiguator
from pathlib import Path
import json

dis = RecipeDisambiguator()

for recipe_file in Path("processed").glob("*.json"):
    with open(recipe_file) as f:
        recipe = json.load(f)
    
    # Clarify ambiguous ingredients
    clarifications = dis.enhance_ingredient_list(
        ingredients=recipe['ingredients'],
        recipe_name=recipe['name']
    )
    print(f"{recipe['name']}: {len(clarifications)} clarified")
```

## Troubleshooting

### "ModuleNotFoundError: google.generativeai"
```bash
source ../my_venv/bin/activate  # Use the project venv
pip install google-generativeai
```

### Duplicate recipes not imported?
Check `IMPORT_LOG.md` - duplicates are logged but not saved (intentional)

### CSV not parsing correctly?
- Make sure CSV columns are: `name`, `ingredients`, `instructions`
- If using different column names, edit the import script

### Want to see what would be imported?
```bash
python import_recipe_app_recipes.py raw/ --dry-run
```
(Feature can be added if needed)

## Example Workflow

```bash
# 1. Export from recipe.app
#    (manually download and save to raw/)

# 2. Import recipes
cd recipe_app_downloads/
python import_recipe_app_recipes.py raw/

# 3. Check results
cat IMPORT_LOG.md

# 4. View imported recipes
ls processed/
cat processed/mhamsa.json | jq .

# 5. Integrate into pipeline
cp processed/*.json ../data/recipes_multilingual/
```

## See Also

- `recipe_app_downloads/README.md` - Full documentation
- `src/ingredient_disambiguator.py` - Disambiguation module
- `QUICK_START_DISAMBIGUATION.md` - Ingredient clarification
