# Ingredient & Recipe Disambiguation Guide

## Overview

This guide explains how to handle ambiguous ingredients and recipe names in the Djerban cookbook pipeline, particularly for:

1. **Ambiguous ingredient mentions** (e.g., "pepper" could mean bell pepper, hot green pepper, or black pepper)
2. **Hebrew recipe names with implied vowels** (e.g., עג׳ה could be "Eeja" or "Aja")

---

## The Problem

### Ambiguous Ingredients

In the original Hebrew recipes, some ingredients are written without sufficient context to determine exactly which type they are:

**Example:** A recipe mentions "פלפל" (pepper)
- Could be: **bell pepper** (sweet, colorful chunks) - adds color/texture
- Could be: **hot green pepper** (spicy, thin long pepper) - adds heat
- Could be: **black pepper** (ground spice, tiny specks) - adds subtle spice

The visual appearance of the final dish depends heavily on which pepper is meant!

### Hebrew Vowel Ambiguity

Hebrew often omits vowels, and traditional Tunisian dish names may have multiple valid transliterations:

**Example:** עג׳ה (spelled: aleph-gimmel-ayin-heh)
- Could be: **"Eeja"** - a hearty lentil stew
- Could be: **"Aja"** - possibly a different dish variant

The context (ingredients, cooking technique, cultural tradition) helps resolve this.

---

## Solution: RecipeDisambiguator Class

Located in: `src/ingredient_disambiguator.py`

### Capabilities

#### 1. Clarify Ambiguous Ingredients

```python
from ingredient_disambiguator import RecipeDisambiguator

disambiguator = RecipeDisambiguator()

result = disambiguator.clarify_ingredient(
    ingredient="pepper",
    recipe_name="Harimi",
    other_ingredients=["tomatoes", "garlic", "olive oil", "tofu"]
)

print(result)
# {
#   "ingredient": "pepper",
#   "clarified": "hot green pepper",
#   "alternatives": ["bell pepper", "black pepper", "hot red pepper"],
#   "confidence": 0.75,
#   "reasoning": "In Tunisian cuisine, 'pepper' most commonly refers to long green hot peppers"
# }
```

#### 2. Clarify Ambiguous Recipe Names

```python
result = disambiguator.clarify_recipe_name(
    hebrew_name="עג׳ה",
    ingredients=["עדשים", "בצל", "שום", "שמן", "מים"]
)

print(result)
# {
#   "hebrew_name": "עג׳ה",
#   "canonical_name": "Eeja",
#   "transliterations": ["Eeja", "Aja", "Ajah"],
#   "description": "Traditional Tunisian lentil or bean stew...",
#   "color_profile": "Warm brown and reddish tones...",
#   "confidence": 0.85,
#   "reasoning": "Characteristic Djerban lentil dish..."
# }
```

#### 3. Enhance Full Ingredient Lists

```python
clarifications = disambiguator.enhance_ingredient_list(
    ingredients=["פפר חריף", "עגבניות", "פפר שחור", "שום"],
    recipe_name="Harimi"
)

print(clarifications)
# {
#   "פפר חריף": "hot red pepper",
#   "פפר שחור": "black pepper"
# }
```

---

## How It Works

### Strategy 1: Knowledge Base Lookup

For common ambiguous ingredients/recipes with well-established interpretations:

```python
# For "pepper" in Tunisian cuisine
if ingredient.lower() == "pepper":
    return {
        'clarified': 'hot green pepper',
        'confidence': 0.75,
        'reasoning': 'Most common in Tunisian cooking'
    }

# For עג׳ה (Eeja)
if 'עג' in hebrew_name:
    return {
        'canonical_name': 'Eeja',
        'description': 'Lentil or bean stew...',
        'confidence': 0.85,
        'reasoning': 'Characteristic Djerban dish'
    }
```

### Strategy 2: Gemini API Fallback

For unknown ingredients/recipes, the disambiguator uses Gemini 3 Pro to:
1. Analyze the ingredient in recipe context
2. Return JSON with clarified type, alternatives, and confidence score
3. Fall back to knowledge base if API fails

```python
# If not in knowledge base:
# 1. Call Gemini API with safe prompts
# 2. Parse JSON response
# 3. Return result with confidence score
```

---

## Known Ambiguous Ingredients

Based on the `COLOR_INGREDIENTS` dictionary in `generate_cookbook_images.py`, these ingredients are already well-distinguished:

### Pepper/Hot Peppers
- `'bell pepper'` → chunky sweet pepper pieces (0.8 intensity)
- `'hot pepper'` → bright red/green chili (1.0 intensity)
- `'hot green pepper'` → long bright green chili (1.0 intensity)
- `'hot red pepper'` → long bright red chili (1.2 intensity)
- `'black pepper'` → tiny dark specks (0.3 intensity)

### Tomatoes
- `'tomato'` → tomato red (1.0 intensity)
- `'tomato paste'` → deep concentrated red (2.5 intensity)
- `'sun-dried tomatoes'` → deep burgundy red (1.4 intensity)

### Herbs vs Vegetables
- `'parsley'` → fresh green herb flecks (0.6 intensity)
- `'spinach'` → deep green leaves (1.5 intensity)
- `'green beans'` → vibrant green beans (1.0 intensity)

---

## Known Ambiguous Hebrew Recipes

### עג׳ה (Eeja/Aja)
- **Canonical Name:** Eeja
- **Transliterations:** Eeja, Aja, Ajah
- **Description:** Traditional Tunisian lentil or bean stew
- **Visual:** Warm brown and reddish tones with visible legumes
- **Confidence:** 0.85

### דביח (Dbeekh/Dbaakh)
- **Canonical Name:** Dbeekh
- **Transliterations:** Dbeekh, Dbaakh, Dbeikh
- **Description:** Traditional savory stew, can be plain or festive
- **Visual:** Rich brown savory stew with tender vegetables
- **Confidence:** 0.85

---

## Integration with Pipeline

### Option 1: Manual Pre-Processing

Before running the recipe transformation pipeline, clarify ambiguous ingredients:

```python
# In transform_recipes_gemini.py or your preprocessing step
from src.ingredient_disambiguator import RecipeDisambiguator

disambiguator = RecipeDisambiguator()

# For each recipe
recipe_data = load_recipe("safed_recipes/00_מחמסה.json")

# Clarify ambiguous ingredients
enhanced_ingredients = []
for ingredient in recipe_data['ingredients']:
    result = disambiguator.clarify_ingredient(
        ingredient=ingredient,
        recipe_name=recipe_data.get('name_hebrew', ''),
        other_ingredients=recipe_data['ingredients']
    )
    # Use clarified ingredient for veganization & translation
    enhanced_ingredients.append(result['clarified'])

recipe_data['ingredients'] = enhanced_ingredients
```

### Option 2: Integrate into Image Generation

Use disambiguated ingredients for more accurate color analysis:

```python
# In generate_cookbook_images.py
from src.ingredient_disambiguator import RecipeDisambiguator

class CookbookImageGenerator:
    def __init__(self):
        self.disambiguator = RecipeDisambiguator()
        self.appearance_analyzer = AppearanceAnalyzer()
    
    def generate_dish_image(self, dish_name, ingredients, output_path):
        # Clarify ambiguous ingredients first
        clarified_ingredients = []
        for ing in ingredients:
            result = self.disambiguator.clarify_ingredient(
                ingredient=ing,
                recipe_name=dish_name,
                other_ingredients=ingredients
            )
            if result['confidence'] >= 0.5:
                clarified_ingredients.append(result['clarified'])
            else:
                clarified_ingredients.append(ing)
        
        # Use clarified ingredients for color analysis
        appearance = self.appearance_analyzer.analyze_ingredients(
            clarified_ingredients
        )
        # ... generate image with accurate colors ...
```

### Option 3: Standalone CLI

```bash
# Run disambiguation on a recipe file
python src/ingredient_disambiguator.py --recipe-file safed_recipes/00_מחמסה.json

# Or test specific ingredient
python src/ingredient_disambiguator.py --test-ingredient "pepper" --recipe "Harimi"
```

---

## Confidence Scores

The disambiguator returns a confidence score (0.0-1.0):

| Score Range | Meaning | Action |
|---|---|---|
| 0.85-1.0 | Very high confidence | Use directly in pipeline |
| 0.70-0.84 | High confidence | Use with minor verification |
| 0.50-0.69 | Medium confidence | Consider alternatives for critical cases |
| < 0.50 | Low confidence | Requires manual review |

---

## Adding New Ambiguous Ingredients

To extend the knowledge base in `ingredient_disambiguator.py`:

```python
class RecipeDisambiguator:
    AMBIGUOUS_INGREDIENTS = {
        'your_ingredient': {
            'alternatives': ['option1', 'option2', 'option3'],
            'common_tunisian': ['most_likely_option'],
        },
        # ... more entries ...
    }
    
    HEBREW_DISH_VARIANTS = {
        'hebrew_letters': {
            'variants': ['English1', 'English2'],
            'description_en': 'What it is',
            'color_profile': 'Visual appearance',
        },
        # ... more entries ...
    }
```

Then update the `clarify_ingredient()` or `clarify_recipe_name()` methods to handle your new entries.

---

## API Behavior

The disambiguator uses Gemini 3 Pro API with these safeguards:

1. **Simple, direct prompts** to avoid safety filters
2. **Temperature 0.1-0.2** for consistent, deterministic responses
3. **Retry logic** with up to 3 attempts on failure
4. **Knowledge base fallback** if API is blocked or unavailable
5. **Graceful degradation** - returns confidence score of 0.0 if disambiguation fails

---

## Example: Full Workflow

```python
from src.ingredient_disambiguator import RecipeDisambiguator
import json

# Initialize
disambiguator = RecipeDisambiguator()

# Load recipe
with open('data/safed_recipes/05_דביח_חגים.json') as f:
    recipe = json.load(f)

print(f"Recipe: {recipe['name_hebrew']}")
print(f"Original ingredients: {recipe['ingredients']}")

# Clarify recipe name
name_result = disambiguator.clarify_recipe_name(
    hebrew_name=recipe['name_hebrew'],
    ingredients=recipe['ingredients']
)
print(f"\nRecipe clarification:")
print(f"  English name: {name_result['canonical_name']}")
print(f"  Color profile: {name_result['color_profile']}")
print(f"  Confidence: {name_result['confidence']}")

# Clarify ingredients
print(f"\nIngredient clarifications:")
for ingredient in recipe['ingredients'][:3]:
    result = disambiguator.clarify_ingredient(
        ingredient=ingredient,
        recipe_name=recipe['name_hebrew'],
        other_ingredients=recipe['ingredients']
    )
    if result['confidence'] >= 0.5:
        print(f"  '{ingredient}' → '{result['clarified']}' ({result['confidence']*100:.0f}%)")
```

---

## Performance Notes

- **Knowledge base lookups:** Instant (< 10ms)
- **API calls:** ~2 seconds per ingredient (depends on API latency)
- **Recommended:** Use knowledge base first, API only for unknowns
- **Batch processing:** For large recipe sets, cache results to avoid redundant API calls

---

## Troubleshooting

### API Calls Are Being Blocked

The Gemini API may block requests if:
- Prompt mentions cooking "ingredients" in certain contexts
- Text triggers safety filters

**Solution:** The disambiguator uses simplified, direct prompts and knowledge base fallbacks.

### Confidence Score is 0.0

This means the disambiguator couldn't clarify the ingredient/recipe. Check:
1. Is the ingredient/recipe in the knowledge base?
2. Is the API key valid?
3. Is the API accessible?

Use the clarified response's reasoning field for context.

### Hebrew Text Not Working

Ensure:
- File encoding is UTF-8
- Hebrew characters are passed as Unicode strings (Python 3+)
- Gemini API key has access

---

## Future Enhancements

1. **User feedback loop** - Learn from corrections to improve confidence scores
2. **Image-based disambiguation** - Use photos to confirm ingredient types
3. **Multi-language support** - Arabic and Spanish disambiguation
4. **Numeric quantity analysis** - Use ingredient amounts to refine guesses

---

## See Also

- `generate_cookbook_images.py` - Color ingredient mapping
- `transform_recipes_gemini.py` - Main recipe transformation pipeline
- `PIPELINE_GUIDE.md` - Overall pipeline documentation
