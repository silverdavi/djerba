# Djerba-Tanjir Vegan Cookbook Project Plan

## Overview
A multilingual vegan cookbook featuring traditional recipes from two Tunisian regions:
- **Djerba** (David Silver's paternal side)
- **Tanjir** (Enny Silver's maternal side)

## Book Specifications
- **Languages**: Hebrew, English, Arabic, Spanish (4 languages total)
- **Format**: Double-page spread per recipe (2 pages each)
- **Focus**: Etymology and historical roots of dish names
- **Typography**: Professional LaTeX with beautiful fonts
- **Content**: Traditional vegan recipes with cultural context

## Project Structure

### 1. Recipe Organization
Current status: 35 recipes moved to individual folders
```
recipes/
├── 01_מחמסה/
│   ├── 1_original_hebrew.md
│   ├── 2_translations/
│   │   ├── english.md
│   │   ├── arabic.md
│   │   └── spanish.md
│   ├── 3_etymology_research.md
│   └── 4_recipe_data.json
├── 02_שמיד/
│   └── ... (same structure)
└── ... (35 recipes total)
```

### 2. Research Components
For each recipe, develop:

#### Etymology Research (`3_etymology_research.md`)
- **Root Analysis**: Arabic/Berber/Hebrew linguistic origins
- **Historical Context**: Cultural significance and regional variations
- **Transliteration**: Standardized romanization across languages
- **Regional Variations**: Djerba vs Tanjir differences
- **Cultural Notes**: Traditional preparation contexts, celebrations

#### Translation Process (`2_translations/`)
- **Hebrew → English**: Base translation with cultural notes
- **Hebrew → Arabic**: Maintaining regional dialect authenticity  
- **Hebrew → Spanish**: Considering Sephardic Jewish culinary connections
- **Consistency**: Unified terminology across languages

### 3. Data Structure (`4_recipe_data.json`)
```json
{
  "recipe_id": "01_מחמסה",
  "names": {
    "hebrew": "מחמסה",
    "english": "Mahmasah",
    "arabic": "محمصة", 
    "spanish": "Majmasá"
  },
  "etymology": {
    "root": "ح-م-ص (to roast/toast)",
    "origin": "Arabic",
    "meaning": "toasted/roasted dish",
    "variants": ["محمصة", "מחמסה"]
  },
  "ingredients": {
    "hebrew": [...],
    "english": [...],
    "arabic": [...],
    "spanish": [...]
  },
  "instructions": {
    "hebrew": [...],
    "english": [...], 
    "arabic": [...],
    "spanish": [...]
  },
  "cultural_context": {
    "region": "Djerba",
    "occasion": "daily meal",
    "season": "any",
    "history": "..."
  },
  "latex_formatting": {
    "chapter_title": "...",
    "page_layout": "double_spread",
    "image_placement": "right_page_top"
  }
}
```

### 4. LaTeX Structure
```
latex/
├── main.tex                 # Main document
├── preamble.sty            # Package imports and setup
├── cookbook.cls            # Custom document class
├── styles/
│   ├── fonts.sty           # Typography definitions
│   ├── colors.sty          # Color scheme
│   ├── layout.sty          # Page layout and spacing
│   └── multilingual.sty    # Language-specific formatting
├── chapters/
│   ├── 01_מחמסה.tex
│   ├── 02_שמיד.tex
│   └── ... (35 recipe chapters)
├── assets/
│   ├── images/             # Recipe photos, illustrations
│   ├── fonts/              # Custom font files
│   └── logos/              # Family/regional emblems
└── bibliography/
    ├── etymology.bib       # Linguistic sources
    └── cultural.bib        # Historical/cultural sources
```

## Implementation Phases

### Phase 1: Translation Pipeline
1. Set up automated translation workflow using LLMs
2. Translate all 35 recipes from Hebrew to English, Arabic, Spanish
3. Review and refine translations for cultural accuracy
4. Create standardized terminology glossary

### Phase 2: Etymology Research
1. Research linguistic origins for each dish name
2. Document historical context and regional variations
3. Create etymological database with cross-references
4. Develop transliteration standards for all languages

### Phase 3: Data Compilation
1. Structure all content into JSON format
2. Ensure consistency across languages
3. Add cultural context and historical notes
4. Prepare LaTeX formatting specifications

### Phase 4: LaTeX Development
1. Create custom document class for cookbook format
2. Design typography system supporting 4 scripts
3. Implement double-page layout templates
4. Set up automated chapter generation from JSON

### Phase 5: Content Integration
1. Generate LaTeX chapters from JSON data
2. Integrate etymology research into layout
3. Add cultural context sidebars
4. Fine-tune typography and spacing

### Phase 6: Final Production
1. Compile complete cookbook
2. Review and proofread all languages
3. Adjust layout and typography
4. Generate final PDF for publication

## Technical Tools
- **Translation**: OpenAI GPT-4.1, Perplexity for research
- **Etymology Research**: Academic databases, linguistic references
- **LaTeX**: XeLaTeX for multilingual support
- **Version Control**: Git for collaborative editing
- **Automation**: Python scripts for data processing

## Success Criteria
- All 35 recipes available in 4 languages
- Comprehensive etymology for each dish name
- Professional cookbook layout with cultural authenticity
- Publishable PDF meeting industry standards
- Preservation of family culinary heritage

## Timeline Estimate
- **Phase 1-2**: 2-3 weeks (Translation + Research)
- **Phase 3**: 1 week (Data compilation)
- **Phase 4**: 2 weeks (LaTeX development)
- **Phase 5-6**: 2 weeks (Integration + Final production)
- **Total**: ~7-8 weeks for complete cookbook 