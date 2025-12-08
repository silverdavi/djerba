# Recipe.app Downloads

This folder contains recipes downloaded from recipe.app for processing.

## Structure

```
recipe_app_downloads/
├── README.md (this file)
├── raw/                    # Raw exported recipes from recipe.app
│   ├── *.json
│   ├── *.csv
│   └── *.txt
├── processed/              # After deduplication & validation
│   └── *.json
└── IMPORT_LOG.md          # Log of what was imported
```

## Workflow

1. **Export from recipe.app**
   - Export your recipes as JSON/CSV from the recipe.app interface
   - Save to `raw/` folder

2. **Process & Validate**
   - Run: `python import_recipe_app_recipes.py raw/`
   - Validates structure
   - Deduplicates
   - Converts to standard format

3. **Review**
   - Check `processed/` folder
   - Check `IMPORT_LOG.md` for import results

4. **Integrate**
   - Copy to `data/recipes_multilingual/` or use in pipeline
   - Run through disambiguation module if needed

## How to Download from recipe.app

1. Open recipe.app
2. Go to Settings → Export
3. Select format: JSON (preferred) or CSV
4. Download all recipes
5. Save to `raw/` folder here

## Supported Formats

- **JSON**: Preferred format
  ```json
  {
    "id": "recipe-id",
    "name": "Recipe Name",
    "ingredients": ["ing1", "ing2"],
    "instructions": ["step1", "step2"],
    "metadata": {}
  }
  ```

- **CSV**: Will be converted to JSON
  - Columns: name, ingredients, instructions

## Import Status

- Recipes imported: 0
- Last import: Not yet
- Last update: [timestamp]

See `IMPORT_LOG.md` for details.

## Next Steps

1. [ ] Export recipes from recipe.app
2. [ ] Save to `raw/` folder
3. [ ] Run import script
4. [ ] Review processed recipes
5. [ ] Integrate into pipeline
