# Vegan Djerban Family Cookbook - Usage Guide

## Overview

The cookbook generation pipeline has been separated into two main components:
1. **Markdown Generation** - AI-powered content creation (recipes, research, translations, images)
2. **LaTeX Generation** - PDF compilation (will be addressed later)

## Quick Start

### 1. Markdown Generation (Core AI Pipeline)

Generate recipes, research, translations, and images:

```bash
# Run the master pipeline (default: markdown only)
python master_pipeline.py --markdown-only

# Or run the cookbook pipeline directly
python cookbook_pipeline.py --test 2
```

### 2. Available Options

#### Master Pipeline Commands

```bash
# Generate markdown content only (recommended)
python master_pipeline.py --markdown-only

# Generate LaTeX structure only (after markdown exists)
python master_pipeline.py --latex-only

# Run complete pipeline (markdown + LaTeX)
python master_pipeline.py --full
```

#### Cookbook Pipeline Commands

```bash
# Test with default 2 recipes
python cookbook_pipeline.py

# Test with specific number of recipes
python cookbook_pipeline.py --test 5

# Process all recipes (full pipeline)
python cookbook_pipeline.py --full

# Process specific recipe by name
python cookbook_pipeline.py --recipe "Mhamsa"
```

## Generated Content

After running the markdown pipeline, you'll find:

### Recipe Content
- `data/recipes/markdown/` - Main recipe files in markdown format
- `data/recipes/translations/` - Hebrew, Spanish, and Arabic translations

### Research Files
- `data/research/` - Cultural etymology and veganization research
  - `*_etymology.txt` - Cultural and historical research
  - `*_vegan.txt` - Veganization strategies  
  - `*_synthesis.txt` - Combined research synthesis

### Images
- `data/images/generated/` - AI-generated food photography

### Progress Tracking
- `data/pipeline_progress.json` - Processing status and error logs

## API Requirements

Ensure you have these API keys in your `.env` file:

```env
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_google_key_here  
PERPLEXITY_API_KEY=your_perplexity_key_here
```

## Processing Pipeline

Each recipe goes through these steps:

1. **Etymology Research** (Perplexity) - Cultural and historical context
2. **Veganization Research** (Perplexity) - Plant-based adaptation strategies
3. **Research Synthesis** (Gemini) - Combine research into structured report
4. **Recipe Generation** (GPT-4o) - Create complete vegan recipe
5. **Translation** (GPT-4o) - Hebrew, Spanish, and Arabic versions
6. **Image Generation** (DALL-E) - Professional food photography

## Family Heritage Lines

The pipeline processes recipes from three family lines:

- **Silver-Cohen-Trabelsi** - Djerban Jewish cuisine from Tunisia
- **Silver-Kadoch-Muyal** - Tangier Jewish cuisine from Morocco  
- **Silver** - Modern vegan adaptations

## Example Output

A processed recipe includes:

```
data/recipes/markdown/mhamsa.md
data/recipes/translations/mhamsa_hebrew.md
data/recipes/translations/mhamsa_spanish.md
data/recipes/translations/mhamsa_arabic.md
data/research/mhamsa_etymology.txt
data/research/mhamsa_vegan.txt
data/research/mhamsa_synthesis.txt
data/images/generated/mhamsa.png
```

## Troubleshooting

### Common Issues

1. **API Key Errors**: Check your `.env` file has all required keys
2. **Rate Limiting**: The pipeline includes delays between API calls
3. **Network Issues**: Research steps require internet connectivity

### Error Recovery

- Check `data/pipeline_progress.json` for detailed error logs
- Failed recipes can be reprocessed individually using `--recipe` flag
- The pipeline saves progress after each recipe

## Next Steps

Once markdown generation is working smoothly:

1. Review generated recipes for accuracy
2. Check translations for cultural authenticity  
3. Verify image quality and relevance
4. Address LaTeX compilation separately when ready

## Cultural Preservation

This pipeline preserves:
- ✅ Traditional cooking techniques adapted for plant-based ingredients
- ✅ Cultural context and family stories
- ✅ Hebrew terminology and transliterations
- ✅ Regional differences (Tunisian vs Moroccan Jewish cuisine)
- ✅ Multilingual accessibility 