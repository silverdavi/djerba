# Comprehensive Recipe Structure for Multilingual Cookbook

## Overview
Each recipe will be a complete, self-contained JSON object with all information needed for 4-language display. The book layout will feature floating text boxes (not flowing text) in Typst.

## Recipe JSON Structure

```json
{
  "id": "unique_recipe_id",
  "names": {
    "english": "Recipe Name in English",
    "hebrew": "שם המתכון בעברית",
    "arabic": "اسم الوصفة بالعربية",
    "spanish": "Nombre de la Receta en Español"
  },
  "metadata": {
    "category": "Main Course / Soup / Bread / etc",
    "serves": "4-6 people",
    "prep_time_minutes": 20,
    "cook_time_minutes": 30,
    "difficulty": "Easy / Medium / Difficult"
  },
  "ingredients": {
    "english": [
      {
        "name": "Ingredient name",
        "amount": "2",
        "unit": "cups"
      }
    ],
    "hebrew": [],
    "arabic": [],
    "spanish": []
  },
  "instructions": {
    "english": [
      {
        "step": 1,
        "text": "First step of preparation"
      }
    ],
    "hebrew": [],
    "arabic": [],
    "spanish": []
  },
  "etymology": {
    "english": {
      "name_meaning": "What the dish name means",
      "linguistic_roots": "Arabic/Hebrew/Berber origin",
      "historical_reference": "Any documented historical reference",
      "summary": "2-3 sentence summary of etymology"
    },
    "hebrew": {},
    "arabic": {},
    "spanish": {}
  },
  "history": {
    "english": {
      "origins": "Where and when the dish originated",
      "evolution": "How the dish evolved over time",
      "cultural_significance": "Why is it important?",
      "regional_variations": "How different regions prepare it",
      "summary": "3-4 sentence historical summary"
    },
    "hebrew": {},
    "arabic": {},
    "spanish": {}
  },
  "djerban_tradition": {
    "english": {
      "role_in_family": "How this dish is used in family traditions",
      "occasions": "When is it served? (Shabbat, holidays, etc)",
      "preparation_rituals": "Any special preparation traditions",
      "cultural_meaning": "What does it mean to the Djerban Jewish community?",
      "summary": "2-3 sentence summary of its place in Djerban tradition"
    },
    "hebrew": {},
    "arabic": {},
    "spanish": {}
  },
  "cooking_notes": {
    "english": {
      "tips": ["Tip 1", "Tip 2", "Tip 3"],
      "variations": ["Variation 1", "Variation 2"],
      "substitutions": ["Substitution 1", "Substitution 2"]
    },
    "hebrew": {},
    "arabic": {},
    "spanish": {}
  },
  "research_references": {
    "etymology_md": "filename of etymology research markdown",
    "history_md": "filename of history research markdown",
    "sources": ["Source 1", "Source 2", "Source 3"]
  }
}
```

## Key Sections Explained

### 1. **Names** (4 Languages)
- Complete recipe name in each language
- Will appear at top of recipe card in visual layout

### 2. **Metadata**
- Basic recipe information
- Category, serves, timing, difficulty level

### 3. **Ingredients** (4 Languages)
- Structured list with name, amount, unit
- Easy to display in columns
- Will be in floating text boxes

### 4. **Instructions** (4 Languages)
- Numbered steps
- Clear, concise language
- Will be in floating text boxes

### 5. **Etymology** (4 Languages)
- Name meaning
- Linguistic roots (Arabic/Hebrew/Berber origin)
- Historical references
- Short summary (2-3 sentences)
- **Source**: From Perplexity research files

### 6. **History** (4 Languages)
- Origins of the dish
- How it evolved
- Cultural significance
- Regional variations
- Short summary (3-4 sentences)
- **Source**: From Perplexity research files

### 7. **Djerban Tradition** (4 Languages)
- Role in family/community
- When it's served
- Preparation rituals/traditions
- Cultural meaning for Djerban Jewish community
- Short summary (2-3 sentences)

### 8. **Cooking Notes** (4 Languages)
- Practical tips for success
- Variations and substitutions
- Modern adaptations

### 9. **Research References**
- Link to original Perplexity research files
- Source citations
- For documentation/verification

## Visual Layout Strategy (Typst)

```
┌─────────────────────────────────────────┐
│  RECIPE NAME (ENGLISH)                  │
│  שם המתכון (HEBREW)                     │
│  اسم الوصفة (ARABIC)                    │
│  Nombre (SPANISH)                       │
├─────────────────────────────────────────┤
│                                         │
│  [FLOATING BOX 1]        [FLOATING BOX 2]
│  - Etymology             - History
│  - Name Meaning          - Origins
│  - Linguistic Roots      - Significance
│                                         │
│  [FLOATING BOX 3]        [FLOATING BOX 4]
│  - Ingredients           - Instructions
│  - Listed by lang        - Numbered steps
│                                         │
│  [FLOATING BOX 5]                       │
│  - Djerban Tradition                    │
│  - Role & Occasions                     │
│                                         │
└─────────────────────────────────────────┘
```

## Current Phase

1. ✅ Create comprehensive English recipe JSON structure
2. ✅ Populate with data from existing recipes + research
3. ✅ Validate structure with 3-5 sample recipes
4. Next: Translation pipeline for Hebrew, Arabic, Spanish
5. Next: Typst layout design with floating text boxes
6. Next: Compile final multilingual visual cookbook


