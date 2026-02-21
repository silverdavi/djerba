#!/bin/bash
# Build Silver Cooks book cover

cd "$(dirname "$0")"

echo "Building Silver Cooks book cover..."
echo "=================================="

# First, build the ISBN barcode
echo "Building ISBN barcode..."
lualatex -interaction=nonstopmode isbn_barcode.tex > /dev/null 2>&1
if [ -f isbn_barcode.pdf ]; then
    echo "✅ ISBN barcode generated"
else
    echo "❌ ISBN barcode failed"
    exit 1
fi

# Use lualatex for fontspec support - TWO PASSES
echo "Pass 1..."
lualatex -interaction=nonstopmode cover.tex > /dev/null 2>&1

echo "Pass 2..."
lualatex -interaction=nonstopmode cover.tex

if [ -f cover.pdf ]; then
    echo ""
    echo "✅ Cover generated: cover.pdf"
    echo "   Dimensions: 17.95\" × 8.5\" (with 0.125\" bleed)"
    echo ""
    # Open on macOS
    if command -v open &> /dev/null; then
        open cover.pdf
    fi
else
    echo "❌ Build failed"
    exit 1
fi
