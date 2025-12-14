#!/bin/bash
# Build Silver Cooks book cover (8.5" x 8.5" version)

cd "$(dirname "$0")"

echo "Building Silver Cooks book cover (8.5\" x 8.5\")..."
echo "=================================================="

# Use lualatex for fontspec support - TWO PASSES
echo "Pass 1..."
lualatex -interaction=nonstopmode cover85.tex > /dev/null 2>&1

echo "Pass 2..."
lualatex -interaction=nonstopmode cover85.tex

if [ -f cover85.pdf ]; then
    echo ""
    echo "✅ Cover generated: cover85.pdf"
    echo "   Dimensions: 18.23\" × 8.75\" (8.5x8.5 pages + 0.98 spine + bleed)"
    echo ""
    # Open on macOS
    if command -v open &> /dev/null; then
        open cover85.pdf
    fi
else
    echo "❌ Build failed"
    exit 1
fi

