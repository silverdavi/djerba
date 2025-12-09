# Recipe JSON Schema

Each recipe is stored as a JSON file in `recipes/` directory.

## Schema

```json
{
  "id": "string",           // Unique identifier, used for filename (e.g., "mhamsa")
  "image": "string",        // Image filename in images/ folder (e.g., "mhamsa.png")
  
  "meta": {
    "servings": "string",   // e.g., "4–6"
    "prep_time": "string",  // e.g., "10 min"
    "cook_time": "string",  // e.g., "20 min"
    "difficulty": "string"  // e.g., "Easy", "Medium", "Hard"
  },
  
  "name": {
    "he": "string",         // Hebrew name
    "es": "string",         // Spanish name
    "ar": "string",         // Arabic name
    "en": "string"          // English name
  },
  
  "description": {
    "he": "string",         // Hebrew description (includes etymology if desired)
    "es": "string",
    "ar": "string",
    "en": "string"
  },
  
  "image_prompt": "string (optional)",  // Custom image generation prompt override
                                        // If provided, this exact prompt will be used
                                        // instead of auto-generated prompt. Allows manual
                                        // correction of image generation issues.
  
  "ingredients": {
    "he": ["string", ...],  // List of ingredients in Hebrew
    "es": ["string", ...],
    "ar": ["string", ...],
    "en": ["string", ...]
  },
  
  "variants": [             // Array of cooking variants (e.g., dry vs saucy)
    {
      "name": {
        "he": "string",     // Variant name in Hebrew
        "es": "string",
        "ar": "string",
        "en": "string"
      },
      "steps": {
        "he": ["string", ...],  // Steps for this variant
        "es": ["string", ...],
        "ar": ["string", ...],
        "en": ["string", ...]
      }
    }
  ]
}
```

## Notes

1. **Languages**: All text fields use ISO 639-1 codes:
   - `he` = Hebrew (RTL)
   - `es` = Spanish (LTR)
   - `ar` = Arabic (RTL)
   - `en` = English (LTR)

2. **Variants**: Use when a recipe has multiple preparation methods (e.g., dry vs saucy). 
   - If only one method, still use `variants` array with one entry.
   - Steps are numbered sequentially across all variants in the output.

3. **Images**: Place in `images/` folder. Supported formats: PNG, JPG, WebP.

4. **Description**: Can include etymology, history, or cultural context merged into one paragraph.

## Example

See `recipes/mhamsa.json` for a complete example.

## Build

```bash
source venv/bin/activate
python build.py
```

Output:
- `output/web/` — Individual HTML pages + index
- `output/print/` — Combined HTML + PDF for printing

