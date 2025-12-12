# Canonical Recipe Schema

This is the **single source of truth** for all recipes in the cookbook.

## Design Principles

1. **One language (English)** for the canonical source
2. **Structured ingredients** with separate fields for amount, unit, ingredient
3. **Metric units** as canonical (ml, g) with rendering to locale-specific units
4. **Ingredient IDs** for consistent translation lookup
5. **Multilingual output** is generated from this, not stored here

## Schema

```json
{
  "id": "string",                    // Unique ID (lowercase, english, e.g., "mhamsa")
  "slug": "string",                  // URL-friendly slug
  "source_file": "string",           // Original source file for reference
  
  "name": "string",                  // English name of the dish
  "name_hebrew": "string",           // Original Hebrew name (for reference)
  "name_origin": "string",           // Etymology of the name
  
  "description": "string",           // 2-3 sentence description in English
  "cultural_context": "string",      // Djerban/Tunisian/Moroccan Jewish tradition notes
  "is_vegan": boolean,               // Whether recipe is vegan (or veganized)
  "vegan_adaptation_notes": "string | null",  // If adapted, notes on what was changed
  
  "meta": {
    "servings": "string",            // e.g., "4-6"
    "prep_time_minutes": number,     // Numeric for calculations
    "cook_time_minutes": number,
    "total_time_minutes": number,
    "difficulty": "easy | medium | hard"
  },
  
  "ingredients": [
    {
      "ingredient_id": "string",     // Canonical ID (e.g., "olive_oil")
      "name": "string",              // English name (e.g., "Olive oil")
      "amount": number | null,       // Original numeric value (null if "to taste")
      "unit": "string | null",       // Original unit: g, ml, unit, tsp, tbsp (null if "to taste")
      "preparation": "string | null", // e.g., "diced", "minced", "room temperature"
      "notes": "string | null",       // e.g., "(optional)", "for coating"
      "is_optional": boolean,
      "measurements": {              // Multi-unit representations for localization
        "metric": { "value": number, "unit": "g" | "ml" },
        "imperial": { "value": number, "unit": "oz" | "fl oz" },
        "volume": { "value": number, "unit": "cups" | "tbsp" | "tsp" },
        "original": { "value": number, "unit": "string" }
      }
    }
  ],
  
  "steps": [
    {
      "step": number,
      "instruction": "string",
      "time_minutes": number | null,  // If step has specific timing
      "tips": "string | null"
    }
  ],
  
  "variants": [                       // Optional: for recipes with variations
    {
      "name": "string",
      "description": "string",
      "steps": [/* same structure as main steps */]
    }
  ] | null,
  
  "image": {
    "filename": "string",
    "prompt": "string | null"         // Custom image generation prompt
  },
  
  "tags": ["string"],                 // e.g., ["shabbat", "holiday", "quick", "dessert"]
  "related_recipes": ["string"]       // IDs of related recipes
}
```

## Canonical Units

| Type | Canonical Unit | Notes |
|------|----------------|-------|
| Weight | `g` (grams) | Convert from oz, lb |
| Volume (large) | `ml` (milliliters) | Convert from cups |
| Volume (small) | `tsp`, `tbsp` | Keep as-is for small amounts |
| Count | `unit` | For whole items: "1 unit onion" |
| To taste | `null` | amount and unit both null |

## Unit Conversion Reference

For rendering to US units:
- 1 cup = 240 ml
- 1 tbsp = 15 ml
- 1 tsp = 5 ml
- 1 oz = 28.35 g
- 1 lb = 453.6 g

## Ingredient IDs

Use lowercase_snake_case:
- `olive_oil`
- `onion`
- `sweet_paprika`
- `chickpea_flour`

Full dictionary in `../ingredients_dictionary.json`

