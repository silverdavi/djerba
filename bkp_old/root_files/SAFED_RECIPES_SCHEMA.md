# Safed Recipe Data Schema

This document defines the JSON schema for recipes parsed from `safed_some.md`.

## JSON Structure

Each recipe is stored in a separate `.json` file.

```json
{
  "id": "string (unique identifier, slugified English name or transliteration)",
  "name_hebrew": "string (The name as it appears in the source)",
  "ingredients": [
    "string (ingredient line 1)",
    "string (ingredient line 2)"
  ],
  "instructions": [
    "string (step 1)",
    "string (step 2)"
  ],
  "metadata": {
    "source_file": "safed_some.md",
    "original_text_block": "string (raw text for reference)"
  }
}
```

## Fields Description

- **id**: A URL-safe unique identifier derived from the recipe name. If English name isn't available, a transliteration or hash is used.
- **name_hebrew**: The raw Hebrew name extracted from the line starting with `**שם המתכון:` or `שם המתכון:`.
- **ingredients**: A list of strings, each representing a line from the `רשימת מצרכים:` section. Empty lines are ignored.
- **instructions**: A list of strings, each representing a line from the `אופן ההכנה:` section. Empty lines are ignored.
- **metadata**:
    - `source_file`: The filename the recipe was parsed from.
    - `original_text_block`: The raw text block corresponding to this recipe, useful for debugging or re-parsing.

