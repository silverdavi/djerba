#!/bin/bash
# Build Silver Cooks book cover

cd "$(dirname "$0")"

echo "Building Silver Cooks book cover..."
echo "=================================="

# Use lualatex for fontspec support
lualatex -interaction=nonstopmode cover.tex

if [ -f cover.pdf ]; then
    echo ""
    echo "✅ Cover generated: cover.pdf"
    echo "   Dimensions: 16.95\" × 8.25\" (with 0.125\" bleed)"
    echo ""
    # Open on macOS
    if command -v open &> /dev/null; then
        open cover.pdf
    fi
else
    echo "❌ Build failed"
    exit 1
fi

