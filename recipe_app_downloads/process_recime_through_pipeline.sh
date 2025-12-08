#!/bin/bash
# Process ReciMe recipes through the full Gemini pipeline
# This script veganizes, translates, and generates images for all 36 recipes

set -e

cd "$(dirname "$0")/.."

echo "════════════════════════════════════════════════════════════════"
echo "  ReciMe Recipes → Full Pipeline Processing"
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check if transform_recipes_gemini.py exists
if [ ! -f "transform_recipes_gemini.py" ]; then
    echo "❌ Error: transform_recipes_gemini.py not found in $(pwd)"
    exit 1
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found. Please create it with your GOOGLE_API_KEY"
    exit 1
fi

echo "📂 Source recipes: data/safed_recipes_recime/"
echo "📤 Output location: data/recipes_multilingual/"
echo "🖼️  Images: data/images/generated/"
echo ""

# Count recipes
RECIPE_COUNT=$(ls -1 data/safed_recipes_recime/*.json 2>/dev/null | wc -l)
echo "📊 Found $RECIPE_COUNT recipes to process"
echo ""

# Show pipeline options
echo "════════════════════════════════════════════════════════════════"
echo "Choose your processing option:"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "  1) Fast - JSON only (no images) - ~2 minutes"
echo "     └─ Veganize + Translate to 4 languages"
echo ""
echo "  2) Medium - With images - ~15-20 minutes"
echo "     └─ Veganize + Translate + Generate AI images"
echo ""
echo "  3) First recipe only (test) - ~30 seconds"
echo "     └─ Test with first recipe to verify setup"
echo ""
echo "  4) Cancel"
echo ""
read -p "Select option (1-4): " OPTION

case $OPTION in
    1)
        echo ""
        echo "🚀 Starting pipeline (JSON only)..."
        echo ""
        python3 transform_recipes_gemini.py \
            --start 0 \
            --limit $RECIPE_COUNT
        ;;
    2)
        echo ""
        echo "🚀 Starting pipeline (with images)..."
        echo ""
        echo "⚠️  Note: This will take ~15-20 minutes and use API credits"
        echo "          for image generation (~36 images at ~$0.05 each)"
        echo ""
        read -p "Continue? (y/n): " CONFIRM
        if [ "$CONFIRM" = "y" ] || [ "$CONFIRM" = "Y" ]; then
            python3 transform_recipes_gemini.py \
                --start 0 \
                --limit $RECIPE_COUNT \
                --with-images
        else
            echo "Cancelled"
            exit 0
        fi
        ;;
    3)
        echo ""
        echo "🧪 Testing with first recipe..."
        echo ""
        FIRST_RECIPE=$(ls -1 data/safed_recipes_recime/*.json | head -1 | xargs basename)
        python3 transform_recipes_gemini.py \
            --single "$FIRST_RECIPE" \
            --with-images
        ;;
    4)
        echo "Cancelled"
        exit 0
        ;;
    *)
        echo "❌ Invalid option"
        exit 1
        ;;
esac

echo ""
echo "════════════════════════════════════════════════════════════════"
echo "✅ Processing complete!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📁 Recipes saved to: data/recipes_multilingual/"
if [ "$OPTION" = "2" ]; then
    echo "🖼️  Images saved to: data/images/generated/"
fi
echo ""
