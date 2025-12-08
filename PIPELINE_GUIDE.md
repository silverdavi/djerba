# Djerban Jewish Vegan Cookbook Pipeline

A comprehensive pipeline for transforming traditional Tunisian-Djerban Jewish recipes into **vegan**, **multilingual** (Hebrew, Arabic, Spanish, English) cookbook content with AI-generated dish images.

---

## 📁 Project Structure

```
RecipeDjerba/
├── data/
│   ├── safed_recipes/              # INPUT: 34 original Hebrew recipes
│   │   ├── 00_מחמסה.json
│   │   ├── 01_שמיד.json
│   │   └── ...
│   │
│   ├── recipe_research/            # Historical/etymology research files
│   │   ├── mahmessa_history.md
│   │   ├── couscous_history.md
│   │   └── ...
│   │
│   ├── recipes_multilingual/       # OUTPUT: Vegan 4-language JSON files
│   │   ├── mhamsa.json
│   │   ├── harimi.json
│   │   ├── couscous.json
│   │   └── ... (30 recipes)
│   │
│   └── images/
│       └── generated/              # OUTPUT: AI-generated dish images
│           ├── mhamsa.png
│           ├── harimi.png
│           └── ... (30 images, ~3MB each, 2K resolution)
│
├── transform_recipes_gemini.py     # MAIN PIPELINE SCRIPT
├── generate_cookbook_images.py     # Image generation module
├── bkp_old/                        # Archived old files
└── .env                            # API keys (GOOGLE_API_KEY)
```

---

## 🔄 Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RECIPE TRANSFORMATION                        │
└─────────────────────────────────────────────────────────────────────┘

   INPUT                    STEP 1                   STEP 2                   OUTPUT
┌───────────┐          ┌─────────────┐          ┌─────────────┐          ┌───────────┐
│  Hebrew   │    🌱    │   Vegan     │    🌍    │ 4-Language  │    📸    │   JSON +  │
│  Recipe   │ ───────► │   Hebrew    │ ───────► │   Recipe    │ ───────► │   Image   │
│  (JSON)   │          │   Recipe    │          │   (JSON)    │          │   (PNG)   │
└───────────┘          └─────────────┘          └─────────────┘          └───────────┘
     │                       │                        │                        │
     │                       │                        │                        │
     ▼                       ▼                        ▼                        ▼
data/safed_recipes/    Gemini 3 Pro            Gemini 3 Pro          data/recipes_multilingual/
00_מחמסה.json          veganizes               translates            mhamsa.json
                       ingredients              to HE/AR/ES/EN        + images/generated/mhamsa.png
```

---

## 📥 Input Format

Each input recipe in `data/safed_recipes/` is a simple Hebrew JSON:

```json
{
  "name_hebrew": "חרימי",
  "ingredients": [
    "דגים",
    "שמן",
    "שום",
    "פפריקה חריפה",
    "2 כפות רסק עגבניות",
    "מיץ לימון"
  ],
  "instructions": [
    "לשים בסיר את השמן ולהוסיף את כל החומרים...",
    "להוסיף את המים והדגים..."
  ],
  "metadata": {
    "source_file": "safed_some.md"
  },
  "id": "חרימי"
}
```

---

## 📤 Output Format

The pipeline produces comprehensive multilingual JSON files matching this template:

```json
{
  "id": "harimi",
  "image": "harimi.png",
  "meta": {
    "servings": "3–4",
    "prep_time": "15 min",
    "cook_time": "25 min",
    "difficulty": "Easy"
  },
  "name": {
    "he": "חרימי",
    "es": "El Harimi",
    "ar": "الحرايمي",
    "en": "Harimi"
  },
  "description": {
    "he": "תבשיל אדום חריף וחמצמץ, עשיר בשום וקימל, המוגש כאן עם טופו במקום הדג המסורתי...",
    "es": "Un guiso rojo picante y ácido, rico en ajo y alcaravea...",
    "ar": "مرقة حمراء حارة وقارصة، غنية بالثوم والكروية...",
    "en": "A spicy, tangy red stew rich in garlic and caraway..."
  },
  "ingredients": {
    "he": ["1 חבילת טופו מוצק", "6 שיני שום כתושות", "..."],
    "es": ["1 bloque de tofu firme", "6 dientes de ajo machacados", "..."],
    "ar": ["1 قالب توفو", "6 سنون ثوم مرحي", "..."],
    "en": ["1 block firm tofu", "6 cloves garlic, crushed", "..."]
  },
  "steps": {
    "he": ["מחממים שמן בסיר...", "מוסיפים את הטופו..."],
    "es": ["Calentar aceite...", "Añadir el tofu..."],
    "ar": ["سخّن الزيت في الطنجرة...", "حط التوفو..."],
    "en": ["Heat oil in a pot...", "Add tofu..."]
  }
}
```

### Recipes with Variants

Some recipes have multiple preparation methods (e.g., dry vs. sauce):

```json
{
  "id": "mhamsa",
  "variants": [
    {
      "name": {"he": "מחמסה יבשה", "en": "Dry Mhamsa", ...},
      "steps": {"he": [...], "es": [...], "ar": [...], "en": [...]}
    },
    {
      "name": {"he": "מחמסה ברוטב", "en": "Mhamsa with Sauce", ...},
      "steps": {"he": [...], "es": [...], "ar": [...], "en": [...]}
    }
  ]
}
```

---

## 🌱 Vegan Substitutions

The pipeline automatically converts traditional ingredients:

| Original | Vegan Substitute | Hebrew |
|----------|------------------|--------|
| **Meat** (beef, lamb, chicken) | Soy protein / Seitan / Tofu | סויה מפוררת / סייטן / טופו |
| **Fish** | Smoked tofu / Seaweed-based | טופו מעושן |
| **Sausage** | Vegan sausage | נקניקיות טבעוניות |
| **Egg** (in cakes) | Apple sauce | רסק תפוחים |
| **Egg** (meringue) | Aquafaba | אקווה פאבה (מי חומוס) |
| **Egg** (binder in pastries) | Chickpea flour + water | קמח חומוס + מים |
| **Egg** (coating) | Chickpea flour batter | בלילת קמח חומוס |
| **Butter** | Coconut oil / Vegan margarine | שמן קוקוס |
| **Meat broth** | Vegetable broth | ציר ירקות |

---

## 🚀 Running the Pipeline

### Prerequisites

```bash
# Activate virtual environment
source my_venv/bin/activate

# Required packages
pip install google-generativeai python-dotenv

# API key in .env
GOOGLE_API_KEY=your_gemini_api_key
```

### Commands

```bash
# List all available recipes
python transform_recipes_gemini.py --list

# Process a single recipe (JSON only)
python transform_recipes_gemini.py --single "00_מחמסה.json"

# Process a single recipe with image generation
python transform_recipes_gemini.py --single "00_מחמסה.json" --with-images

# Process all recipes (JSON only)
python transform_recipes_gemini.py

# Process all recipes with images
python transform_recipes_gemini.py --with-images

# Process specific range
python transform_recipes_gemini.py --start 10 --limit 5 --with-images
```

### Output

```
🍳 Processing 34 recipes...
   Model: gemini-3-pro-preview
   Output: data/recipes_multilingual/
   Images: data/images/generated/

[1/34] Processing: 00_מחמסה.json
  Processing: מחמסה
  🌱 Veganizing: מחמסה
    ✅ Veganized successfully
  🌍 Translating to 4 languages...
    📚 Found historical research
    ✅ Saved: mhamsa.json
🎨 Generating image: mhamsa.png
   Prompt preview: Create a stunning photograph of Mhamsa...
✅ Image saved: data/images/generated/mhamsa.png
    🖼️  Image saved: mhamsa.png
```

---

## 🖼️ Image Generation

Images are generated using **Gemini 3 Pro Image** with these specifications:

| Setting | Value |
|---------|-------|
| **Aspect Ratio** | 1:1 (square) |
| **Resolution** | 2K (~3MB per image) |
| **Style** | Professional food photography |
| **Lighting** | Natural soft window light |
| **Composition** | Top-down or 45° angle |

### Standalone Image Generation

```bash
# Test generation
python generate_cookbook_images.py --test

# Generate from recipe JSON
python generate_cookbook_images.py --recipe-json data/recipes_multilingual/harimi.json

# Generate specific dish
python generate_cookbook_images.py --dish "Couscous" --description "Traditional steamed semolina"
```

---

## 🌍 Language Details

### Hebrew (he)
- Modern Israeli Hebrew
- Preserves Tunisian/Djerban terminology

### Arabic (ar)
- **Tunisian Derja dialect** (not Modern Standard Arabic)
- Uses local cooking terms: طنجرة (pot), مرقة (broth), نفوّح (season), كأس (cup)

### Spanish (es)
- Natural Latin American Spanish
- Sephardic influences where appropriate

### English (en)
- Clear, accessible American English
- Cultural terms preserved with explanations

---

## 📚 Historical Research

The pipeline uses research files from `data/recipe_research/` to enrich descriptions:

```markdown
# HARIMI - HISTORY

**Hebrew Name:** חרימי

### Historical Origins
Harimi is a signature dish of the Jewish communities of Djerba...

### Etymology
The name derives from the Arabic root h-r-m (sacred or forbidden)...

### Cultural Significance
Traditionally served on Shabbat evenings and festivals...
```

If research exists, it's incorporated into the description. Otherwise, the AI generates context from culinary knowledge.

---

## 🔧 Technical Details

### Models Used
- **Text Generation**: `gemini-3-pro-preview`
- **Image Generation**: `gemini-3-pro-image-preview`

### Pipeline Steps

1. **Load** Hebrew recipe from `data/safed_recipes/`
2. **Veganize** (Hebrew → Vegan Hebrew) with retry logic
3. **Load** historical research if available
4. **Translate** to 4 languages with cultural context
5. **Save** JSON to `data/recipes_multilingual/`
6. **Generate** dish image (if `--with-images`)
7. **Save** PNG to `data/images/generated/`

### Error Handling
- Retry up to 3 times on API failures
- Fallback to original recipe if veganization fails
- JSON parse error recovery
- Rate limiting (2s delay between recipes)

---

## 📊 Current Status

| Metric | Count |
|--------|-------|
| Total recipes | 34 |
| Successfully processed | 30 |
| Images generated | 30 |
| Failed (retry needed) | 4 |

### Failed Recipes (JSON parse errors)
- `00_מחמסה.json` - Mhamsa
- `16_סופגניות.json` - Sufganiyot
- `19_שקשוקה_של_בצל_מטוגן_ארוך.json` - Onion Shakshuka
- `30_אדמשושה.json` - Admeshusha

To retry failed recipes:
```bash
python transform_recipes_gemini.py --single "00_מחמסה.json" --with-images
```

---

## 📁 Backup

Old/superseded files are archived in `bkp_old/`:
- `bkp_old/data/` - Old recipe formats
- `bkp_old/latex/` - Previous LaTeX cookbook attempt
- `bkp_old/typst/` - Previous Typst cookbook attempt
- `bkp_old/root_files/` - Old scripts and documentation

