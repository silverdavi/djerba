#!/bin/bash
cd "$(dirname "$0")"
echo "Building cover85b (18.375 x 8.5)..."
lualatex -interaction=nonstopmode cover85b.tex > /dev/null 2>&1
lualatex -interaction=nonstopmode cover85b.tex
if [ -f cover85b.pdf ]; then
    echo "✅ cover85b.pdf generated (18.375\" × 8.5\")"
    open cover85b.pdf
fi
